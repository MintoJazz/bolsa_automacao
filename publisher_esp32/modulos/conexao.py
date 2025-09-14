from network import WLAN,STA_IF
from time import sleep, localtime, time
from machine import reset, RTC
from ntp import settime
from umqtt.simple import MQTTClient

def conectar_wifi(lcd, ssid, pswd):
    lcd.clear()
    lcd.putstr("Conectando WiFi...")
    sta_if = WLAN(STA_IF)

    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, pswd)
        timeout = 15
        while not sta_if.isconnected() and timeout > 0:
            sleep(1)
            timeout -= 1

    if sta_if.isconnected():
        lcd.putstr("\nConectado!")
        sleep(1)
    else:
        lcd.putstr("\nFalha no WiFi!")
        sleep(3)
        reset()

def ajustar_hora_ntp(lcd):
    lcd.clear()
    lcd.putstr("Sincronizando hora...")
    
    try:
        settime()
        # Lembrete: ajustar para o fuso UTC-3 (Brasília)
        agora_utc = time()
        fuso_horario_offset = -3 * 3600
        tm = localtime(agora_utc + fuso_horario_offset)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
        lcd.putstr("\nHora ajustada!")
    except Exception as e:
        lcd.putstr("\nErro NTP!")
    time.sleep(1)

def conectar_mqtt(lcd, client_id, mqtt_broker, mqtt_port):
    lcd.clear()
    lcd.putstr("Conectando MQTT...")
    client = MQTTClient(client_id, mqtt_broker, port=mqtt_port)
    try:
        client.connect()
        lcd.putstr("\nMQTT Conectado!")
        time.sleep(1)
    except OSError as e:
        lcd.putstr("\nFalha no MQTT!")
        time.sleep(3)
        reset()

def timestamp():
    tupla_data = RTC().datetime()
    return f"{tupla_data[0]}-{tupla_data[1]}-{tupla_data[2]} {tupla_data[4]}:{tupla_data[5]}:{tupla_data[6]}.{tupla_data[7]}"