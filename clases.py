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
        self.columaError = 0

