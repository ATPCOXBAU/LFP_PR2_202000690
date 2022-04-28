from clases import Error
import webbrowser
import sys


class analizadorsintactico:
    def __init__(self):
        self.instruccionDetectada = ''
        self.resultadoFinal = ''
        self.listaTokens = []
        self.listaErrores = []
        self.i = 0
        self.partidos = []
        self.instruccionencontrada = False

    def reutnError(self):
        return self.listaErrores

    def limpiar(self):
        self.listaErrores = []
        self.listaTokens = []

    def run(self):
        token = self.listaTokens[self.i]
        self.listaInstrucciones()
        token = self.listaTokens[self.i]
        if token.tipo == 'FinalAn':
            print('Se ha completado el Analisis Sintactico')

    def getinstrucciones(self, type):
        if type == 'RESULTADO' or type == 'JORNADA' or type == 'GOLES' or type == 'TABLA' \
                or type == 'PARTIDOS' or type == 'TOP' or type == 'ADIOS':
            return True
        else:
            return False

    def listaInstrucciones(self):
        if self.i < len(self.listaTokens) -1:
            token = self.listaTokens[self.i]
        else:
            token = self.listaTokens[len(self.listaTokens) - 1]
        type = token.tipo
        if self.getinstrucciones(type):
            self.instruccionencontrada = True
            self.instruccion()
            self.listaInstrucciones()

        elif type == 'FinalAn':
            return
        elif self.getinstrucciones(type) is False and self.instruccionencontrada == False:
            error = Error(f'SINTACTICO, Se esperaba  Una Instruccion', token.lexema, 0)
            error.columna = 1
            self.listaErrores.append(error)

    def instruccion(self):
        token = self.listaTokens[self.i]
        type = token.tipo
        if type == 'RESULTADO':

            self.resultado()
        elif type == 'JORNADA':
            self.jornada()
        elif type == 'GOLES':
            self.goles()
        elif type == 'TABLA':
            self.tabla()
        elif type == 'PARTIDOS':
            self.partidosins()
        elif type == 'TOP':
            self.top()
        elif type == 'ADIOS':
            self.adios()
        else:
            return

    def actualizarToken(self, posi):
        return self.listaTokens[posi]

    def declararError(self, contenido, token):

        error = Error(f'SINTACTICO, Se esperaba  {contenido}', token.lexema, token.columna + len(token.lexema))
        self.listaErrores.append(error)

    def adios(self):
        token = self.listaTokens[self.i]
        if token.tipo == 'ADIOS':
            self.i += 1
            self.respuestaADIOS()
        else:
            self.declararError('ADIOS', token)

    def comyear(self, firtstoken):
        anio1 = ''
        anio2 = ''
        completado = False
        if firtstoken.tipo == 'MENORQUE':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'ENTERO':
                anio1 = token.lexema
                self.i += 1
                token = self.actualizarToken(self.i)
                if token.tipo == 'GUION':
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    if token.tipo == 'ENTERO':
                        anio2 = token.lexema
                        self.i += 1
                        completado = True
                        print(self.i, len(self.listaTokens))
                        if self.i < len(self.listaTokens) - 1:
                            token = self.actualizarToken(self.i)
                            if token.tipo == 'MAYORQUE' and self.i <= len(self.listaTokens):
                                return [completado, anio1, anio2]
                            else:
                                self.declararError('MAYORQUE', token)
                                if completado is True:
                                    return [completado, anio1, anio2]
                                else:
                                    return [completado, anio1, anio2]
                        else:
                            self.declararError('MAYORQUE', token)
                            return [completado, anio1, anio2]
                    else:
                        token = self.actualizarToken(self.i)
                        self.declararError('ENTERO', token)
                        return [completado, anio1, anio2]
                else:
                    token = self.actualizarToken(self.i)
                    self.declararError('GUION', token)
                    return [completado, anio1, anio2]
            else:
                token = self.actualizarToken(self.i)

                self.declararError('ENTERO', token)
                return [completado, anio1, anio2]
        else:
            token = self.actualizarToken(self.i)
            self.declararError('MENORQUE', firtstoken)
            return [completado, anio1, anio2]

    def flagF(self, firstoken, nombregen):
        nombrearchv = nombregen
        if firstoken.tipo == '-f':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'IDENTIFICADOR':
                nombrearchv = token.lexema
                return nombrearchv
            else:
                self.declararError('IDFENTIFICADOR', token)
                return nombrearchv

        else:
            return nombrearchv

    def flagN(self, firstoken, nombregen):
        nombrearchv = nombregen
        if firstoken.tipo == '-n':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'ENTERO':
                nombrearchv = token.lexema
                return nombrearchv
            else:
                self.declararError('IDFENTIFICADOR', token)
                return nombrearchv
        else:
            return nombrearchv

    def resultado(self):
        equipo1 = ''
        equipo2 = ''
        anio1 = ''
        anio2 = ''

        token = self.listaTokens[self.i]
        if token.tipo == 'RESULTADO':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'CADENA':
                equipo1 = token.lexema
                self.i += 1
                token = self.actualizarToken(self.i)
                if token.tipo == 'VS':
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    if token.tipo == 'CADENA':
                        equipo2 = token.lexema

                        self.i += 1
                        token = self.actualizarToken(self.i)
                        if token.tipo == 'TEMPORADA':
                            self.i += 1
                            token = self.actualizarToken(self.i)
                            x = self.comyear(token)

                            if x[0] is True:
                                anio1 = x[1]
                                anio2 = x[2]
                                if self.i < len(self.listaTokens) -1:
                                    self.i+1
                                    token = self.actualizarToken(self.i)
                                if anio1 != '' and anio2 != '' and equipo1 != '' and equipo2 != '':
                                    temporada = anio1 + '-' + anio2
                                    self.respuestaRESULTADO(equipo1, equipo2, temporada)
                                pass
                            else:
                                return
                        else:
                            self.declararError('TEMPORADA', token)
                    else:
                        self.declararError('CADENA', token)
                else:
                    self.declararError('VS', token)
            else:
                self.declararError('CADENA', token)
        else:
            self.declararError('RESULTADO', token)

    def jornada(self):
        numero = ''
        nombrearchivo = 'jornada'
        token = self.listaTokens[self.i]
        if token.tipo == 'JORNADA':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'ENTERO':
                self.i += 1
                numero = token.lexema
                token = self.actualizarToken(self.i)
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    x = self.comyear(token)
                    if x[0] is True:
                        anio1 = x[1]
                        anio2 = x[2]
                        self.i += 1
                        token = self.actualizarToken(self.i)

                        nombrearchivo = self.flagF(token, nombrearchivo)
                        if anio1 != 0 and anio2 != 0 and numero != '':
                            temporada = anio1 + '-' + anio2
                            self.respuestaJORNADA(numero, temporada, nombrearchivo)
                    else:
                        return
                else:
                    self.declararError('VS', token)
            else:
                self.declararError('CADENA', token)
        else:
            self.declararError('RESULTADO', token)

    def goles(self):

        equipo1 = ''
        condicion = ''
        anio1 = ''
        anio2 = ''
        token = self.listaTokens[self.i]
        if token.tipo == 'GOLES':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'LOCAL' or token.tipo == 'VISITANTE' or token.tipo == 'TOTAL':
                condicion = token.lexema
                self.i += 1
                token = self.actualizarToken(self.i)
                if token.tipo == 'CADENA':
                    equipo1 = token.lexema
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    if token.tipo == 'TEMPORADA':
                        self.i += 1
                        token = self.actualizarToken(self.i)
                        x = self.comyear(token)
                        if x[0] is True:
                            anio1 = x[1]
                            anio2 = x[2]
                            if self.i < len(self.listaTokens) -1:
                                self.i += 1
                                token = self.actualizarToken(self.i)
                            if anio1 != 0 and anio2 != 0 and condicion != '' and equipo1 != '':
                                temporada = anio1 + '-' + anio2
                                self.respuestaGOLES(condicion, equipo1, temporada)
                            pass
                        else:
                            return
                    else:
                        self.declararError('TEMPORADA', token)
                else:
                    self.declararError('CADENA', token)
            else:
                self.declararError('CONDICION', token)
        else:
            self.declararError('GOLES', token)

    def flagJI(self, firstoken):
        nombrearchv = '1'
        if firstoken.tipo == '-ji':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'ENTERO':
                nombrearchv = token.lexema
                return nombrearchv
            else:
                self.declararError('ENTERO', token)
                return nombrearchv
        else:
            return nombrearchv

    def flagJF(self, firstoken):
        nombrearchv = '37'
        if firstoken.tipo == '-jf':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'ENTERO':
                nombrearchv = token.lexema
                return nombrearchv
            else:
                self.declararError('ENTERO', token)
                return nombrearchv
        else:
            return nombrearchv

    def tabla(self):
        anio1 = ''
        anio2 = ''
        nombrearchivo = 'temporada'
        token = self.listaTokens[self.i]
        if token.tipo == 'TABLA':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'TEMPORADA':
                self.i += 1
                token = self.actualizarToken(self.i)
                x = self.comyear(token)
                if x[0] is True:
                    anio1 = x[1]
                    anio2 = x[2]
                    if self.i < len(self.listaTokens) -1 :
                        self.i += 1
                        token = self.actualizarToken(self.i)
                    nombrearchivo = self.flagF(token, nombrearchivo)
                    if anio1 != 0 and anio2 != 0:
                        temporada = anio1 + '-' + anio2
                        self.respuestaTABLA(temporada, nombrearchivo)
                else:
                    return
            else:
                token = self.actualizarToken(self.i)
                self.declararError('TEMPORADA', token)
        else:
            token = self.actualizarToken(self.i)
            self.declararError('TABLA', token)

    def partidosins(self):
        jornadai = '1'
        jornadaf = '37'
        anio1 = ''
        anio2 = ''
        nombrearchivo = 'partidos'
        token = self.listaTokens[self.i]
        if token.tipo == 'PARTIDOS':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'CADENA':
                equipo1 = token.lexema
                self.i += 1
                token = self.actualizarToken(self.i)
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    x = self.comyear(token)
                    if x[0] is True:
                        anio1 = x[1]
                        anio2 = x[2]

                        if self.i < len(self.listaTokens) -1:
                            self.i += 1
                            token = self.actualizarToken(self.i)
                        else:
                            pass

                        while self.i < len(self.listaTokens) -1:
                            token = self.actualizarToken(self.i)
                            if token.tipo == '-f':
                                nombrearchivo = self.flagF(token, nombrearchivo)
                                self.i += 1

                            elif token.tipo == '-ji':
                                jornadai = self.flagJI(token)
                                self.i += 1
                            elif token.tipo == '-jf':
                                jornadaf = self.flagJF(token)
                                self.i += 1
                            else:
                                self.i += 1
                        self.i = len(self.listaTokens) - 1
                        if anio1 != '' and anio2 != '':
                            temporada = anio1 + '-' + anio2
                            self.respuestaPARTIDOS(temporada, equipo1, nombrearchivo, jornadai, jornadaf)
                        else:
                            self.declararError('TEMPORADA', token)
                    else:
                        return
                else:
                    self.declararError('TEMPORADA', token)
            else:
                self.declararError('CADENA', token)
        else:
            self.declararError('PARTIDOS', token)

    def top(self):
        condicion = ''
        numerotop = 5
        token = self.listaTokens[self.i]
        if token.tipo == 'TOP':
            self.i += 1
            token = self.actualizarToken(self.i)
            if token.tipo == 'SUPERIOR' or token.tipo == 'INFERIOR':
                condicion = token.lexema
                self.i += 1
                token = self.actualizarToken(self.i)
                if token.tipo == 'TEMPORADA':
                    self.i += 1
                    token = self.actualizarToken(self.i)
                    x = self.comyear(token)
                    if x[0] is True:
                        anio1 = x[1]
                        anio2 = x[2]
                        if self.i < len(self.listaTokens) -1:
                            self.i +=1
                            token = self.actualizarToken(self.i)
                        numerotop = self.flagN(token, numerotop)
                        if anio1 != 0 and anio2 != 0:
                            temporada = anio1 + '-' + anio2
                            self.respuestaTOP(condicion, numerotop,temporada)
                        pass
                    else:
                        return
                else:
                    self.declararError('TEMPORADA', token)
            else:
                self.declararError('CONDICION', token)
        else:
            self.declararError('GOLES', token)

    def analizar(self, listaTokens, listaErrores, listapartidos):
        self.i = 0
        self.instruccionencontrada = False
        self.resultadoFinal = ''
        self.partidos = listapartidos
        self.listaErrores = listaErrores
        self.listaTokens = listaTokens
        self.run()

    def respuestaRESULTADO(self, equipo1, equipo2, temporada):
        equipo1 = equipo1.replace("\"", '')
        equipo2 = equipo2.replace("\"", '')
        temporada = temporada
        for partido in self.partidos:
            if partido['local'] == equipo1 and partido['visitante'] == equipo2 and partido['temporada'] == temporada:
                resultado = 'El resultado de este partido fue: '
                resultado += f' {equipo1} {partido["goleslocal"]} - {equipo2} {partido["golesvisitante"]}'
                break
            else:
                resultado = 'No se encontro Resultado'
        self.resultadoFinal = resultado

    def JORNADAHTML(self, lista, nombrearch, jornada, temporada):
        archivo = open(f'{nombrearch}.html', 'w')
        abertura = f'''
                               <!DOCTYPE html>
                               <html lang="en">
                               <head>
                                 <title>{nombrearch}</title>
                                  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                                  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                               </head>
                               <body>
                              '''
        tabla = f'''    
                                <table class="table table-dark">
    
                                      <tr>
                                        <th>Equipo Local</th>
                                        <th>Equipo Visitante</th>
                                        <th>Resultado </th>
                                      </tr>
                                       {self.genTablas(lista, 'JORNADA')}
                                       
                                <h1> TABLA CORRESPONDIENTE A LA JORNADA NUMERO: {jornada} Y TEMPORADA {temporada}</h1>
                                '''

        final = '''
    
                                </body>
                                </html>
                        '''

        archivo.write(abertura + tabla + final)
        archivo.close()
        webbrowser.open(f"{nombrearch}.html")

    def genTablas(self, lista, tipo):
        contenidoListado = ''
        if tipo == 'JORNADA':
            for partido in lista:
                contenidoListado += f'''
                       <tr>
                           <td>{partido['equipo1']}</td>
                           <td>{partido['equipo2']}</td>
                           <td>{partido['resultado']}</td>
        
                       </tr>
                       '''
            return contenidoListado
        elif tipo == 'TABLA':
            for partido in lista:
                contenidoListado += f'''
                                  <tr>
                                      <td>{partido['equipo']}</td>               
                                      <td>{partido['punteo']}</td>
                                  </tr>
                                  '''
            return contenidoListado
        elif tipo == 'PARTIDOS':
            for partido in lista:
                contenidoListado += f'''
                                  <tr>
                                      <td>{partido['jornada']}</td>
                                       <td>{partido['ecnuentro']}</td>
                                       <td>{partido['resultado']}</td>
                                  </tr>
                                  '''
            return contenidoListado

    def respuestaJORNADA(self, numero, temporada, nombrearchivo):
        obj = []
        for partido in self.partidos:
            if partido['temporada'] == temporada and partido['jornada'] == numero:
                dato = {
                    'equipo1': partido['local'],
                    'equipo2': partido['visitante'],
                    'resultado': partido["goleslocal"] + "-" + partido["golesvisitante"],
                }
                obj.append(dato)
        self.resultadoFinal = f'Generando archivo de resultados jornada {numero} temporada {temporada}'
        self.JORNADAHTML(obj, nombrearchivo, numero, temporada)

    def respuestaGOLES(self, condicion, equipo, temporada):
        contadorGoles = 0
        equipo1 = equipo.replace('\"', '')
        for partido in self.partidos:
            if condicion == 'TOTAL':
                if (partido['local'] == equipo1 or partido['visitante'] == equipo1) and partido[
                    'temporada'] == temporada:
                    if partido['local'] == equipo1:
                        contadorGoles += int(partido['goleslocal'])
                    elif partido['visitante'] == equipo1:
                        contadorGoles += int(partido['golesvisitante'])
            elif condicion == 'LOCAL':
                if partido['local'] == equipo1 and partido['temporada'] == temporada:
                    contadorGoles += int(partido['goleslocal'])
            elif condicion == 'VISITANTE':
                if partido['visitante'] == equipo1 and partido['temporada'] == temporada:
                    contadorGoles += int(partido['golesvisitante'])
            else:
                contadorGoles += 0

        if condicion == 'LOCAL' or condicion == 'VISITANTE':
            self.resultadoFinal = f'Los goles anotados por el {equipo} de {condicion} en la temporada {temporada} fueron {str(contadorGoles)}'
        else:
            self.resultadoFinal = f'Los goles anotados por el {equipo} en TOTAL en la temporada {temporada} fueron {str(contadorGoles)}'

    def respuestaTABLA(self, temporada, nombrearchivo):
        partidoTempo = []
        equipos = []
        resultados = []
        for partido in self.partidos:
            if partido['temporada'] == temporada:
                if int(partido["goleslocal"]) > int(partido["golesvisitante"]):
                    resultado = 'GanaLocal'
                elif int(partido["goleslocal"]) == int(partido["golesvisitante"]):
                    resultado = 'Empate'
                elif int(partido["goleslocal"]) < int(partido["golesvisitante"]):
                    resultado = 'GanaVisita'
                dato = {
                    'equipo1': partido['local'],
                    'equipo2': partido['visitante'],
                    'resultado': resultado
                }
                partidoTempo.append(dato)
                equipos.append(partido['local'])
                equipos.append(partido['visitante'])

        convert_list_to_set = set(equipos)
        equipos = list(convert_list_to_set)

        contador = 0
        tablaPunteos = []
        while contador < len(equipos):
            punteo = 0
            equipoactual = equipos[contador]
            for resultado in partidoTempo:
                if equipoactual == resultado['equipo1'] and resultado['resultado'] == 'GanaLocal':
                    punteo += 3
                elif equipoactual == resultado['equipo2'] and resultado['resultado'] == 'GanaVisita':
                    punteo += 3
                elif (equipoactual == resultado['equipo2'] or equipoactual == resultado['equipo1']) and resultado[
                    'resultado'] == 'Empate':
                    punteo += 1
                else:
                    punteo += 0

            obj = {
                'equipo': equipos[contador],
                'punteo': int(punteo)
            }
            contador += 1
            tablaPunteos.append(obj)

        tablaPunteos = sorted(tablaPunteos, key=lambda i: i['punteo'], reverse=True)

        self.resultadoFinal = f'Generando archivo de clasificación de temporada {temporada}'
        self.TABLAHTML(tablaPunteos, temporada, nombrearchivo)

    def TABLAHTML(self, lista, temporada, nombrearchvio):
        archivo = open(f'{nombrearchvio}.html', 'w')
        abertura = f'''
                                      <!DOCTYPE html>
                                      <html lang="en">
                                      <head>
                                        <title>{nombrearchvio}</title>
                                         <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                                         <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                                      </head>
                                      <body>
                                     '''
        tabla = f'''    
                                       <table class="table table-dark">
    
                                             <tr>
                                               <th>Nombre del Equipo</th>
                                              
                                               <th>Punteo Total </th>
                                             </tr>
                                              {self.genTablas(lista, 'TABLA')}
    
                                       <h1> TABLA CORRESPONDIENTE A LA TEMPORADA {temporada}</h1>
                                       '''

        final = '''
    
                                       </body>
                                       </html>
                               '''

        archivo.write(abertura + tabla + final)
        archivo.close()
        webbrowser.open(f"{nombrearchvio}.html")
    def respuestaPARTIDOS(self, temporada, equipo1, nombrearchivo, jornadai, jornadaf):

        partidosportemporada = []
        listafinal = []
        x = int(jornadai)
        equipo1 = equipo1.replace("\"", '')
        for partido in self.partidos:
            if partido['temporada'] == temporada:
                if partido['local'] == equipo1 or partido['visitante'] == equipo1:
                    partido['jornada'] = int(partido['jornada'])
                    partidosportemporada.append(partido)

        partidosportemporada = sorted(partidosportemporada, key=lambda i: i['jornada'])

        while int(jornadai) <= x <= int(jornadaf):
            for juego in partidosportemporada:
                if juego['jornada'] == x:
                    obj = {
                        "jornada": juego['jornada'],
                        'ecnuentro': juego['local'] + ' vs ' + juego['visitante'],
                        'resultado': juego["goleslocal"] + "-" + juego["golesvisitante"],

                    }
                    listafinal.append(obj)
            x += 1

        self.PARTIDOSHTML(listafinal, temporada, equipo1, nombrearchivo, jornadai, jornadaf)

        self.resultadoFinal = 'Generarendo archivo'

    def PARTIDOSHTML(self, lista, temporada, equipo1, nombrearchivo, jornadai, jornadaf):
        archivo = open(f'{nombrearchivo}.html', 'w')
        abertura = f'''
                                              <!DOCTYPE html>
                                              <html lang="en">
                                              <head>
                                                <title>{nombrearchivo}</title>
                                                 <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                                                 <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                                              </head>
                                              <body>
                                             '''
        tabla = f'''    
                                               <table class="table table-dark">
    
                                                     <tr>
                                                       <th>Resultado</th>
    
                                                       <th>Encuentro </th>
                                                        <th>Resultado </th>
                                                     </tr>
                                                      {self.genTablas(lista, 'PARTIDOS')}
    
                                               <h1> TABLA CORRESPONDIENTE A LOS ENCUENTROS DE {equipo1} EN DESDE LA TEMPORADA {temporada} DESDE LA JORNADA {jornadai}, HASTA {jornadaf}</h1>
                                               '''

        final = '''
    
                                               </body>
                                               </html>
                                       '''

        archivo.write(abertura + tabla + final)
        archivo.close()
        webbrowser.open(f"{nombrearchivo}.html")

    def respuestaTOP(self, condicion, numerotop,temporada):
        partidoTempo = []
        equipos = []

        contenido = f'El top {condicion} de la temporada {temporada} fue \n'


        for partido in self.partidos:
            if partido['temporada'] == temporada:
                if int(partido["goleslocal"]) > int(partido["golesvisitante"]):
                    resultado = 'GanaLocal'
                elif int(partido["goleslocal"]) == int(partido["golesvisitante"]):
                    resultado = 'Empate'
                elif int(partido["goleslocal"]) < int(partido["golesvisitante"]):
                    resultado = 'GanaVisita'
                dato = {
                    'equipo1': partido['local'],
                    'equipo2': partido['visitante'],
                    'resultado': resultado
                }
                partidoTempo.append(dato)
                equipos.append(partido['local'])
                equipos.append(partido['visitante'])

        convert_list_to_set = set(equipos)
        equipos = list(convert_list_to_set)

        contador = 0
        tablaPunteos = []
        while contador < len(equipos):
            punteo = 0
            equipoactual = equipos[contador]
            for resultado in partidoTempo:
                if equipoactual == resultado['equipo1'] and resultado['resultado'] == 'GanaLocal':
                    punteo += 3
                elif equipoactual == resultado['equipo2'] and resultado['resultado'] == 'GanaVisita':
                    punteo += 3
                elif (equipoactual == resultado['equipo2'] or equipoactual == resultado['equipo1']) and resultado[
                    'resultado'] == 'Empate':
                    punteo += 1
                else:
                    punteo += 0

            obj = {
                'equipo': equipos[contador],
                'punteo': int(punteo)
            }
            contador += 1
            tablaPunteos.append(obj)

        tablaPunteos = sorted(tablaPunteos, key=lambda i: i['punteo'], reverse=True)

        if condicion == "SUPERIOR":
            index = 0
            while index <= (int)(numerotop)-1:
                nombre = tablaPunteos[index]['equipo']
                contenido += f'{index+1} {nombre} \n'
                index += 1

        else:
            index = len(tablaPunteos)-1
            indexdestino = len(tablaPunteos)-(int)(numerotop)
            while   indexdestino <= index:
                nombre = tablaPunteos[index]['equipo']
                contenido += f'{index+1} {nombre} \n'
                index -= 1

        self.resultadoFinal = contenido

    def respuestaADIOS(self):
        self.resultadoFinal = 'GRACIAS POR HACER USO DE LALIGA BOT!!!'
