from prettytable import PrettyTable
from reportes import Reporte_Lista
from graphviz import Digraph
import uuid
instrucciones = ['imprimir', 'imprimirln', 'conteo', 'promedio', 'contarsi','datos', 'sumar', 'max', 'min', 'exportarReporte', 'Claves', 'Registros']

class AnalizadorSintactico:

    def __init__(self, tokens=[]):
        self.errores = []
        self.g = Digraph('Ejemplo', filename='png')
        self.tokens = tokens
        self.tokens.reverse()
        self.actions = []
        self.claves = []
        self.aux = []
        self.registers = []
        self.conteo = 0
        self.text = ""
        self.valor = ""
        self.tabla = {}

    def agregaError(self, obtenido, esperado, fila, columna):
        self.errores.append("<ERROR SINTÁCTICO> Se obtuvo {}, se esperaba {}. Fila: {}, Columna: {}".format(
            obtenido, esperado, fila, columna))

        tmp = self.tokens.pop()
        while tmp.tipo != "punto y coma":
            tmp = self.tokens.pop()
    
    def crearNodo(self, etiqueta: str) -> str:
        id = str(uuid.uuid1())
        self.g.node(id,etiqueta)
        return id

    def agregarHijo(self,id_padre,id_hijo :str):
        self.g.edge(id_padre,id_hijo)


    def impErrores(self):
        x = PrettyTable()
        x.field_names = ["Errores"]
        if len(self.errores) == 0:
            print('No hay errores')
        else:
            for i in self.errores:
                x.add_row([i])
            print(x)

    def analizar(self):
        self.INICIO()
        self.impErrores()

    def INICIO(self):
        self.INSTRUCCIONES()

    def INSTRUCCIONES(self):
        self.INSTRUCCION()
        self.INSTRUCCIONES2()

    def INSTRUCCION(self):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo == 'imprimir':
                self.INSTRUCCION_IMPRIMIR()
            elif tmp.tipo == 'imprimirln':
                self.INSTRUCCION_IMPRIMIRLN()
            elif tmp.tipo == 'conteo':
                self.INSTRUCCION_CONTEO()
            elif tmp.tipo == 'promedio':
                self.INSTRUCCION_PROMEDIO()
            elif tmp.tipo == 'contarsi':
                self.INSTRUCCION_CONTARSI()
            elif tmp.tipo == 'datos':
                self.INSTRUCCION_DATOS()
            elif tmp.tipo == 'sumar':
                self.INSTRUCCION_SUMAR()
            elif tmp.tipo == 'max':
                self.INSTRUCCION_MAX()
            elif tmp.tipo == 'min':
                self.INSTRUCCION_MIN()
            elif tmp.tipo == 'exportarReporte':
                self.INSTRUCCION_EXPORTAR()
            elif tmp.tipo == 'Claves':
                self.INSTRUCCION_CLAVES()
            elif tmp.tipo == 'Registros':
                self.INSTRUCCION_REGISTROS()

            """elif tmp.tipo == 'palabra':
                self.INSTRUCCION_ASIGNACION()"""
        except:
            pass

    def INSTRUCCIONES2(self):
        try:
            tmp = self.tokens[-1]
            if tmp.tipo in instrucciones:
                self.INSTRUCCION()
                self.INSTRUCCIONES2()
            else:
                pass
        except:
            pass

    # FUNCIONES DE IMPRIMIR CON SUS RESPECTIVAS CADENAS

    def INSTRUCCION_IMPRIMIR(self):
        tmp = self.tokens.pop()
        if tmp.tipo == "imprimir":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo('palabra')
                    self.agregarHijo(n5,n6)
                    self.text += tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('punto_y_coma')
                            n10 = self.crearNodo('palabra')
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo("INSTRUCCION IMPRIMIR")
                            self.agregarHijo(n11,n1)
                            self.agregarHijo(n11,n3)
                            self.agregarHijo(n11,n5)
                            self.agregarHijo(n11,n7)
                            self.agregarHijo(n11, n9)
                        else:
                            self.agregaError(
                                tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')',
                                         tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string',
                                     tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "imprimir", tmp.linea, tmp.columna)

    def INSTRUCCION_IMPRIMIRLN(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "imprimirln":
            n12 = self.crearNodo('instruccion')
            n13 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n12,n13)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n14 = self.crearNodo('parentesis')
                n15 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n14,n15)
                tmp = self.tokens.pop()
                
                if tmp.tipo == "string":
                    n16 = self.crearNodo('string')
                    n17 = self.crearNodo('palabra')
                    self.agregarHijo(n16,n17)
                    self.actions.append(tmp.lexema) 
                    tmp = self.tokens.pop()

                    if tmp.tipo == "parentesis final":
                        n18 = self.crearNodo('parentesis')
                        n19 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n18,n19)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n20 = self.crearNodo('punto_y_coma')
                            n21 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n20,n21)
                            n22 = self.crearNodo("INSTRUCCION IMPRIMIRLN")
                            self.agregarHijo(n22, n12)
                            self.agregarHijo(n22, n14)
                            self.agregarHijo(n22, n16)
                            self.agregarHijo(n22, n18)
                            self.agregarHijo(n22, n20)
                        else:
                            self.agregaError(
                                tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')',
                                         tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string',
                                     tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "imprimirln", tmp.linea, tmp.columna)

    # INSTRUCCION PARA REALIZAR EL CONTEO

    def INSTRUCCION_CONTEO(self):
        
        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "conteo":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "parentesis final":
                    n5 = self.crearNodo('parentesis')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    tmp = self.tokens.pop()
                    if tmp.tipo == "punto y coma":
                        n7 = self.crearNodo('punto_y_coma')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        n9 = self.crearNodo("INSTRUCCION CONTEO")
                        self.agregarHijo(n9, n1)
                        self.agregarHijo(n9, n3)
                        self.agregarHijo(n9, n5)
                        self.agregarHijo(n9, n7)
                        self.actions.append(">>>" + str(self.conteo))
                    else:
                        self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, '(', tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, 'conteo', tmp.linea, tmp.columna)

    # INSTRUCCION PARA REALIZAR EL PROMEDIO

    def INSTRUCCION_PROMEDIO(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        index = 0
        promedio = 0
        suma = 0
        lineas = 0
        tmp = self.tokens.pop()
        if tmp.tipo == "promedio":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('parentesis')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo('INSTRUCCION PROMEDIO')
                            self.agregarHijo(n11, n1)
                            self.agregarHijo(n11, n3)
                            self.agregarHijo(n11, n5)
                            self.agregarHijo(n11, n7)
                            self.agregarHijo(n11, n9)
                            index = self.claves.index(self.text)
                            for i in range(0, len(self.registers)):
                                suma += float(self.registers[i][index])
                                lineas += 1
                            promedio = suma / lineas
                            self.actions.append(">>>"+str(promedio))
                            self.text = ""
                        else:
                            self.agregaError(
                                        tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')',
                                                 tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "promedio", tmp.linea, tmp.columna)

    # INSTRUCCION CONTAR SI

    def INSTRUCCION_CONTARSI(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        index = 0
        counter = 0
        tmp = self.tokens.pop()
        if tmp.tipo == "contarsi":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "coma":
                        n7 = self.crearNodo('coma')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "entero":
                            n9 = self.crearNodo('entero')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            self.valor = tmp.lexema
                            tmp = self.tokens.pop()
                            if tmp.tipo == "parentesis final":
                                n11 = self.crearNodo('parentesis')
                                n12 = self.crearNodo(tmp.lexema)
                                self.agregarHijo(n11,n12)
                                tmp = self.tokens.pop()
                                if tmp.tipo == "punto y coma":
                                    n13 = self.crearNodo('punto_y_coma')
                                    n14 = self.crearNodo(tmp.lexema)
                                    self.agregarHijo(n13,n14)
                                    n15 = self.crearNodo('INSTRUCCION_CONTARSI')
                                    self.agregarHijo(n15, n1)
                                    self.agregarHijo(n15, n3)
                                    self.agregarHijo(n15, n5)
                                    self.agregarHijo(n15, n7)
                                    self.agregarHijo(n15, n9)
                                    self.agregarHijo(n15, n11)
                                    self.agregarHijo(n15, n13)
                                    index = self.claves.index(self.text)
                                    for i in range(0, len(self.registers)):
                                        if self.registers[i][index] == self.valor:
                                            counter += 1
                                    self.actions.append(">>>" + str(counter))
                                    self.text = ""
                                    self.valor = ""
                                else:
                                    self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                            else:
                                self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
                        else:
                            self.agregaError(tmp.tipo, 'entero', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, 'coma', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "contarsi", tmp.linea, tmp.columna)

    # INSTRUCCION PARA MOSTRAR TABLA CON DATOS

    def INSTRUCCION_DATOS(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "datos":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "parentesis final":
                    n5 = self.crearNodo('parentesis')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    tmp = self.tokens.pop()
                    if tmp.tipo == "punto y coma":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        n9 = self.crearNodo('INSTRUCCION_DATOS')
                        self.agregarHijo(n9,n1)
                        self.agregarHijo(n9,n3)
                        self.agregarHijo(n9,n5)
                        self.agregarHijo(n9,n7)
                        self.imprimir_datos()
                    else:
                        self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, '(', tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, 'datos', tmp.linea, tmp.columna)

    # INSTRUCCION PARA SUMAR REGISTRO

    def INSTRUCCION_SUMAR(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        index = 0
        suma = 0
        tmp = self.tokens.pop()
        if tmp.tipo == "sumar":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('parentesis')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo("INSTRUCCION_SUMAR")
                            self.agregarHijo(n11,n1)
                            self.agregarHijo(n11,n3)
                            self.agregarHijo(n11,n5)
                            self.agregarHijo(n11,n7)
                            self.agregarHijo(n11,n9)
                            index = self.claves.index(self.text)
                            for i in range(0, len(self.registers)):
                                suma += float(self.registers[i][index])
                            self.actions.append(">>>" + str(suma))
                            self.text = ""
                        else:
                            self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "promedio", tmp.linea, tmp.columna)

    # INSTRUCCION PARA ENCONTRAR EL VALOR MAXIMO EN UN REGISTRO

    def INSTRUCCION_MAX(self):
        
        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        index = 0
        maximos = []
        maximo = 0
        tmp = self.tokens.pop()
        if tmp.tipo == "max":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('punto_y_coma')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo("INSTRUCCION_MAX")
                            self.agregarHijo(n11,n1)
                            self.agregarHijo(n11,n3)
                            self.agregarHijo(n11,n5)
                            self.agregarHijo(n11,n7)
                            self.agregarHijo(n11,n9)
                            index = self.claves.index(self.text)
                            for i in range(0, len(self.registers)):
                                maximos.append(float(self.registers[i][index]))
                            maximo = max(maximos)
                            self.actions.append(">>>" + str(maximo))
                            self.text = ""
                        else:
                            self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "max", tmp.linea, tmp.columna)

    # INSTRUCCION PARA ENCONTRAR EL VALOR MINIMO EN UN REGISTRO

    def INSTRUCCION_MIN(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        index = 0
        minimos = []
        minimo = 0
        tmp = self.tokens.pop()
        if tmp.tipo == "min":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('parentesis')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('string')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo('INSTRUCCION_MIN')
                            self.agregarHijo(n11,n1)
                            self.agregarHijo(n11,n3)
                            self.agregarHijo(n11,n5)
                            self.agregarHijo(n11,n7)
                            self.agregarHijo(n11,n9)
                            index = self.claves.index(self.text)
                            for i in range(0, len(self.registers)):
                                minimos.append(float(self.registers[i][index]))
                            minimo = min(minimos)
                            self.actions.append(">>>" + str(minimo))
                            self.text = ""
                        else:
                            self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "min", tmp.linea, tmp.columna)

    # INSTRUCCION PARA EXPORTAR REPORTES

    def INSTRUCCION_EXPORTAR(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "exportarReporte":
            n1 = self.crearNodo('instruccion')
            n2 = self.crearNodo(tmp.lexema)
            self.agregarHijo(n1,n2)
            tmp = self.tokens.pop()
            if tmp.tipo == "parentesis inicio":
                n3 = self.crearNodo('parentesis')
                n4 = self.crearNodo(tmp.lexema)
                self.agregarHijo(n3,n4)
                tmp = self.tokens.pop()
                if tmp.tipo == "string":
                    n5 = self.crearNodo('string')
                    n6 = self.crearNodo(tmp.lexema)
                    self.agregarHijo(n5,n6)
                    self.text = tmp.lexema
                    tmp = self.tokens.pop()
                    if tmp.tipo == "parentesis final":
                        n7 = self.crearNodo('punto_y_coma')
                        n8 = self.crearNodo(tmp.lexema)
                        self.agregarHijo(n7,n8)
                        tmp = self.tokens.pop()
                        if tmp.tipo == "punto y coma":
                            n9 = self.crearNodo('punto_y_coma')
                            n10 = self.crearNodo(tmp.lexema)
                            self.agregarHijo(n9,n10)
                            n11 = self.crearNodo("INSTRUCCION_EXPORTAR")
                            self.agregarHijo(n11,n1)
                            self.agregarHijo(n11,n3)
                            self.agregarHijo(n11,n5)
                            self.agregarHijo(n11,n7)
                            self.agregarHijo(n11,n9)
                            Reporte_Lista(self.text, self.claves, self.registers)
                            self.text = ""
                        else:
                            self.agregaError(tmp.tipo, ';', tmp.linea, tmp.columna)
                    else:
                        self.agregaError(tmp.tipo, ')', tmp.linea, tmp.columna)
                else:
                    self.agregaError(tmp.tipo, 'string', tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "(", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "exportarReporte", tmp.linea, tmp.columna)


    # --------------------------------   INSTRUCCION PARA AGREGAR LAS CLAVES   --------------------------------------

    def INSTRUCCION_CLAVES(self):
        
        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "Claves":
            tmp = self.tokens.pop()
            if tmp.tipo == "igual":
                tmp = self.tokens.pop()
                if tmp.tipo == "corchete inicio":
                    tmp = self.tokens.pop()
                    self.CLAVES(tmp)
                else:
                    self.agregaError(tmp.tipo, "[", tmp.linea, tmp.columna)
            else:
                self.agregaError(tmp.tipo, "=", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "Claves", tmp.linea, tmp.columna)
            

    def CLAVES(self, tmp):
        if tmp.tipo == "string":
            self.claves.append(tmp.lexema)
            tmp = self.tokens.pop()
            self.CLAVES2(tmp)
        else:
            self.agregaError(tmp.tipo, "comilla", tmp.linea, tmp.columna)
            

    def CLAVES2(self, tmp):
        if tmp.tipo == "coma":
            tmp = self.tokens.pop()
            if tmp.tipo == "string":
                self.claves.append(tmp.lexema)
                tmp = self.tokens.pop()
                self.CLAVES2(tmp)
            else:
                self.agregaError(tmp.tipo, "string", tmp.linea, tmp.columna)
        
        elif tmp.tipo == "corchete final":
            self.actions.append(self.claves)
        else:
            self.agregaError(tmp.tipo, "coma", tmp.linea, tmp.columna)

    # ---------------------------------------------------------------------------------------------------

    def INSTRUCCION_REGISTROS(self):

        if self.text != "":
            self.actions.append(self.text)
            self.text = ""

        tmp = self.tokens.pop()
        if tmp.tipo == "Registros":
            tmp = self.tokens.pop()
            if tmp.tipo == "igual":
                tmp = self.tokens.pop()
                if tmp.tipo == "corchete inicio":
                    tmp = self.tokens.pop()
                    self.FILA(tmp)
                else:
                    self.agregaError(tmp.tipo, "[", tmp.linea, tmp.columna)
            else:
                    self.agregaError(tmp.tipo, "=", tmp.linea, tmp.columna)
        else:
            self.agregaError(tmp.tipo, "Registro", tmp.linea, tmp.columna)
    


    def FILA(self, tmp):
        
        if tmp.tipo == "llave inicio":
            tmp = self.tokens.pop()
            if tmp.tipo == "string" or tmp.tipo == "entero":
                self.conteo += 1
                self.aux.append(tmp.lexema)
                tmp = self.tokens.pop()
                self.FILA2(tmp)
            else:
                self.agregaError(tmp.tipo, "string", tmp.linea, tmp.columna)

        elif tmp.tipo == "corchete final":
            pass
        else:
            self.agregaError(tmp.tipo, "llave inicio", tmp.linea, tmp.columna)

    def FILA2(self, tmp):
        if tmp.tipo == "coma":
            tmp = self.tokens.pop()
            if tmp.tipo == "string" or tmp.tipo == "entero":
                self.aux.append(tmp.lexema)
                self.conteo += 1
                tmp = self.tokens.pop()
                self.FILA2(tmp)
        
        elif tmp.tipo == "llave final":
            tmp = self.tokens.pop()
            self.registers.append(self.aux)
            self.actions.append(self.aux)
            self.aux = []
            self.FILA(tmp)
            

    def imprimir_datos(self):
        x = PrettyTable()
        x.field_names = self.claves
        for i in self.registers:
            x.add_row(i)
        self.actions.append(x)
