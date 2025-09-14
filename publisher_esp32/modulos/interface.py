from machine import reset
from umqtt.simple import MQTTClient

class cliente_mqtt:
    def __init__(self, broker, lcd = None, id_cliente = ''):
        self.broker = broker
        self.lcd = lcd
        self.id_cliente = id_cliente

        self.cliente = MQTTClient(self.id_cliente, self.broker)
        self.cliente.connect()

    def publicar(self, mensagem, topico):
        self.cliente.publish(
            topico.encode(),
            mensagem.encode()
        )