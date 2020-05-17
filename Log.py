
# Hilo que exportara el texto a pdf
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
#import time



class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    def Enviar(self, texto, titulo, num_tarea, num_total_tareas):
        self.texto = texto 
        self.titulo = titulo
        self.num_tarea = num_tarea
        self.num_total_tareas = num_total_tareas

    @pyqtSlot()
    def Exportar(self):
        print("En hilo " + self.titulo)
        texto = self.texto
        titulo = self.titulo
        salida = " Procesando texto de " + titulo + "\n" + " Tarea (%s/%s)" % (self.num_tarea, self.num_total_tareas) + "\n"
        self.intReady.emit(salida)
        salida = " -- Archivo exportado en " + titulo + "\n"
        self.intReady.emit(salida)
        self.finished.emit()