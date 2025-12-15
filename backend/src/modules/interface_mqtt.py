import paho.mqtt.client as mqtt

class interface_mqtt:
    def __init__(self, broker, porta, topicos, client_id = "", callback_on_message = None):
        self.broker = broker
        self.porta = porta
        self.client_id = client_id
        self.topicos = topicos

        self.cliente = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, self.client_id)
        self.cliente.on_connect = self.on_connect
        self.callback_on_message = self.callback_padrao if callback_on_message == None else callback_on_message
        self.cliente.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Conectado ao Broker HiveMQ!")
            for topico in self.topicos:
                self.inscrever(topico)
        else:
            print(f"Falha na conexão, código de retorno: {rc}")

    def inscrever(self, topico):
        self.cliente.subscribe(topico)

    def on_message(self, client, userdata, msg):
        payload_decoded = msg.payload.decode()
        if self.callback_on_message:
            self.callback_on_message(msg.topic, payload_decoded)

    def callback_padrao(self, topico, payload):
        print("--- [Callback Padrão da Classe] ---")
        print(f"Mensagem recebida no tópico: '{topico}'")
        print(f"Conteúdo (Payload): '{payload}'")
        print("-----------------------------------\n")

    def set_callback_on_message(self, callback_func):
        self.callback_on_message = callback_func

    def rodar(self): 
        try:
            self.cliente.connect(self.broker, self.porta)
            self.cliente.loop_forever()
        except KeyboardInterrupt:
            print("\nLoop interrompido pelo usuário. Desconectando...")
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
        finally:
            self.cliente.disconnect()
            print("Cliente desconectado.")