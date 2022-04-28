import webbrowser


class reportes:
    def __init__(self):
        return

    def reporteTokens(self,listadeTokens,tipo):
        archivo = open(f'{tipo}.html', 'w')
        abertura = f'''
                   <!DOCTYPE html>
                   <html lang="en">
                   <head>
                     <title>Reporte LFP</title>
                     <meta charset="utf-8">
                     <meta name="viewport" content="width=device-width, initial-scale=1">
                     <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                     <style>
                     .fakeimg {{
                       height: 200px;
                       background: #aaa;
                     }}
                     </style>
                   </head>
                   <body>

                   <div class="p-5 bg-{self.color(tipo)} text-white text-center">
                     <h1>  {tipo} </h1>
                     <p>Carlos Javier Cox Bautista 202000690</p> 
                   </div>

                   <nav class="navbar navbar-expand-sm bg-dark navbar-dark">

                   </nav>
                  '''
        tabla = f'''
                <div class="container mt-5">
                    <table class="table table-hover">
                        <tr><th>TIPO TOKEN</th><th>LEXEMA</th><th>COLUMNA</th></tr>
                        {self.tablas(listadeTokens,tipo)}
                        </table>
                        </div>

                    '''

        final = '''

                    <br>
                    <div class="mt-5 p-4 bg-dark text-white text-center">
                      <p>Carlos Cox Bautista 202000690 LFP</p>
                    </div>

                    </body>
                    </html>
            '''

        archivo.write(abertura + tabla + final)
        archivo.close()
        webbrowser.open(f"{tipo}.html")

    def color(self,tipo):
        if tipo == 'Reporte de Tokens':
            colorr = 'success'
        else:
            colorr = 'danger'
        return colorr

    def tablas(self,listadetokens,tipo):
        contenidoListado = ''
        if tipo == 'Reporte de Tokens':
            for token in listadetokens:
                contenidoListado += f'''
                   <tr>
                       <td>{token.tipo}</td>
                       <td>{token.lexema}</td>
                       <td>{token.columna}</td>

                   </tr>
                   '''
        elif tipo == 'Reporte de Erroes':
            for token in listadetokens:
                contenidoListado += f'''
                    <tr>
                       <td>{token.tipo}</td>
                       <td>{token.lexema}</td>
                       <td>{token.columna}</td>
                   </tr>
                   '''

        return contenidoListado
