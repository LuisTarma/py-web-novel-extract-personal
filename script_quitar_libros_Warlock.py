# -*- coding: utf-8 -*-

def quitarNovelas():
	archivo = open("lista.txt")
	caps = []

	for linea in archivo:
		limpio = linea.rstrip()
		sw = 0
		url = ""
		for letra in limpio:
			if letra == "\"":
				sw += 1
				continue
			if sw == 1:
				url += letra
			if sw == 2:
				caps.append(url)
				sw = 0
	archivo.close()
	return caps

caps = quitarNovelas()
for i in caps:
	print(i)
	

def listar(lista):
	archivo = open("salida.txt", "wr")
	for url in lista:
		pass
		
