from tkinter import *
from tkinter import ttk 
from AnalizadorLexico import AnalizadorLexico
from AnalizadorSintactico import AnalizadorSintactico
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from reportes import Errors_report, Errors_report_Sintact, Tokens_report

def Cargar_Archivo():
    Tk().withdraw()
    filename = askopenfilename()
    if ".lfp" in filename:
        messagebox.showinfo("Carga Completa", "El archivo se cargó correctamente")
        file = open(filename, 'r')
        content = file.read()
        terminal.insert(END, content)
        file.close()
    else: 
        messagebox.showerror("Error", "El archivo debe contener la extension \".lfp\"")

def Analizar_Archivo():
    console.delete('1.0','end')
    scanner = AnalizadorLexico()
    scanner.analizar(terminal.get('1.0','end'))
    
    if ComboBox_report.get() == "Tokens":
        Tokens_report(scanner.listaTokens)
    elif ComboBox_report.get() == "Errores":
        Errors_report(scanner.listaErrores, "Errores_Lexicos")
        
    sintactic = AnalizadorSintactico(scanner.listaTokens)
    sintactic.analizar()
    if ComboBox_report.get() == "Errores":
        Errors_report_Sintact(sintactic.errores, "Errores_Sintacticos")
    elif ComboBox_report.get() == "Árbol":
        sintactic.g.view()
    acciones = sintactic.actions
    for i in acciones:
        console.insert(END, "\n" + str(i))     
    

if __name__ == '__main__':

    form = Tk()
    form.title("MARK20")
    form["bg"]='#0062a4'
    form.resizable(False, False)
    form_height = 700 
    form_width = 1310
    screen_width = form.winfo_screenwidth() 
    screen_height = form.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (form_width/2)) 
    y_cordinate = int((screen_height/2) - (form_height/2))
    form.geometry("{}x{}+{}+{}".format(form_width, form_height, x_cordinate, y_cordinate))

    console = Text(form, height=37, width=80, background="#1e1e1e", foreground="#fff", )
    console.place(x=635, y=80)
    terminal = Text(form, height=37, width=71, background="#1e1e1e", foreground="#fff")
    terminal.place(x=30, y=80)

    #buttons
    button_charge = Button(form, text="Cargar Archívo", height=1, width=15,command = Cargar_Archivo).place(x=400, y=30)
    button_analasys = Button(form, text = "Analizar Archivo", height=1, width=15, command= Analizar_Archivo).place(x=540, y=30)

    datos = ["Tokens","Errores","Árbol"]
    #comboBox
    ComboBox_report = ttk.Combobox(form, width=15)
    ComboBox_report.place(x=680, y=32)
    ComboBox_report["values"] = datos
    ComboBox_report.current(0)

    form.mainloop()