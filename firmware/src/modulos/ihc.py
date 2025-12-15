from .lib.machine_i2c_lcd import I2cLcd

class meu_lcd:
    def __init__(self, bus_i2c, endereco, linhas, colunas):
        self.bus_i2c = bus_i2c
        self.endereco = endereco
        self.linhas = linhas
        self.colunas = colunas

        self.display = [[' ' for coluna in range(0,self.colunas)] for linha in range(0,self.linhas)]

        self.lcd = I2cLcd(
            self.bus_i2c, 
            self.endereco,
            self.linhas, 
            self.colunas
        )

    def imprimir(self, texto, linha = 0):
        if linha == 0: self.limpar_painel()
        
        diff = self.colunas - len(texto)

        lista_linha = [texto[caracter] for caracter in (range(self.colunas) if diff < 0 else range(len(texto)))]
        for _ in (range(diff) if diff > 0 else range(0)): lista_linha.append(" ")
        
        if lista_linha == self.display[linha]: return

        for coluna,caracter in enumerate(lista_linha): 
            if caracter != self.display[linha][coluna]: 
                self.display[linha][coluna] = caracter
                self.lcd.move_to(coluna,linha)
                self.lcd.putchar(self.display[linha][coluna])

    def limpar_painel(self):
        self.display = [[' ' for coluna in range(0,self.colunas)] for linha in range(0,self.linhas)]
        self.lcd.clear()