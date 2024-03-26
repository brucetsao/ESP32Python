from HTU21D	import HTU21D#使用HTU21DF
from myLib	import * #使用使用者自訂函數

lectura = HTU21D(22,21)
hum = lectura.humidity
temp = lectura.temperature
print('Humedad: ', + hum)
print('Temperatura: ', + temp)