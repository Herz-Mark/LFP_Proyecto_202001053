class Token:
    def __init__(self, lexema, tipo, linea, columna):
        self.lexema = lexema
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def imprimir(self):
        print(self.lexema, self.tipo, self.linea, self.columna)
    
    def Enviar(self):
        return(self.lexema, self.tipo, self.linea, self.columna)
