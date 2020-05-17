# coding: utf-8

from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from UI import *
from os.path import isfile, isdir
from os import scandir, getcwd
from subprocess import call
from PyQt5.QtCore import QThread

#from reportlab.lib.pagesizes import A4
#from reportlab.pdfgen import canvas
import RecuperarTitulo
import Exportar_pdf as expo
from xhtml2pdf import pisa

class Principal(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self, *args, **kwargs):
		QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
		self.setupUi(self)
		self.b_carpeta.clicked.connect(self.Seleccionar)
		self.b_iniciar.clicked.connect(self.Formatear)
		self.btn_css.clicked.connect(self.Abrir_Css)
		self.btn_convertir.clicked.connect(self.Convertir)
		self.salida = ""
		self.interruptor = 0
		self.cantidad = 0
		self.contador_progreso = 0
		# Directorio Actual
		self.cwd = getcwd()
		print("Directorio de trabajo: " + self.cwd)

	def Abrir_Css(self):
		comando = "notepad.exe " + self.cwd + "\default.css"
		call(comando)
	def HiloTerminado(self):
		self.salida += "Terminado con exito!!"
		self.t_salida.setPlainText(self.salida)
		self.progreso.setProperty("value", 100)
		self.thread.quit
	def onIntReady(self, i):
		self.contador_progreso += self.cantidad
		self.t_progreso.setText(str(self.contador_progreso))
		self.salida += i
		self.t_salida.setPlainText(self.salida)
		#self.progreso.value(self.contador_progreso)
		self.progreso.setProperty("value", self.contador_progreso)
		#self.interruptor = 1
	def listaArchivos(self, path):
		return [obj.name for obj in scandir(path) if obj.is_file()]
	def Seleccionar(self):
		self.folder = str(QFileDialog.getExistingDirectory(self, "Seleccionar Directorio"))
		self.carpeta.setText(self.folder)
		self.btn_convertir.setEnabled(True)
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
		#os.system()
		#os.popen()
		comando = "FileEncodingConverter/FileEncodingConverter.exe \"" + self.folder + "\" ANSI *.html && exit"
		self.obj = expo.Worker()  # Sin padre!
		self.thread = QThread()  # Sin padre!
		self.obj.intReady.connect(self.Convirtiendo)
		self.obj.moveToThread(self.thread)
		self.obj.finished.connect(self.FinConversion)
		self.thread.started.connect(self.obj.Convertir)	
		#self.cantidad = (((100 / len(archivos_txt))*100)/100)/2
		#print("Progreso Total " + str(self.cantidad))
		self.obj.EnviarC(comando, self.folder)
		#num_tarea += 1Z
		self.thread.start()
	def Convirtiendo(self, i):
		self.t_salida.setPlainText(str(i))
	def FinConversion(self):
		pass
	def QuitarEspacio(self, titulo):
		print("Quitando espacios de " + titulo)
		t = ""
		empezar = 0
		for caracter in titulo.rstrip():
			#print(caracter)
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
	def ExportarPDF(self, texto, titulo):
		# Sin usar
		"""
		Metodo 1
		Por defecto esta en tamaño A4 (595.2 de ancho y 841.8 de alto)
		
		print("Creando pdf de " + titulo )
		# Tamaño A4 en width y height
		w, h = A4
		titulo = titulo + ".pdf"
		pdf = canvas.Canvas(titulo)
		# Extremo superior izquierdo con margen
		txt = pdf.beginText(10, h-50)
		txt.setFont("Times-Roman", 12)
		txt.textLines(texto)
		#pdf.drawString(50,h - 50,texto)
		#pdf.showPage()
		pdf.drawText(txt)
		pdf.save()
		"""
		"""
		Metodo 2
		Usando xhtml2pdf Funciona 100 x 100
		"""
		#self.Log(" --- Exportando archivo a pdf " + titulo)
		titulo = "salida/" + titulo + ".pdf"
		pdf = open(titulo, "w+b")
		pdfStatus = pisa.CreatePDF(texto, dest=pdf)
		pdf.close()
		#pisa.showLogging()
		#self.Log(" --- Archivo pdf guardado como " + titulo + ".pdf")
		return pdfStatus.err
	def Log(self, texto):
		self.logView.append('%s' % texto) #append string
   		#QtGui.QApplication.processEvents() #update gui for pyqt
		QtWidgets.QApplication.processEvents()
		#self.t_salida.setPlainText(texto)
		#print(texto)
		return 
	def Formatear(self):
		self.interruptor = 0
		verde = "<span style=\" font-size:8pt; font-weight:600; color:#00ff00;\" >"
		if self.salida == "":
			self.salida = "Iniciando... \n"
		self.t_salida.setPlainText(self.salida)

		#para_titulo = ["<","h","1"," ","c","l","a","s","s","="]
		if self.texto_titulo.text() == "":
			return
		else:
			para_tituloT = self.texto_titulo.text()

		try:
			# Todos los archivos a procesar
			archivos = self.listaTodos
		except:
			#self.Log("Selecciona primero una carpeta we ;)")
			return

		# Todo hasta a debe ser borrado  // Ex: </div><!-- .header-wrapper -->
		a = self.principio.text()
		# Todo desde b debe ser borrado  // Ex: </article><!-- #post-## -->
		b = self.fin.text()

		if a=="" and b=="":
			#self.Log("Nada que procesar en los archivos... :(")
			return
		# Procesamiento de a
		archivos_txt = []
		titulos_txt = []
		for archivo in archivos:
			file = open(archivo)
			inicio = ""
			sw = 0
			for linea in file:
				limpio = linea.rstrip()
				if limpio == str(b):
					break
				if sw == 1:
					inicio += limpio + "\n"
				if limpio == str(a):
					sw = 1
				# Recuperar Titulo del cap
				empezar = 0
				#titulo = ""
				titulo = RecuperarTitulo(linea[:10], para_tituloT)
				if titulo != "":
					self.titulo = titulo
			
			#self.salida += "Procesando archivo '" + str(archivo) + "\n"
			#self.Log(self.salida)

			titulo_limpio = self.QuitarEspacio(self.titulo)
			#print(titulo_limpio)

			self.salida += "---- Titulo recuperado: " + str(titulo_limpio)  +  "\n"
			print("Procesado " + titulo_limpio)
			#self.Log("Procesado " + titulo_limpio)
			self.t_salida.setPlainText("Procesado " + titulo_limpio)

			fin = verde + "Finalizado con exito"
			fin += "</span>"
			self.t_salida.append(fin)

			out_file = open(str("salida/" + titulo_limpio + ".txt"), "w")
			out_file.write(inicio)
			out_file.close()
			archivos_txt.append(str("salida/" + titulo_limpio + ".txt"))
			titulos_txt.append(titulo_limpio)
			file.close()
			#self.ExportarPDF(inicio, titulo_limpio)
			#a = 0
			#while self.interruptor == 0:
			#	print(a)
			#	a+=1

		# Funcionando
		forced = True
		if forced == True:
			self.obj = expo.Worker()  # Sin padre!
			self.thread = QThread()  # Sin padre!
			self.obj.intReady.connect(self.onIntReady)
			self.obj.moveToThread(self.thread)
			self.obj.finished.connect(self.HiloTerminado)
			self.thread.started.connect(self.obj.Exportar)	
			self.cantidad = (((100 / len(archivos_txt))*100)/100)/2
			print("Progreso Total " + str(self.cantidad))
			defecto = True
			if forced == True:
				defecto = True
			self.obj.Enviar(titulos_txt, archivos_txt, defecto)
			#num_tarea += 1Z
			self.thread.start()

		#self.t_salida.setPlainText(inicio)

if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	window = Principal()
	window.show()
	app.exec_()
