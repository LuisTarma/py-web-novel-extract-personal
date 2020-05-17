
def RecuperarTitulo(linea, para_tituloT):
    titulo = ""
    if linea[:10] == para_tituloT:
        #print(linea)
        for caracter in linea:
            if caracter==">":
                empezar=1
                continue
            if caracter=="<":
                empezar=0
            if empezar==1:
                titulo+=caracter
    return titulo
        