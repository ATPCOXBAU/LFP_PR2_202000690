class Token:
    def __init__(self, tipo, lexema, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.columna = columna - len(lexema)



class Error:
    def __init__(self, tipo, lexema, columna):
        self.tipo = tipo
        self.lexema = lexema
        self.columna = columna - len(lexema)

    def getInfo(self):
        print('\n***** ***** ***** *****')
        print('Tipo:', self.tipo)
        print('Lexema:', self.lexema)
        print('Columna:', self.columna)
