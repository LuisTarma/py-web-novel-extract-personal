
# Hilo que exportara el texto a pdf
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
#from time
from subprocess import call
#from weasyprint import HTML, CSS
from time import sleep

from xhtml2pdf import pisa

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    def Enviar(self, titulos, archivos, defecto):
        self.defecto = defecto
        self.titulos = titulos
        self.archivos = archivos
    @pyqtSlot()
    def Exportar(self):
        i = 0
        for i in range(len(self.archivos)):
            #pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result,  default_css=open('default.css','r').read())
            archivo = self.archivos[i]
            titulo = self.titulos[i]
            print("En hilo " + titulo)
            texto = open(archivo).read()
            salida = " Procesando texto de " + titulo + "\n"
            self.intReady.emit(salida)
            titulo = "salida/" + titulo + ".pdf"
            #HTML(texto).write_pdf(titulo, stylesheets=[CSS(string='@page { size:letter; }')])
            pdf = open(titulo, "w+b")
            #if self.defecto:
            pdfStatus = pisa.CreatePDF(texto, dest=pdf, default_css=open('default.css', 'r').read())
            #else:
            #    pdfStatus = pisa.CreatePDF(texto, dest=pdf)
            pdf.close()
            #pisa.showLogging()
            salida = " -- Archivo exportado en " + titulo + "\n"
            self.intReady.emit(salida)
        self.finished.emit()

    def EnviarC(self,  comando, carpeta):
        self.comando = comando
        self.carpeta = carpeta

    def Convertir(self):
        comando = self.comando
        carpeta = self.carpeta
        try:
            call(comando)
            self.intReady.emit("Convirtiendo....")
            sleep(2)
            self.finished.emit()
            return
        except:
            print("Error en la ejecucion del comando " + comando)
            self.intReady.emit("Error en la conversion - Ejecutar Conversion Manualmente")
            self.finished.emit()
            return False