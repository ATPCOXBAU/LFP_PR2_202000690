from tkinter import *
from analizadorlexico import Analizadorexico
from analizadorsintactico import analizadorsintactico
from reportes import reportes
import webbrowser
BG_GRAY = "#EAEDDE"
BG_COLOR = "white"
TEXT_COLOR = "black"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"


class Interface:

    def __init__(self):
        self.listaErroresGlobal = []
        self.listaTokensGlobal = []
        self.root = Tk()
        self.root.geometry('1000x725')
        self.root.title('Proyecto 2')
        self.root.resizable(0, 0)
        self.Frame = Frame(self.root, width='1000', height='725')
        self.Frame.pack()
        self.Frame.config(bg='#F0F7D4')
        self.analizador = Analizadorexico()
        self.sintactico = analizadorsintactico()

        self.partidos = []
        self.reportes = reportes()

        self.text = Text(self.root, width=65, height=27, bg=BG_COLOR, fg=TEXT_COLOR,
                         font=FONT, padx=5, pady=5)

        self.text.place(x=0, y=0)
        self.text.configure(cursor="arrow", state=DISABLED)

        scrollbar = Scrollbar(self.text)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text.yview)

        bottom_label = Label(self.root, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        self.boxmsg = Entry(bottom_label, bg="#6198AE", fg=TEXT_COLOR, font=FONT)
        self.boxmsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.boxmsg.focus()
        self.boxmsg.bind("<Return>", self.enviarmensaje)
        buttnenviar = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20, bg=BG_GRAY,
                             command=lambda: self.enviarmensaje())
        buttnenviar.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

        btnReporte = Button(self.root, text="Reporte Errores", font=FONT_BOLD, width=20, bg="#007CAD",
                            command=lambda: self.genreporterror())
        btnReporte.place(x=750, y=10)

        btnlimlog = Button(self.root, text="Limpiar Log Errores", font=FONT_BOLD, width=20, bg="#007CAD",
                           command=lambda: self.limpiarLog('errores'))
        btnlimlog.place(x=750, y=60)

        btnretoken = Button(self.root, text="Reporte Tokens", font=FONT_BOLD, width=20, bg="#007CAD",
                            command=lambda: self.genreporttoken())
        btnretoken.place(x=750, y=110)

        btnlogtoken = Button(self.root, text="Limpiar Log de Tokens", font=FONT_BOLD, width=20, bg="#007CAD",
                             command=lambda: self.limpiarLog('tokens'))
        btnlogtoken.place(x=750, y=160)

        btnusuario = Button(self.root, text="Manual de Usuario", font=FONT_BOLD, width=20, bg="#007CAD",
                            command=lambda: self.genmanualUser())
        btnusuario.place(x=750, y=210)

        btnrtecnico = Button(self.root, text="Manual Tecnico", font=FONT_BOLD, width=20, bg="#007CAD",
                             command=lambda: self.fenmanualTec())
        btnrtecnico.place(x=750, y=260)
        self.InfoBot()
        self.root.mainloop()

    def agregarDatos(self, listaTokens, listaErrores):
        for token in listaTokens:
            self.listaTokensGlobal.append(token)
        for error in listaErrores:
            self.listaErroresGlobal.append(error)


    def agregarSINTACTICO(self, listaErrorSint):
        for error in listaErrorSint:
            self.listaErroresGlobal.append(error)

    def enviarmensaje(self):
        msg = self.boxmsg.get()
        self.mostrarmensaje(msg, "Tu")
        entrada = msg
        self.analizador.limpiar('errores')
        self.analizador.limpiar('tokens')

        self.analizador.analizar(entrada)
        self.agregarDatos(self.analizador.listaTokens, self.analizador.listaErrores)
        self.sintactico.analizar(self.analizador.listaTokens, self.analizador.listaErrores, self.partidos)
        self.agregarSINTACTICO(self.sintactico.listaErrores)
        if self.sintactico.resultadoFinal != '' and self.sintactico.instruccionencontrada is True:
            self.mostrarmensaje(self.sintactico.resultadoFinal,"LaLigaBOT")
            if self.sintactico.resultadoFinal == 'GRACIAS POR HACER USO DE LALIGA BOT!!!':
                self.root.destroy()

        else:
            self.mostrarmensaje('No se ha podido Leer un Comando Valido',"LaLigaBOT")



    def limpiarLog(self, tipo):
        if tipo == 'errores':
            self.listaErroresGlobal = []
        else:
            self.listaTokensGlobal = []


    def genreporttoken(self):
        listado = self.listaTokensGlobal
        self.reportes.reporteTokens(listado, 'Reporte de Tokens')

    def genreporterror(self):
        listado = self.listaErroresGlobal
        self.reportes.reporteTokens(listado, 'Reporte de Erroes')



    def InfoBot(self):
        file = open('LaLigaBot-LFP.csv', encoding="utf8")
        contenido = file.read()
        plays = contenido.split("\n")
        jsonpartidos = []
        for partido in plays:
            datos = partido.split(',')
            play = {
                'fecha': datos[0],
                'temporada': datos[1],
                'jornada': datos[2],
                'local': datos[3],
                'visitante': datos[4],
                'goleslocal': datos[5],
                'golesvisitante': datos[6],
            }
            jsonpartidos.append(play)
        self.partidos = jsonpartidos

    def mostrarmensaje(self, msg, sender):
        if not msg:
            return
        self.boxmsg.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text.configure(state=NORMAL)
        self.text.insert(END, msg1)
        self.text.configure(state=DISABLED)
        self.text.see(END)

    def genmanualUser(self):
        webbrowser.get('windows-default').open('Musuario.pdf')

    def fenmanualTec(self):
        webbrowser.get('windows-default').open('Mtecnico.pdf')

