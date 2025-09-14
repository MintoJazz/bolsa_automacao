from modulos.conexao import conectar_wifi, ajustar_hora_ntp, timestamp
from modulos.sensores import temperatura_ds18b20, pressao_bmp180, umidade_dht22
from modulos.interface import cliente_mqtt
from modulos.lib.machine_i2c_lcd import I2cLcd
from machine import I2C, Pin, reset
from ujson import load, dumps
from time import sleep

with open('config.json','r') as arquivo:
    assets = load(arquivo)

sensor = []

try:
    print("Gerando bus...")
    bus_i2c = I2C(
        1,
        sda = Pin(assets['pinos']['sda']),
        scl = Pin(assets['pinos']['scl']),
        freq = 100000
    )
    enderecos_dispositivos = bus_i2c.scan()
except Exception as e:
    print(f"Deu erro no I2C: {e}")

try:
    print("Ligando LCD")
    lcd = I2cLcd(
        bus_i2c, 
        enderecos_dispositivos[0],
        4, 
        20
    )
    lcd.clear()
    lcd.putstr("LCD e I2C Ok!")
except Exception as e:
    print(f"Deu erro no LCD: {e}")

sensor.append(
    pressao_bmp180(
        i2c_bus = bus_i2c
    )
)

sensor.append(
    umidade_dht22(
        pino = assets['pinos']['dht']
    )
)

sensor.append(
    temperatura_ds18b20(
        pino = assets['pinos']['onewire']
    )
)

try:
    lcd.clear()
    lcd.putstr("Conectando WiFi...")
    lcd.putstr(f"\n{conectar_wifi(assets['wifi']['ssid'],assets['wifi']['pswd'])}")
    sleep(2)
except Exception as e:
    lcd.putstr(f"\n{e}")
    sleep(3)
    reset()

try:
    lcd.clear()
    lcd.putstr("Sincronizando hora...")
    lcd.putstr(f"\n{ajustar_hora_ntp()}")
    sleep(2)
except Exception as e:
    lcd.putstr(f"\n{e}")
    sleep(3)

try:
    lcd.clear()
    lcd.putstr('Conectando MQTT...')
    cliente = cliente_mqtt(
        broker = assets['mqtt']['broker'],
        id_cliente = assets['mqtt']['id_cliente']
    )
    lcd.putstr('\nMQTT Conectado!')
    sleep(2)
except Exception as e:
    lcd.putstr(f"\n{e}")
    sleep(3)
    reset()

while True:
    json_pub = {'timestamp':timestamp()}

    output = 'Medicoes'

    for i in range(0,len(sensor)):
        json_pub[sensor[i].tipo] = sensor[i].ler_sensor()
        output += f'\n{sensor[i].tipo}: {json_pub[sensor[i].tipo]}'
        sleep(0.1)

    lcd.clear()
    lcd.putstr(output)
    
    cliente.publicar(
        mensagem = dumps(json_pub),
        topico = assets['mqtt']['topico']
    )
    sleep(0.5)