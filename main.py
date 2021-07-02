from itertools import count, permutations
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
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
    df_pos=pd.DataFrame(posiciones_ballet,columns=['FASE 1 POSICIONES'])
    df_pasos=pd.DataFrame(pasos,columns=['FASE 2 PASOS'])
    df_ballet=pd.concat([df_pos,df_pasos],axis=1)
    return df_ballet
        
def probabilidad_clasica(df_ballet):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
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

def probabilidad_subjetiva_tabla1(df_ballet):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
    prob_posiciones=[]
    frec_pasos_par=[]
    frec_pasos_impar=[]
    for i in range(len(posiciones_ballet)):
        frec=posiciones_ballet.count(i+1)
        frec=frec/len(posiciones_ballet)
        frec=Fraction(frec).limit_denominator()
        prob_posiciones.append(frec)
        if pasos[i]=='Relevé':
            frec_pasos_par.append(1)
        else:
            frec_pasos_par.append(0)
        if pasos[i]=='Retiré':
            frec_pasos_impar.append(1)
        else:
            frec_pasos_impar.append(0)
        
    df_prob=pd.DataFrame(prob_posiciones,columns=['Fase 1 Posiciones'])
    df_par=pd.DataFrame(frec_pasos_par,columns=['Paso 1 Relevé'])
    df_impar=pd.DataFrame(frec_pasos_impar,columns=['Paso 2 Retiré'])
    df_subjetiva1=pd.concat([df_prob,df_par,df_impar],axis=1)
    suma=sum(prob_posiciones)
    prob_posiciones.append(suma)
    return df_subjetiva1,prob_posiciones

def probabilidad_subjetiva_tabla2(prob_pos, df_ballet):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
    pasos_fraccion_par=[]
    pasos_fraccion_impar=[]
    cont_par=0
    cont_impar=0
    for i in range(len(pasos)):
        if pasos[i]=='Relevé':
            cont_par=1
            pasos_fraccion_par.append(Fraction(cont_par/len(pasos)).limit_denominator())
            cont_par=0
        else:
            pasos_fraccion_par.append(0)
        if pasos[i]=='Retiré':
            cont_impar=1
            pasos_fraccion_impar.append(Fraction(cont_impar/len(pasos)).limit_denominator())
            cont_impar=0
        else:
            pasos_fraccion_impar.append(0)
    suma_par=sum(pasos_fraccion_par)
    pasos_fraccion_par.append(suma_par)
    sum_impar=sum(pasos_fraccion_impar)
    pasos_fraccion_impar.append(sum_impar)
    df1= pd.DataFrame(prob_pos,columns=['Fase 1 Posciones'])
    df2=pd.DataFrame(pasos_fraccion_par,columns=['Fase 2 Paso 1 Relevé'])
    df3=pd.DataFrame(pasos_fraccion_impar,columns=['Fase 2 Paso 2 Retiré'])
    df_subjetiva2=pd.concat([df1,df2,df3],axis=1)
    return df_subjetiva2

df_subjetivo1, array=probabilidad_subjetiva_tabla1(practica_ballet())

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
    label5=tk.Label(raiz,text='Probabilidad Subjetiva',font=(50))
    label5.place(x=50,y=450)
    table4 = Text(raiz)
    table4.insert(INSERT,df_subjetivo1.to_string())
    table4.place(x=20, y=500,height=100, width=450)
    table5 = Text(raiz)
    table5.insert(INSERT,probabilidad_subjetiva_tabla2(array, practica_ballet()).to_string())
    table5.place(x=500, y=500,height=120, width=500)

run()
raiz.mainloop()