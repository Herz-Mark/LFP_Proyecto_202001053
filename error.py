class Error:
    def __init__(self, descripción, linea, columna):
        self.descripcion = descripción
        self.linea = linea
        self.columna = columna

    def Imprimir(self):
        print(self.descripcion, self.linea, self.columna)

    def Enviar(self):
        return(self.descripcion, self.linea, self.columna)