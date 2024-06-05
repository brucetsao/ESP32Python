# 這個程式定義了 MQTTClient 類，用於處理 MQTT 連接和消息傳輸。
# 包含初始化、連接、發送、訂閱、等待消息、檢查消息等功能。
# 使用註解詳細解釋了每個方法的作用和邏輯。
# 這個程式通過 Socket 進行網絡通信，並提供 SSL 支持。
# MQTTClient 類處理 MQTT 協議中的基本操作，
# 包括連接、發送消息、訂閱主題和處理消息。
try:
    import usocket as socket  # 嘗試引入 usocket 以確保兼容
except:
    import socket  # 如果 usocket 不可用，則引入 socket
import ustruct as struct  # 使用 ustruct 進行二進位數據處理
from ubinascii import hexlify  # 用於十六進位表示

# 自定義 MQTT 例外，用於錯誤處理
class MQTTException(Exception):
    pass

# MQTT 客戶端類，用於處理 MQTT 連接和消息傳輸
class MQTTClient:

    # 初始化 MQTT 客戶端
    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        if port == 0:
            port = 8883 if ssl else 1883  # 默認端口，根據 SSL 設置
        self.client_id = client_id  # 客戶端 ID
        self.sock = None  # 初始化 socket
        self.server = server  # MQTT 伺服器地址
        self.port = port  # MQTT 伺服器端口
        self.ssl = ssl  # 是否使用 SSL
        self.ssl_params = ssl_params  # SSL 參數
        self.pid = 0  # MQTT 報文 ID
        self.cb = None  # 回調函數
        self.user = user  # 用戶名
        self.pswd = password  # 密碼
        self.keepalive = keepalive  # 保持連接的週期
        self.lw_topic = None  # 最後遺言主題
        self.lw_msg = None  # 最後遺言消息
        self.lw_qos = 0  # 最後遺言的 QOS 等級
        self.lw_retain = False  # 是否保留最後遺言

    # 發送字串
    def _send_str(self, s):
        self.sock.write(struct.pack("!H", len(s)))  # 發送字串長度
        self.sock.write(s)  # 發送字串內容

    # 接收長度
    def _recv_len(self):
        n = 0
        sh = 0
        while True:
            b = self.sock.read(1)[0]  # 讀取一個字節
            n |= (b & 0x7f) << sh  # 使用移位和 OR 計算長度
            if not b & 0x80:  # 如果最高位不是 1，則表示結束
                return n
            sh += 7  # 每次移位 7 位

    # 設置回調函數
    def set_callback(self, f):
        self.cb = f  # 設置回調函數

    # 設置最後遺言
    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2  # 確保 QOS 在合法範圍內
        assert topic  # 確保主題不為空
        self.lw_topic = topic  # 設置最後遺言的主題
        self.lw_msg = msg  # 設置最後遺言的消息
        self.lw_qos = qos  # 設置最後遺言的 QOS 等級
        self.lw_retain = retain  # 設置是否保留最後遺言

    # 連接到 MQTT 伺服器
    def connect(self, clean_session=True):
        self.sock = socket.socket()  # 創建 socket
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]  # 取得伺服器地址
        self.sock.connect(addr)  # 連接到伺服器
        if self.ssl:
            import ussl  # 引入 SSL 套件
            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)  # 包裝 socket 以使用 SSL
        premsg = bytearray(b"\x10\0\0\0\0\0")  # 預設的連接訊息
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")  # MQTT 版本訊息

        # 計算消息的大小
        sz = 10 + 2 + len(self.client_id)  # 計算所需的字節大小
        msg[6] = clean_session << 1  # 根據是否是清理會話設置標記
        if self.user is not None:
            sz += 2 + len(self.user) + 2 + len(self.pswd)  # 如果有用戶名和密碼，則增加大小
            msg[6] |= 0xC0  # 設置標記
        if self.keepalive:
            assert self.keepalive < 65536  # 確保 keepalive 在合法範圍內
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0x00FF
        if self.lw_topic:
            sz += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)  # 增加最後遺言的大小
            msg[6] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[6] |= self.lw_retain << 5

        # 編碼 MQTT 消息的長度
        i = 1
        while sz > 0x7f:
            premsg[i] = (sz & 0x7f) | 0x80  # 使用多字節編碼
            sz >>= 7
            i += 1
        premsg[i] = sz

        self.sock.write(premsg, i + 2)  # 發送預設的連接訊息
        self.sock.write(msg)  # 發送 MQTT 版本訊息
        #print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)  # 發送客戶端 ID
        if self.lw_topic:
            self._send_str(self.lw_topic)  # 發送最後遺言的主題
            self._send_str(self.lw_msg)  # 發送最後遺言的消息
        if self.user is not None:
            self._send_str(self.user)  # 發送用戶名
            self._send_str(self.pswd)  # 發送密碼
        resp = self.sock.read(4)  # 讀取伺服器的回應
        assert resp[0] == 0x20 and resp[1] == 0x02  # 確保回應合法
        if resp[3] != 0:
            raise MQTTException(resp[3])  # 如果回應碼不為 0，則拋出例外
        return resp[2] & 1  # 返回 MQTT 連接標記

    # 中斷與 MQTT 伺服器的連接
    def disconnect(self):
        self.sock.write(b"\xe0\0")  # 發送中斷訊息
        self.sock.close()  # 關閉 socket

    # 發送 ping
    def ping(self):
        self.sock.write(b"\xc0\0")  # 發送 ping 訊息

    # 發送 MQTT 訊息
    def publish(self, topic, msg, retain=False, qos=0):
        pkt = bytearray(b"\x30\0\0\0")  # 預設 MQTT 發送訊息
        pkt[0] |= qos << 1 | retain  # 設置 QOS 和是否保留
        sz = 2 + len(topic) + len(msg)  # 計算 MQTT 消息大小
        if qos > 0:
            sz += 2  # 如果 QOS 大於 0，則增加大小
        assert sz < 2097152  # 確保消息大小在合法範圍內
        i = 1
        while sz > 0x7f:
            pkt[i] = (sz & 0x7f) | 0x80  # 編碼消息大小
            sz >>= 7
            i += 1
        pkt[i] = sz  # 設置最後的消息大小
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)  # 發送 MQTT 訊息標記
        self._send_str(topic)  # 發送主題
        if qos > 0:
            self.pid += 1  # 增加 MQTT 報文 ID
            pid = self.pid  # 設置報文 ID
            struct.pack_into("!H", pkt, 0, pid)  # 包裝報文 ID
            self.sock.write(pkt, 2)  # 發送報文 ID
        self.sock.write(msg)  # 發送消息
        if qos == 1:  # 如果 QOS 為 1，等待回應
            while True:
                op = self.wait_msg()  # 等待消息
                if op == 0x40:  # 如果回應為 PUBACK
                    sz = self.sock.read(1)  # 讀取大小
                    assert sz == b"\x02"  # 確保大小合法
                    rcv_pid = self.sock.read(2)  # 讀取接收到的報文 ID
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]  # 計算報文 ID
                    if pid == rcv_pid:
                        return  # 如果報文 ID 一致，則返回
        elif qos == 2:  # 如果 QOS 為 2，拋出例外
            assert 0

    # 訂閱主題
    def subscribe(self, topic, qos=0):
        assert self.cb is not None, "必須設置訂閱回調函數"
        pkt = bytearray(b"\x82\0\0\0")  # 預設 MQTT 訂閱訊息
        self.pid += 1  # 增加報文 ID
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)  # 包裝訂閱訊息
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt)  # 發送訂閱訊息
        self._send_str(topic)  # 發送訂閱主題
        self.sock.write(qos.to_bytes(1, "little"))  # 發送 QOS 等級
        while True:
            op = self.wait_msg()  # 等待回應
            if op == 0x90:  # 如果收到 SUBACK
                resp = self.sock.read(4)  # 讀取回應
                #print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]  # 確保回應 ID 正確
                if resp[3] == 0x80:  # 如果訂閱失敗
                    raise MQTTException(resp[3])  # 拋出例外
                return  # 返回成功

    # 等待單個 MQTT 消息
    def wait_msg(self):
        res = self.sock.read(1)  # 讀取一個字節
        self.sock.setblocking(True)  # 設置 socket 阻塞
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)  # 如果為空，拋出錯誤
        if res == b"\xd0":  # PINGRESP
            sz = self.sock.read(1)[0]  # 讀取大小
            assert sz == 0  # 確保大小合法
            return None
        op = res[0]  # 取得操作碼
        if op & 0xf0 != 0x30:  # 如果不是 PUBLISH
            return op
        sz = self._recv_len()  # 取得消息長度
        topic_len = self.sock.read(2)  # 讀取主題長度
        topic_len = (topic_len[0] << 8) | topic_len[1]  # 計算主題長度
        topic = self.sock.read(topic_len)  # 讀取主題
        sz -= topic_len + 2  # 調整消息大小
        if op & 6:
            pid = self.sock.read(2)  # 讀取報文 ID
            pid = pid[0] << 8 | pid[1]  # 計算報文 ID
            sz -= 2  # 調整消息大小
        msg = self.sock.read(sz)  # 讀取消息
        self.cb(topic, msg)  # 調用回調函數
        if op & 6 == 2:
            pkt = bytearray(b"\x40\x02\0\0")  # PUBACK
            struct.pack_into("!H", pkt, 2, pid)  # 包裝報文 ID
            self.sock.write(pkt)  # 發送 PUBACK
        elif op & 6 == 4:
            assert 0

    # 檢查是否有來自伺服器的待處理消息
    def check_msg(self):
        self.sock.setblocking(False)  # 設置非阻塞
        return self.wait_msg()  # 檢查消息
