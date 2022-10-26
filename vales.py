
from tkinter import *
from reportlab.graphics.barcode import code93
from reportlab.graphics.barcode import code39
from reportlab.graphics.barcode import usps
from reportlab.graphics.barcode import usps4s
from reportlab.graphics.barcode import ecc200datamatrix
import sqlite3 as sq3
from tkinter import messagebox
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
import ttkbootstrap as ttk


con = sq3.connect('vales_db.db')
cur = con.cursor()

#MenuAyuda
    #Lincecia
def licencia():
    gnuglp = '''
    Generador vales pdf, gestionador de vales
    Copyright (C) 2022 - Matias Salinas
    \n ===============================
    This program is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public 
    License as published by the Free Software Foundation, 
    either version 3 of the License, or (at your option) any 
    later version.
    This program is distributed in the hope that it will be 
    useful, but WITHOUT ANY WARRANTY; without even the 
    implied warranty of MERCHANTABILITY or FITNESS FOR A 
    PARTICULAR PURPOSE.  See the GNU General Public License 
    for more details.
    You should have received a copy of the GNU General Public 
    License along with this program.  
    If not, see <https://www.gnu.org/licenses/>.
    '''
    messagebox.showinfo("Lincencia",gnuglp)

    #AcercaDe
def acerca():
    messagebox.showinfo("Acerca de..","Creado por Matias Salinas")

def salir():
    resp = messagebox.askquestion('Confrimar','Desea salir del programa?')
    if resp == "yes":
        con.close() # desconecta la base de datos
        raiz.destroy() # cierra el programa


def capta_codigo(self):

    estado_texto =''
    query_codigo = '''SELECT * FROM vales
    WHERE _id ='''
    #for registro in cur.execute(query_codigo + codigo):
    #    print(registro)
    cur.execute(query_codigo + codigo.get())
    resultado = cur.fetchall()
    print(resultado)
    if resultado == []:
        messagebox.showerror('ERROR','No existe un vale con ese codigo en la base de datos.')
    else:
        for campo in resultado:
            codigo.set(campo[0])
            nombre.set(campo[1])
            monto.set(campo[2])
            estado.set(campo[3])
    if estado.get() == 0:
        estado_t.set('Vigente')
    else:
        estado_t.set('utilizado')
def buscar_nombres():

    cur.execute('SELECT nombre FROM valesnombres')
            #fetchall guarda la info que trajo el execute
    resultado = cur.fetchall()
    #print(resultado)
    retorno =['Nombres']
    for e in resultado:
        nombre = e[0]
        retorno.append(nombre) #append agrega el elemento al final de una lista
    
    return retorno

def generar():
    instruct1 = '''SELECT max(_id) FROM vales'''
    cur.execute(instruct1)
    numero = cur.fetchone()
    numero1 = numero[0] + 1
    letras = monto_esc.get()
    son = monto_num.get()
    nombrev = nombreva.get()
    cantidad = int(vales.get()/10)
    my_canvas = canvas.Canvas('Vales'+nombrev+str(son)+'.pdf')
    for h in range(cantidad):
        my_canvas.line(297.5,842,297.5,0)
        my_canvas.line(0,673.6,595,673.6)
        my_canvas.line(0,505.2,595,505.2)
        my_canvas.line(0,505.2,595,505.2)
        my_canvas.line(0,336.8,595,336.8)
        my_canvas.line(0,168.4,595,168.4)
        x=0
        y=842
        
        
        for k in range(2):
            
            for i in range (5):
                
                numerostring = str(numero1).zfill(8)
                codigo = code128.Code128(numerostring)
                my_canvas.setFont('Helvetica-Bold',24)
                my_canvas.drawString(x+10,y-22,'YPF')
                my_canvas.rect(x+8,y-32,50,8,stroke=1,fill=1)#Linea debajo YPF
                my_canvas.setFont('Helvetica',20)
                my_canvas.drawString(x+60,y-18,'VALE')
                my_canvas.setFont('Times-Roman',18)
                my_canvas.drawString(x+120,y-18,'Horacio Brigido S.R.L')
                my_canvas.drawString(x+60,y-52,'Por la suma de: .....................')
                #numero en letras
                my_canvas.drawString(x+190,y-49,letras)
                my_canvas.setFont('Courier',14)
                my_canvas.drawCentredString(x+147,y-68,nombrev)
                my_canvas.setFont('Helvetica-Bold',16)
                my_canvas.drawString(x+5,y-165,'Son $.............')
                my_canvas.setFont('Helvetica-Bold',24)
                my_canvas.drawString(x+50,y-160,str(son))
                my_canvas.setFont('Helvetica',10)
                my_canvas.drawString(x+240,y-165,'Firma')
                my_canvas.drawString(x+205,y-155,'.................................')
                my_canvas.drawString(x+120,y-85,numerostring)
                codigo.drawOn(my_canvas,x+100,y-115)
                lista1 = [(numero1,nombrev,son,0)]
                con.executemany('''INSERT INTO vales VALUES  (?,?,?,?)''',lista1)
                con.commit()
                y -= 168.4
                numero1 += 1
            y=842
            x = x + 297.5
        my_canvas.showPage()
    my_canvas.save()

