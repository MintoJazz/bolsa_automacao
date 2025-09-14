from network import WLAN,STA_IF
from time import sleep, localtime, time
from machine import reset, RTC
from ntp import settime
from umqtt.simple import MQTTClient

def conectar_wifi(ssid, pswd):
    sta_if = WLAN(STA_IF)

    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect(ssid, pswd)
        timeout = 15
        while not sta_if.isconnected() and timeout > 0:
            sleep(1)
            timeout -= 1

    if not sta_if.isconnected(): # A conexão falhou
        sta_if.active(False) # Desliga a interface para economizar energia
        raise Exception('Falha no WiFi!')
    
    return 'Conectado!'

def ajustar_hora_ntp():
    try:
        settime()
        agora_utc = time()
        fuso_horario_offset = -3 * 3600
        tm = localtime(agora_utc + fuso_horario_offset)
        RTC().datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
        return 'Hora ajustada!'
    except Exception as e:
        raise Exception('Erro NTP!')

def timestamp():
    tupla_data = RTC().datetime()
    return f"{tupla_data[0]}-{tupla_data[1]}-{tupla_data[2]} {tupla_data[4]}:{tupla_data[5]}:{tupla_data[6]}.{tupla_data[7]}"