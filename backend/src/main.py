from modules.interface_mqtt import interface_mqtt
from json import load

with open('./config.json', 'r') as arquivo:
    config = load(arquivo)

if __name__ == '__main__':
    cliente_mqtt = interface_mqtt(
        config['broker'],
        config['porta'],
        config['topicos']
    )

    cliente_mqtt.rodar() 