def capta_vales(self):
    try:
        cantidadV = vales.get()
    except FloatingPointError:
        print("FPE")
        return
    except ValueError:
        print("VE")
        return
    except TclError:
        messagebox.showerror('Error','Solo ingrese numeros')
        return
    msg = ''
    if cantidadV %10 != 0:
        msg = 'ingrese un numero valido'
        messagebox.showerror('Error', msg)
    else:
        pass

def abrir():
    global vales, nombreva,monto_num,monto_esc
    vales = IntVar()
    nombreva = StringVar()
    monto_num = IntVar()
    monto_esc = StringVar()
    #paginas = IntVar()

    top = Toplevel()
    nombres = buscar_nombres()
    vales_label = ttk.Label(top, text='Vales a generar:', font='Times')
    vales_label.grid(row=0,column=0,padx=5,pady=5)

    vales_input = ttk.Entry(top, textvariable=vales)
    vales_input.grid(row=0, column=1,padx=10,pady=10)
    vales_input.bind('<Return>', capta_vales)
    vales_input.bind('<Tab>', capta_vales)

    nombrede_label = ttk.Label(top, text='A nombre de:', font='Times')
    nombrede_label.grid(row=1,column=0,padx=5,pady=5)
    
    nombre_option = ttk.OptionMenu(top,nombreva, *nombres)#frame donde esta, la variable que esta utilizando, y al final de donde saca la info, el astericos es por que no sabemos cuanta info le vamos a pasar
    nombre_option.grid(row=1,column=1,padx=10,pady=10)


    monto_num_label = ttk.Label(top, text='Monto en numero:', font='Times')
    monto_num_label.grid(row=2,column=0,padx=5,pady=5)

    monto_num_input = ttk.Entry(top, textvariable=monto_num)
    monto_num_input.grid(row=2, column=1,padx=10,pady=10)

    monto_esc_label = ttk.Label(top, text='Monto escrito:', font='Times')
    monto_esc_label.grid(row=3,column=0,padx=5,pady=5)

    monto_esc_input = ttk.Entry(top, textvariable=monto_esc)
    monto_esc_input.grid(row=3, column=1,padx=10,pady=10)
    '''
    paginas_label = ttk.Label(top, text='Paginas a generar(10):', font='Times')
    paginas_label.grid(row=4,column=0,padx=5,pady=5)
    
    paginas_input = ttk.Entry(top, textvariable=paginas)
    paginas_input.grid(row=4, column=1,padx=10,pady=10)
    '''
    

    boton_generar = ttk.Button(top,text='Generar vales',command=generar)
    boton_generar.grid(row=4, column=1)

