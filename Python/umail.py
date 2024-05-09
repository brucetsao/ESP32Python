# uMail (MicroMail) for MicroPython
# SMTP（簡單郵件傳輸協定）的MicroPython版本
#這個 MicroPython 程式實現了 SMTP（簡單郵件傳輸協定）的基本功能，
# 允許 MicroPython 與 SMTP 伺服器通信。
# 註解詳細解釋了 SMTP 類的初始化、身份驗證、設置郵件接收者、發送郵件、關閉連接等功能。
# 該程式使用套接字進行網路通信，並提供多種身份驗證方式。
# 程式中還解釋了 SMTP 命令和 SSL/TLS 安全連接的相關過程。

import usocket  # 引入網路通訊的套件

# 一些 SMTP 預設的常數和命令
DEFAULT_TIMEOUT = 10  # 預設超時時間，單位為秒
LOCAL_DOMAIN = '127.0.0.1'  # 預設本地域名
CMD_EHLO = 'EHLO'  # SMTP 命令
CMD_STARTTLS = 'STARTTLS'  # SMTP 命令，用於啟用 TLS 安全連接
CMD_AUTH = 'AUTH'  # SMTP 命令，用於身份驗證
CMD_MAIL = 'MAIL'  # SMTP 命令，用於開始郵件發送
AUTH_PLAIN = 'PLAIN'  # 簡單身份驗證
AUTH_LOGIN = 'LOGIN'  # 登入身份驗證

# SMTP 類別，用於與 SMTP 伺服器進行通信
class SMTP:
    # 執行 SMTP 命令
    def cmd(self, cmd_str):
        sock = self._sock  # 獲取連接的 Socket
        sock.write('%s\r\n' % cmd_str)  # 發送命令
        resp = []  # 儲存回應訊息
        next = True  # 用於檢查回應是否還在繼續
        while next:
            code = sock.read(3)  # 讀取回應碼
            next = sock.read(1) == b'-'  # 檢查回應是否有下一行
            resp.append(sock.readline().strip().decode())  # 讀取回應
        return int(code), resp  # 回傳回應碼和回應內容

    # SMTP 初始化函式
    def __init__(self, host, port, ssl=False, username=None, password=None):
        import ussl  # 引入 SSL 套件
        self.username = username  # 設置用戶名
        addr = usocket.getaddrinfo(host, port)[0][-1]  # 取得伺服器地址
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)  # 建立 Socket
        sock.settimeout(DEFAULT_TIMEOUT)  # 設置超時時間
        sock.connect(addr)  # 連接伺服器
        if ssl:
            sock = ussl.wrap_socket(sock)  # 如果使用 SSL，則包裝 Socket
        code = int(sock.read(3))  # 讀取伺服器的回應碼
        sock.readline()  # 讀取剩餘的行
        assert code == 220, '無法連接到伺服器，回應碼：%d, %s' % (code, resp)
        self._sock = sock  # 儲存連接的 Socket

        # 驗證伺服器支持的命令
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)  # 發送 EHLO 命令
        assert code == 250, 'EHLO 命令失敗，回應碼：%d' % code
        if not ssl and CMD_STARTTLS in resp:
            code, resp = self.cmd(CMD_STARTTLS)  # 發送 STARTTLS 命令
            assert code == 220, 'STARTTLS 命令失敗，回應碼：%d, %s' % (code, resp)
            self._sock = ussl.wrap_socket(sock)  # 再次包裝 Socket 以啟用 TLS

        # 如果需要身份驗證
        if username and password:
            self.login(username, password)  # 執行登入流程

    # 用於 SMTP 身份驗證的登入函式
    def login(self, username, password):
        self.username = username  # 儲存用戶名
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)  # 發送 EHLO 命令
        assert code == 250, 'EHLO 命令失敗，回應碼：%d, %s' % (code, resp)

        # 驗證支持的身份驗證方法
        auths = None
        for feature in resp:
            if feature[:4].upper() == CMD_AUTH:  # 找到支持的身份驗證方法
                auths = feature[4:].strip('=').upper().split()
        assert auths is not None, "沒有支持的身份驗證方法"

        from ubinascii import b2a_base64 as b64  # 用於 Base64 編碼
        if AUTH_PLAIN in auths:  # 使用簡單身份驗證
            cren = b64("\0%s\0%s" % (username, password))[:-1].decode()  # 編碼用戶名和密碼
            code, resp = self.cmd('%s %s %s' % (CMD_AUTH, AUTH_PLAIN, cren))
        elif AUTH_LOGIN in auths:  # 使用登入身份驗證
            code, resp = self.cmd("%s %s %s" % (CMD_AUTH, AUTH_LOGIN, b64(username)[:-1].decode()))
            assert code == 334, '用戶名錯誤，回應碼：%d, %s' % (code, resp)
            code, resp = self.cmd(b64(password)[:-1].decode())  # 驗證密碼
        else:
            raise Exception("不支持的身份驗證方法 (%s)" % ', '.join(auths))  # 若不支持則拋出異常

        assert code == 235 or code == 503, '身份驗證失敗，回應碼：%d, %s' % (code, resp)
        return code, resp  # 回傳驗證結果

    # 設置郵件接收者
    def to(self, addrs, mail_from=None):
        mail_from = self.username if mail_from is None else mail_from  # 設置發件人
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)  # 發送 EHLO 命令
        assert code == 250, 'EHLO 命令失敗，回應碼：%d' % code
        code, resp = self.cmd('MAIL FROM: <%s>' % mail_from)  # 發送郵件發件人命令
        assert code == 250, '發件人被拒絕，回應碼：%d, %s' % (code, resp)

        if isinstance(addrs, str):
            addrs = [addrs]  # 如果接收者是字串，轉換為清單
        count = 0
        for addr in addrs:
            code, resp = self.cmd('RCPT TO: <%s>' % addr)  # 發送郵件接收者命令
            if code != 250 and code != 251:
                print('%s 被拒絕，回應：%s' % (addr, resp))
                count += 1  # 若被拒絕則計數
        assert count != len(addrs), '所有接收者被拒絕，回應碼：%d, %s' % (code, resp)

        code, resp = self.cmd('DATA')  # 開始發送郵件
        assert code == 354, '郵件數據被拒絕，回應碼：%d, %s' % (code, resp)
        return code, resp

    # 用於寫入郵件內容
    def write(self, content):
        self._sock.write(content)  # 寫入郵件內容

    # 用於發送郵件
    def send(self, content=''):
        if content:
            self.write(content)  # 如果有內容，則寫入
        self._sock.write('\r\n.\r\n')  # 以 ".\r\n" 標記郵件結束
        line = self._sock.readline()  # 讀取伺服器回應
        return (int(line[:3]), line[4:].strip().decode())  # 回傳回應碼和回應內容

    # 用於關閉連接
    def quit(self):
        self.cmd("QUIT")  # 發送退出命令
        self._sock.close()  # 關閉連接
