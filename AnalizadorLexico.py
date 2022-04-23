from Token import Token
from error import Error
from prettytable import PrettyTable

class AnalizadorLexico:
    
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []
        self.linea = 1
        self.columna = 1
        self.buffer = ''
        self.estado = 0
        self.i = 0

    
    def agregar_token(self,caracter,token,linea,columna):
        self.listaTokens.append(Token(caracter,token,linea,columna))
        self.buffer = ''


    def agregar_error(self,caracter,linea,columna):
        self.listaErrores.append(Error('Caracter ' + caracter + ' no reconocido en el lenguaje.', linea, columna))

    def estado0(self,caracter):
        if caracter == '=':
            self.agregar_token(caracter,'igual',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == '[':
            self.agregar_token(caracter,'corchete inicio',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == ']':
            self.agregar_token(caracter,'corchete final',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == ',':
            self.agregar_token(caracter,'coma',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == '{':
            self.agregar_token(caracter,'llave inicio',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == '}':
            self.agregar_token(caracter,'llave final',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == ';':
            self.agregar_token(caracter,'punto y coma',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == '(':
            self.agregar_token(caracter,'parentesis inicio', self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == ')':
            self.agregar_token(caracter,'parentesis final',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        elif caracter == '_':
            self.agregar_token(caracter,'guion bajo',self.linea,self.columna)
            self.buffer = ''
            self.columna+=1
        #Transicion para estado 1
        elif caracter.isdigit():
            self.buffer += caracter
            self.estado = 1
        #Transicion para estado 2
        elif caracter.isalpha():
            self.buffer += caracter  
            self.estado = 2  
        #Transicion para estado 3
        elif caracter == '#':
            self.buffer += caracter  
            self.estado = 3
        #Transicion para estado 4
        elif caracter == "'":
            self.buffer += caracter
            self.estado = 4 
        #Transicion para estado 7
        elif caracter == '"':    
            self.estado = 7
        elif caracter == '\n':
            self.linea += 1
            self.columna = 1
        elif caracter == ' ':
            self.buffer = ''
            self.columna += 1  
        elif caracter == "\t":
            self.columna +=4
        elif caracter == '\r':
            pass
        #Zona de errores
        else:
            self.buffer += caracter
            self.agregar_error(self.buffer,self.linea,self.columna)
            self.buffer = ''
            self.columna += 1            


    def estado1(self,caracter):
        if caracter.isdigit():
            self.buffer+=caracter
            self.columna+=1
        elif caracter == ".":
            self.buffer+=caracter
            self.columna+=1
        else:
            self.agregar_token(self.buffer,'entero',self.linea,self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1

    def estado2(self,caracter):
        if caracter.isalpha():
            self.buffer+=caracter
            self.columna+=1
        elif caracter == "_":
            self.buffer+=caracter
            self.columna+=1
        else:           
            if self.buffer == "Claves":
                self.agregar_token(self.buffer,'Claves',self.linea,self.columna) 
        
            elif self.buffer == "Registros":
                self.agregar_token(self.buffer,'Registros',self.linea,self.columna)
        
            elif self.buffer == "imprimir":
                self.agregar_token(self.buffer,'imprimir',self.linea,self.columna)

            elif self.buffer == "imprimirln":
                self.agregar_token(self.buffer,'imprimirln',self.linea,self.columna)

            elif self.buffer == "conteo":
                self.agregar_token(self.buffer,'conteo',self.linea,self.columna)
        
            elif self.buffer == "promedio":
                self.agregar_token(self.buffer,'promedio', self.linea, self.columna)

            elif self.buffer == "contarsi":
                self.agregar_token(self.buffer,'contarsi',self.linea,self.columna)
        
            elif self.buffer == "datos":
                self.agregar_token(self.buffer, 'datos', self.linea, self.columna)

            elif self.buffer == "sumar":
                self.agregar_token(self.buffer,'sumar', self.linea, self.columna)
        
            elif self.buffer == "max":
                self.agregar_token(self.buffer,'max', self.linea, self.columna)
        
            elif self.buffer == "min":
                self.agregar_token(self.buffer,'min', self.linea, self.columna)
        
            elif self.buffer == "exportarReporte":
                self.agregar_token(self.buffer,'exportarReporte', self.linea, self.columna)
            else:
                self.agregar_token(self.buffer,'palabra', self.linea, self.columna)
            self.columna+=1
            self.estado = 0
            self.i -= 1
    
    # estado para los comentarios de una línea
    
    def estado3(self, caracter):
        if caracter.isalpha():
            self.buffer += caracter
            self.columna += 1
        elif caracter == " ":
            self.buffer+= caracter
            self.columna += 1
        else:
            self.columna +=1
            self.buffer = ''
            self.estado = 0
            self.i -= 1

    def estado4(self, caracter):
        if caracter == "'":
            self.buffer += caracter
            self.columna += 1
        else:
            self.buffer += caracter
            self.columna += 1
            self.estado = 5

    def estado5(self, caracter):       
        if caracter == " ":
            self.buffer = ''
        elif caracter == '\n':
            self.buffer = ''
            self.columna += 1
            self.linea += 1
        elif caracter == '\t':
            self.buffer = ''
            self.columna +=4
            self.linea += 1
        elif caracter.isalpha():
            self.buffer = ''
            self.columna += 1
        elif caracter.isdigit():
            self.buffer = ''
            self.columna += 1
        else:
            self.buffer = ''
            self.columna += 1
            self.estado = 6
    
    def estado6(self, caracter):
        if caracter == "'":
            self.buffer = ''
            self.columna += 1
        else:
            self.buffer = ''
            self.columna += 1
            self.estado = 0
            self.i -= 1

    def estado7(self, caracter):
        if caracter.isalpha():
            self.buffer += caracter
            self.columna += 1
        elif caracter.isdigit():
            self.buffer += caracter
            self.columna += 1
        elif caracter == '/':
            self.buffer += caracter
            self.columna+=1
        elif caracter == '\\':
            self.buffer += caracter
            self.columna+=1
        elif caracter == '*':
            self.buffer += caracter 
            self.columna+=1
        elif caracter == " ":
            self.buffer += caracter
            self.columna+=1
        elif caracter == "_":
            self.buffer += caracter
            self.columna+=1
        else:
            self.estado = 8
            self.columna+=1
    
    def estado8(self, caracter):
        if caracter == '"':
            self.buffer += caracter
            self.columna += 1
            print("llegué aquí")
        else:
            self.agregar_token(self.buffer,'string', self.linea, self.columna)
            self.estado = 0
            self.columna+=1
            self.i -= 1

           

    def analizar(self, cadena):
        self.listaTokens = []
        self.listaErrores = []


        #recorrer caracter por caracter
        self.i = 0
        while self.i < len(cadena):
            if self.estado == 0:
                self.estado0(cadena[self.i])
            elif self.estado == 1:
                self.estado1(cadena[self.i])
            elif self.estado == 2:
                self.estado2(cadena[self.i])
            elif self.estado == 3:
                self.estado3(cadena[self.i])
            elif self.estado == 4:
                self.estado4(cadena[self.i])
            elif self.estado == 5:
                self.estado5(cadena[self.i])
            elif self.estado == 6:
                self.estado6(cadena[self.i])
            elif self.estado == 7:
                self.estado7(cadena[self.i])
            elif self.estado == 8:
                self.estado8(cadena[self.i])
            self.i += 1

    def impTokens(self):
        x = PrettyTable()
        x.field_names = ["Lexema", "Token", "Fila", "Columna"]
        for i in self.listaTokens:
            x.add_row(i.Enviar())
        print(x)

    def impErrores(self):
        x = PrettyTable()
        x.field_names = ["Descripcion", "Fila", "Columna"]
        if len(self.listaErrores)==0:
            print('No hay errores')
        else:
            for i in self.listaErrores:
                x.add_row(i.Enviar())
            print(x)

                