def checkestado():
    if estado.get() == 0:
        estado.set(1)
        estado_t.set('Utilizado')
        cur.execute('UPDATE vales SET estado = 1 WHERE _id = '+ codigo.get())
        con.commit()
        
    
    else:
        estado.set(0)
        estado_t.set('Vigente')
        cur.execute('UPDATE vales SET estado = 0 WHERE _id= '+ codigo.get())
        con.commit()
        print('chau')
    print(estado.get())


raiz = Tk()
style = ttk.Style('superhero')
raiz.title('Vales')
raiz.iconbitmap("logo_ypf.ico")

def destinatario():
    top1 = Toplevel()
    global nombre_agregar
    nombre_agregar = StringVar()

    nombre_label = ttk.Label(top1,text='Nombre')
    nombre_label.grid(row=1, column=0, padx=5, pady=5)
    nombre_input = ttk.Entry(top1,textvariable=nombre_agregar)
    nombre_input.grid(row=1, column=2, padx=5, pady=5)

    boton_agregar = ttk.Button(top1, command=agregar_destinatario,text="Agregar")
    boton_agregar.grid(row= 2, column=1)

def agregar_destinatario():
    instruct1 = '''SELECT max(_id) FROM valesnombres'''
    cur.execute(instruct1)
    numero = cur.fetchone()
    numero1 = numero[0] + 1
    nombre = nombre_agregar.get()
    lista2=[(numero1,nombre)]
    cur.executemany('INSERT INTO valesnombres VALUES (?,?)',lista2)
    con.commit()
    


#####################################
#----------INTERFAZ------------------
#####################################


barramenu = Menu(raiz) # crea barra menu
raiz.config(menu=barramenu) # agregar el menu a la patanlla principal

bbddmenu = Menu(barramenu, tearoff=0) #crea el submenu bbdd
bbddmenu.add_command(label='Generar vales',command=abrir)
bbddmenu.add_command(label='Agregar destinatario', command=destinatario)
bbddmenu.add_command(label='Salir', command=salir) #agrega el boton salir



ayudamenu = Menu(barramenu, tearoff=0)
ayudamenu.add_command(label= 'Licencia',command=licencia)
ayudamenu.add_command(label='Acerca de',command=acerca)

barramenu.add_cascade(label ='Menu', menu = bbddmenu)#crea el boton BBDD y le asigna los botones del submenu

barramenu.add_cascade(label= 'Acerca de...', menu = ayudamenu)

framecampos = Frame(raiz)
framecampos.pack(fill='y')

codigo = StringVar()
nombre = StringVar()
monto = DoubleVar()
estado = BooleanVar()
estado_t = StringVar()



codigo_label = ttk.Label(framecampos, text='Codigo', font='Times')
codigo_label.grid(row=1,column=0,padx=5,pady=5)
codigo_input = ttk.Entry(framecampos, textvariable=codigo)
codigo_input.grid(row=2, column=0,padx=10,pady=10)
codigo_input.bind('<Return>',capta_codigo)
codigo_input.bind('<Tab>',capta_codigo)

nombre_label = ttk.Label(framecampos,textvariable=nombre,font='Times')
nombre_label.grid(row=3, column=0,padx=5,pady=5)

monto_label = ttk.Label(framecampos,text='Monto',font='Times')
monto_label.grid(row=4,column=0,padx=5,pady=5)

monto2_label = ttk.Label(framecampos,textvariable=monto,font='Times')
monto2_label.grid(row=5,column=0,padx=5,pady=5)

estado_label = ttk.Label(framecampos,text='Estado',font='Times')
estado_label.grid(row=6,column=0,padx=5,pady=5)

estado2_label = ttk.Label(framecampos,textvariable=estado_t,font='Times')
estado2_label.grid(row=7,column=0,padx=5,pady=5)

estado_pasar_button = ttk.Checkbutton(framecampos,command=checkestado)
estado_pasar_button.grid(row=7,column=1)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        con.close() # desconecta la base de datos
        print('p')
        raiz.destroy()


raiz.protocol("WM_DELETE_WINDOW", on_closing)
raiz.mainloop()