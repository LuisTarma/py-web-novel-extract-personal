# coding: utf-8

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from UI import *
from os.path import isfile, isdir
from os import scandir

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.b_carpeta.clicked.connect(self.Seleccionar)
		self.b_iniciar.clicked.connect(self.Formatear)
		self.salida = ""

	def listaArchivos(self, path):
		return [obj.name for obj in scandir(path) if obj.is_file()]

	def Seleccionar(self):
		self.folder = str(QFileDialog.getExistingDirectory(self, "Seleccionar Directorio"))
		self.carpeta.setText(self.folder)

		lista = self.listaArchivos(self.folder)
		self.listaTodos = []
		for item in lista:
			t = ""
			t = self.folder + "/" + item
			self.listaTodos.append(t)

		# Cantidad de achivos
		self.seleccionados.setText(str(len(lista)))
		self.fondo_1.setStyleSheet("background-color: rgb(61, 203, 153);")

	def Convertir(self):
		pass
	def QuitarEspacio(self, titulo):
		print("Quitando espacios de " + titulo)
		t = ""
		empezar = 0
		for caracter in titulo.rstrip():
			print(caracter)
			if caracter == "í":
				t += "i"
				continue
			if caracter == "–":
				continue
			if caracter == "&":
				empezar = 1
			if empezar == 0:
				t += caracter
			if caracter == ";":
				t += "_"
				empezar = 0
		return t
	

	def Formatear(self):
		verde = "<span style=\" font-size:8pt; font-weight:600; color:#0000FF;\" >"
		if self.salida == "":
			self.salida = "Iniciando... \n"
		self.t_salida.setPlainText(self.salida)

		para_titulo = ["<","h","1"," ","c","l","a","s","s","="]
		para_tituloT = "<h1 class="

		if self.check_convertir.isChecked():
			self.Convertir()

		try:
			# Todos los archivos a procesar
			archivos = self.listaTodos
		except:
			self.t_salida.setPlainText("Selecciona primero una carpeta we ;)")
			return

		# Todo hasta a debe ser borrado  // Ex: </div><!-- .header-wrapper -->
		a = self.principio.text()
		# Todo desde b debe ser borrado
		b = self.fin.text()

		if a=="" and b=="":
			self.t_salida.setPlainText("Nada que procesar en los archivos... :(")
			return
		# Procesamiento de a
		for archivo in archivos:
			file = open(archivo)
			inicio = ""
			sw = 0
			for linea in file:
				limpio = linea.rstrip()
				if sw == 1:
					inicio += limpio + "\n"
				if limpio == str(a):
					sw = 1

				# Recuperar Titulo del cap
				empezar = 0
				titulo = ""
				if linea[:10] == para_tituloT:
					print(linea)
					for caracter in linea:
						if caracter==">":
							empezar=1
							continue
						if caracter=="<":
							empezar=0
						if empezar==1:
							titulo+=caracter
				if titulo != "":
					self.titulo = titulo
					print(titulo)
			self.salida += "Procesando archivo '" + str(archivo) + "\n"
			self.t_salida.setPlainText(self.salida)

			titulo_limpio = self.QuitarEspacio(self.titulo)
			print(titulo_limpio)

			self.salida += verde + "---- Titulo recuperado: " + str(titulo_limpio)  + "</span>" + "\n"
			self.salida += verde + "---- Guardado en: " + str(titulo_limpio) + ".txt"  + "</span>" + "\n"
			
			self.t_salida.setPlainText(QtCore.QString(self.salida))
			

			fin = verde + "Finalizado con exito"
			fin += "</span>"
			self.t_salida.append(fin)

			out_file = open(str(titulo_limpio+".txt"), "w")
			out_file.write(inicio)
			out_file.close()
			file.close()

		# Procesamiento de b
		# ....

		#self.t_salida.setPlainText(inicio)







if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = MainWindow()
	window.show()
	app.exec_()
