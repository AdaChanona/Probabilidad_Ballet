from itertools import permutations
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import Text
from tkinter.constants import INSERT
from fractions import Fraction

#tkinter
raiz=tk.Tk()
raiz.title('Bailarinas de Ballet')
raiz.geometry('1000x700')
raiz.pack_propagate(False)
raiz.config(bg='white',width=1000,height=700)

global posiciones_ballet
global pasos_ballet
global bailarinas
global equipo_ballet
posiciones_ballet=[1,2,3,4,5]
pasos_ballet=['Relevé','Retiré']
bailarinas= [1,2,3,4,5,6,7,8,9,10]
equipo_ballet=[]

def equipo_bailarinas():
    equipo= permutations(bailarinas,2)

    for i in list(equipo):
        equipo_ballet.append(i)
    per='permutaciones= '+ str(len(equipo_ballet))
    return per

def rango_bailarinas():
    num_equipo=[]
    for i in range(5):
        num_equipo.append(random.choice(equipo_ballet)) 
    return num_equipo

def dataframe_equipos_seleccionados():
    num_equipo= rango_bailarinas()
    cont=1
    df = pd.DataFrame(columns=['Numero de equipo','Integrantes', 'bailarina principal', 'bailarina secundaria'],
                  index=range(5))
    for i in range(len(num_equipo)):
        equipo=num_equipo[i]
        df.iloc[i]=(cont,num_equipo[i],equipo[0],equipo[1])
        cont=cont+1
    return df

def practica_ballet():
    pasos=[]
    for i in range(len(posiciones_ballet)):
        if posiciones_ballet[i]%2==0:
            pasos.append(pasos_ballet[0])
        else:
            pasos.append(pasos_ballet[1])
    df_pos=pd.DataFrame(posiciones_ballet,columns=['POSICIONES'])
    df_pasos=pd.DataFrame(pasos,columns=['PASOS'])
    df_ballet=pd.concat([df_pos,df_pasos],axis=1)
    return df_ballet
        

def probabilidad_clasica(df_ballet):
    pasos=np.array(df_ballet['PASOS'])
    cont_ret=0
    cont_rel=0
    for i in range(len(pasos)):
        if pasos[i]=='Retiré':
            cont_ret=cont_ret+1
        else:
            cont_rel=cont_rel+1
    prob_ret=Fraction(cont_ret/len(pasos)).limit_denominator()
    prob_rel=Fraction(cont_rel/len(pasos)).limit_denominator()
    frecuencia=[cont_rel,cont_ret]
    prob_pasos=[prob_rel,prob_ret]
    conf=['P(Relevé)','P(Retiré)']
    df1=pd.DataFrame(conf,columns=['Configuraciones'])
    df2= pd.DataFrame(prob_pasos, columns=['Probabilidad'])
    df_salidas=pd.concat([df1,df2],axis=1)
    return df_salidas, frecuencia

def mostrar_grafica(df1,frecuencia):
    grafBarra=plt.bar(df1['Configuraciones'],frecuencia)
    plt.show()



def run():
    df_salida,frecuencia=probabilidad_clasica(practica_ballet())
    label1=tk.Label(raiz,text='Proyecto probabilidad: Bailarinas de ballet',font=(200))
    label1.place(x=300,y=40)
    label2=tk.Label(raiz,text=equipo_bailarinas(),font=(200))
    label2.place(x=650,y=180)
    label3=tk.Label(raiz,text='Equipos seleccionados',font=(50))
    label3.place(x=50,y=100)
    table1 = Text(raiz)
    table1.insert(INSERT,dataframe_equipos_seleccionados().to_string())
    table1.place(x=20, y=140,height=100, width=600)
    table2 = Text(raiz)
    label4=tk.Label(raiz,text='Probabilidad Clásica',font=(50))
    label4.place(x=50,y=270)
    table2.insert(INSERT,practica_ballet().to_string())
    table2.place(x=20, y=310,height=100, width=300)
    table3 = Text(raiz)
    table3.insert(INSERT,df_salida.to_string())
    table3.place(x=350, y=310,height=90, width=300)
    tk.Button(raiz, text="Grafica de barras", command=lambda:mostrar_grafica(df_salida,frecuencia)).place(x=750,y=350)



run()
raiz.mainloop()