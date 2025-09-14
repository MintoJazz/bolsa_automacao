from machine import reset
from umqtt.simple import MQTTClient

class cliente_mqtt:
    def __init__(self, broker, id_cliente = ''):
        try:
            self.broker = broker
            self.id_cliente = id_cliente

            self.cliente = MQTTClient(self.id_cliente, self.broker)
            self.cliente.connect()
        except Exception as e:
            raise e

    def publicar(self, mensagem, topico):
        self.cliente.publish(
            topico.encode(),
            mensagem.encode()
        )