import time
import datetime
from datetime import date
import MySQLdb

db = MySQLdb.connect(host="localhost",user="raspi", passwd="raspberry",db="clima") #conecta con  MySQL/MariaDB
cur = db.cursor() #crea el cursor para las peticiones de  MySQL/MariaDB

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

# Inicializa el BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

# Descartando el primer valor
temperatura = bme280.get_temperature()
presion = bme280.get_pressure()
humedad = bme280.get_humidity()
print('Comienzo de lectura en 3 segundos')
time.sleep(3)


while True:
    temperatura = bme280.get_temperature()
    presion = bme280.get_pressure()
    humedad = bme280.get_humidity()
    fecha = date.today()
    hora = datetime.datetime.now().time()
    print (fecha), "-", unicode(hora.replace(microsecond=0))
    print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperatura, presion, humedad))
    time.sleep(300)

    cur.execute('''INSERT INTO BME280_Data(temperatura,presion,humedad) VALUES(%s,%s,%s);''',(temperatura,presion,humedad))
    db.commit()

