from modulos.conexao import conectar_mqtt, conectar_wifi, ajustar_hora_ntp, timestamp
from modulos.sensores import temperatura_ds18b20, pressao_bmp180, umidade_dht22
from modulos.lib.machine_i2c_lcd import I2cLcd
from machine import I2C, Pin
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

    print("Ligando LCD")
    lcd = I2cLcd(
        bus_i2c, 
        enderecos_dispositivos[0],
        4, 
        20
    )
    lcd.clear()
    lcd.putstr("LCD e I2C Ok!")

    print("Criando BMP180...")
    sensor.append(
        pressao_bmp180(
            i2c_bus = bus_i2c
        )
    )

except Exception as e:
    print(f"Deu erro no I2C: {e}")

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

conectar_wifi(
    lcd,
    assets['wifi']['ssid'],
    assets['wifi']['pswd']
)

ajustar_hora_ntp(lcd)

conectar_mqtt(
    lcd,
    assets['mqtt']['client_id'],
    assets['mqtt']['broker'],
    assets['mqtt']['port']
)

cliente = cliente_mqtt(
    lcd = lcd,
    broker = assets['mqtt']['broker'],
    id_cliente = assets['mqtt']['id_cliente']
)

while True:
    lcd.clear()
    lcd.putstr('Medicoes')
    json_pub = {'timestamp':timestamp()}

    for i in range(0,len(sensor)):
        json_pub[sensor[i].tipo] = sensor[i].ler_sensor()
        lcd.move_to(0,(i+1))
        lcd.putstr(f'{sensor[i].tipo}: {json_pub[sensor[i].tipo]}')
        sleep(0.1)
    
    cliente.publicar(
        mensagem = dumps(json_pub),
        topico = assets['mqtt']['topico']
    )
    print(json_pub)
    sleep(0.5)