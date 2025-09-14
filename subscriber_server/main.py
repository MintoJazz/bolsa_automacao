from modules.interface_mqtt import interface_mqtt
import config

if __name__ == '__main__':
    cliente_mqtt = interface_mqtt(
        'broker.hivemq.com',
        1883,
        ['MintoJazz/JaazielPontoMqtt/teste']
    )

    cliente_mqtt.rodar() 