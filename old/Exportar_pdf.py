
# Hilo que exportara el texto a pdf
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time

from xhtml2pdf import pisa

class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    def Enviar(self, titulos, archivos):
        self.titulos = titulos
        self.archivos = archivos
    @pyqtSlot()
    def Exportar(self):
        i = 0
        for i in range(len(self.archivos)):
            archivo = self.archivos[i]
            titulo = self.titulos[i]
            print("En hilo " + titulo)
            texto = open(archivo).read()
            salida = " Procesando texto de " + titulo + "\n"
            self.intReady.emit(salida)
            titulo = "salida/" + titulo + ".pdf"
            pdf = open(titulo, "w+b")
            pdfStatus = pisa.CreatePDF(texto, dest=pdf)
            pdf.close()
            #pisa.showLogging()
            salida = " -- Archivo exportado en " + titulo + "\n"
            self.intReady.emit(salida)
        self.finished.emit()