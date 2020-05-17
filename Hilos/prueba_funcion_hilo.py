# worker.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


class Worker(QObject):
    finished = pyqtSignal()
    intReady = pyqtSignal(str)

    def Enviar(self, texto):
    	self.texto = texto
    @pyqtSlot()
    def procCounter(self): # A slot takes no params
        l = self.texto
        for i in l:
            #time.sleep(1)
            self.intReady.emit(i)

        self.finished.emit()

    @pyqtSlot()
    def Log(self):
    	v = ["Procesando", "Hecho", "Chau"]
    	for i in v:
    		time.sleep(1)
    		self.intReady.emit(i)

    	self.finished.emit()