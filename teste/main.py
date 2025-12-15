from modulos.sensores import temperatura_ds18b20
from utime import sleep

ds = temperatura_ds18b20(4)

while True:
    sleep(3)
    print(ds.ler_sensor())