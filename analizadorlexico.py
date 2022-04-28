import re
from clases import Token as tkk
from clases import Error


class Analizadorexico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []

    def limpiar(self, tipo):
        if tipo == 'errores':
            self.listaErrores = []
        elif tipo == 'tokens':
            self.listaTokens = []

    def palabrasRES(self, buffer):
        if buffer == 'TOTAL':
            return True
        elif buffer == 'PARTIDOS':
            return True
        elif buffer == 'RESULTADO':
            return True
        elif buffer == 'JORNADA':
            return True
        elif buffer == 'VS':
            return True
        elif buffer == 'TOP':
            return True
        elif buffer == 'SUPERIOR':
            return True
        elif buffer == 'INFERIOR':
            return True
        elif buffer == '-ji':
            return True
        elif buffer == '-jf':
            return True
        elif buffer == '-n':
            return True
        elif buffer == '-f':
            return True
        elif buffer == 'TEMPORADA':
            return True
        elif buffer == 'GOLES':
            return True
        elif buffer == 'LOCAL':
            return True
        elif buffer == 'VISITANTE':
            return True
        elif buffer == 'ADIOS':
            return True
        elif buffer == 'TABLA':
            return True
        elif buffer == 'ADIOS':
            return True
        else:
            return False

    def analizar(self, entrada):
        buffer = ''
        centinela = '&'
        entrada += centinela
        columna = 1
        estado = 0
        index = 0
        largo =len(entrada)
        while index < len(entrada):
            caracter = entrada[index]
            if estado == 0:
                if caracter.isdigit():
                    columna += 1
                    buffer += caracter
                    estado = 1
                elif caracter == '-' or re.search('[A-Za-z_ÑñÁáÉéÍíÓóÚú]', caracter) :
                    columna += 1
                    buffer += caracter
                    estado = 2
                elif caracter == '<':
                    columna += 1
                    buffer += caracter
                    token = tkk('MENORQUE', buffer, columna)
                    self.listaTokens.append(token)
                    buffer = ''
                    estado = 0
                elif caracter == '>':
                    columna += 1
                    buffer += caracter
                    token = tkk('MAYORQUE', buffer, columna)
                    self.listaTokens.append(token)
                    buffer = ''
                    estado = 0
                elif caracter == '\"':
                    columna += 1
                    buffer += caracter
                    estado = 3
                elif caracter == " ":
                    columna += 1
                    estado = 0
                elif caracter == '\t':
                    columna += 4
                    estado = 0
                elif caracter == centinela:
                    columna += 1
                    buffer += caracter
                    if index == len(entrada) - 1:
                        token = tkk('FinalAn', buffer, columna)
                        self.listaTokens.append(token)
                    else:
                        error = Error('Error Lexico', buffer, columna)
                        self.listaErrores.append(error)
                        buffer = ' '
                    buffer = ''
                    estado = 0
            elif estado == 1:
                if caracter.isdigit():
                    columna += 1
                    buffer += caracter
                    estado = 1
                elif re.search('[A-Za-z_ÑñÁáÉéÍíÓóÚú]', caracter):
                        buffer += caracter
                        error = Error('Error Lexico', buffer, columna)
                        self.listaErrores.append(error)
                        buffer = ''
                        estado = 0
                else:
                    if caracter != centinela:
                        columna +=1
                        token = tkk('ENTERO', buffer, columna)
                        self.listaTokens.append(token)
                        buffer = ''
                        estado = 0
                    elif caracter == centinela:
                        index -= 1
                        columna += 1
                        token = tkk('ENTERO', buffer, columna)
                        self.listaTokens.append(token)
                        buffer = ''
                        estado = 0

                if caracter == '-':
                    columna +=1
                    token = tkk('GUION', caracter, columna)
                    self.listaTokens.append(token)
                    estado = 0

                if caracter == '>':
                    columna += 1
                    token = tkk('MAYORQUE', caracter, columna)
                    self.listaTokens.append(token)
                    estado = 0


            elif estado == 2:
                if caracter == '-' or re.search('[A-Za-z_ÑñÁáÉéÍíÓóÚú]', caracter) or caracter == '_' or caracter.isdigit():
                    estado = 2
                    columna += 1
                    buffer += caracter
                else:
                    tipoToken = ''
                    if buffer == 'TOTAL':
                        tipoToken = 'TOTAL'
                    elif buffer == 'PARTIDOS':
                        tipoToken = 'PARTIDOS'
                    elif buffer == 'RESULTADO':
                        tipoToken = 'RESULTADO'
                    elif buffer == 'JORNADA':
                        tipoToken = 'JORNADA'
                    elif buffer == 'VS':
                        tipoToken = 'VS'
                    elif buffer == 'TOP':
                        tipoToken = 'TOP'
                    elif buffer == 'SUPERIOR':
                        tipoToken = 'SUPERIOR'
                    elif buffer == 'INFERIOR':
                        tipoToken = 'INFERIOR'
                    elif buffer == '-ji':
                        tipoToken = '-ji'
                    elif buffer == '-jf':
                        tipoToken = '-jf'
                    elif buffer == '-n':
                        tipoToken = '-n'
                    elif buffer == '-f':
                        tipoToken = '-f'
                    elif buffer == 'TEMPORADA':
                        tipoToken = 'TEMPORADA'
                    elif buffer == 'GOLES':
                        tipoToken = 'GOLES'
                    elif buffer == 'LOCAL':
                        tipoToken = 'LOCAL'
                    elif buffer == 'VISITANTE':
                        tipoToken = 'VISITANTE'
                    elif buffer == 'ADIOS':
                        tipoToken = 'ADIOS'
                    elif buffer == 'TABLA':
                        tipoToken = 'TABLA'

                    else:
                        tipoToken = 'IDENTIFICADOR'

                    if self.palabrasRES(buffer) or tipoToken == 'IDENTIFICADOR':

                        token = tkk(tipoToken, buffer, columna)
                        self.listaTokens.append(token)
                        buffer = ''
                        index -=1
                        estado = 0
                    else:

                        buffer += caracter
                        error = Error('Error Lexico', buffer, columna)
                        self.listaErrores.append(error)
                        buffer = ''
                        estado = 0

            elif estado == 3:
                if caracter == '"':
                    columna += 1
                    buffer += caracter
                    token = tkk('CADENA', buffer, columna)
                    self.listaTokens.append(token)
                    buffer = ''
                    estado = 0
                elif caracter != "\"":
                    columna +=1
                    buffer += caracter
                    estado = 3
            index += 1
        return entrada
