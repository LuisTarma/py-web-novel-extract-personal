# main.py
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QTextEdit, QPushButton
import sys
import prueba_funcion_hilo as worker
import time

class Form(QWidget):

	def __init__(self):
		super().__init__()
		#self.label = QLabel("0")
		self.tEdit = QTextEdit("0")
		self.btn = QPushButton("Iniciar")

		 # 1 - create Worker and Thread inside the Form
		self.obj = worker.Worker()  # no parent!
		
		self.thread = QThread()  # no parent!

		 # 2 - Connect Worker`s Signals to Form method slots to post data.
		self.obj.intReady.connect(self.onIntReady)

		 # 3 - Move the Worker object to the Thread object
		self.obj.moveToThread(self.thread)

		 # 4 - Connect Worker Signals to the Thread slots
		self.obj.finished.connect(self.TareaTerminada)

		 # 5 - Connect Thread started signal to Worker operational slot method
		self.thread.started.connect(self.obj.procCounter)
		self.btn.clicked.connect(self.iniciar)
		 # * - Thread finished signal will close the app if you want!
		# app.exit
		self.thread.finished.connect(self.TareaTerminadaQ)

		 # 6 - Start the thread
		#self.thread.start()
		# 7 - Start the form
		self.terminado = 0
		self.salida = ""
		self.initUI()

	def TareaTerminadaQ(self):
		print("Tarea Terminada QT")
		#self.terminado = 1
	def TareaTerminada(self):
		self.tEdit.append("Tarea terminada")
		#self.terminado = 1
		#print("Variable self.terminado = %s" % self.terminado)
		self.thread.quit

	def iniciar(self):
		self.terminado = 0
		lista = ["Luis", "Ana", "Marco", "Perro"]
		#print("Enviado %s" % i)
		self.obj.Enviar(lista)
		self.thread.start()
		#self.terminado = 0
		#a = 0
			#time.sleep(2)
			#while self.terminado == 0:
			#	print(a)
			#	time.sleep(1)
			#	a+=1
		#print(self.salida)

	def onIntReady(self, i):
			#self.label.setText("{}".format(i))
			self.tEdit.append(i)
			#self.salida += i
			#print(i)

	def initUI(self):
			grid = QGridLayout()
			self.setLayout(grid)
			#grid.addWidget(self.label,0,0)
			grid.addWidget(self.tEdit,0,0)
			grid.addWidget(self.btn, 1,1)

			self.move(300, 150)
			self.setWindowTitle('thread test')
			self.show()



app = QApplication(sys.argv)

form = Form()

sys.exit(app.exec_())