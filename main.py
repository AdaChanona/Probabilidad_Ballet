from itertools import permutations
import random
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib.function_base import append
import pandas as pd
import tkinter as tk
from tkinter import Text
from tkinter.constants import INSERT
from fractions import Fraction

global posiciones_ballet
global pasos_ballet
global bailarinas
global equipo_ballet
posiciones_ballet=[1,2,3,4,5]
pasos_ballet=['Relevé','Retiré']
bailarinas= [1,2,3,4,5,6,7,8,9,10]
equipo_ballet=[]

def permutaciones_bailarinas():
    equipo= permutations(bailarinas,2)
    for i in list(equipo):
        equipo_ballet.append(i)
    per='permutaciones= '+ str(len(equipo_ballet))
    return per

def equipo_bailarinas():
    num_equipo=[]
    for i in range(len(posiciones_ballet)):
        num_equipo.append(random.choice(equipo_ballet)) 
    return num_equipo

def dataframe_equipos_seleccionados():
    num_equipo= equipo_bailarinas()
    rango=int(len(bailarinas)/2)
    cont=1
    df = pd.DataFrame(columns=['Numero de equipo','Integrantes', 'bailarina principal', 'bailarina secundaria'],
                  index=range(rango))
    for i in range(rango):
        equipo=num_equipo[i]
        df.iloc[i]=(cont,num_equipo[i],equipo[0],equipo[1])
        cont=cont+1
    return df

def tabla_fases():
    pasos=[]
    for i in range(len(posiciones_ballet)):
        if posiciones_ballet[i]%2==0:
            pasos.append(pasos_ballet[0])
        else:
            pasos.append(pasos_ballet[-1])
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
    prob_salida=[]
    cont_par=0
    cont_impar=0
    for i in range(len(pasos)):
        if pasos[i]=='Relevé':
            cont_par=1
            pasos_fraccion_par.append(Fraction(cont_par/len(pasos)).limit_denominator())
            prob_salida.append(pasos_fraccion_par[i]*prob_pos[i])
            cont_par=0
        else:
            pasos_fraccion_par.append(0)
        if pasos[i]=='Retiré':
            cont_impar=1
            pasos_fraccion_impar.append(Fraction(cont_impar/len(pasos)).limit_denominator())
            prob_salida.append(pasos_fraccion_impar[i]*prob_pos[i])
            cont_impar=0
        else:
            pasos_fraccion_impar.append(0)
    suma_salida=sum(prob_salida)
    prob_salida.append(suma_salida)
    suma_par=sum(pasos_fraccion_par)
    pasos_fraccion_par.append(suma_par)
    sum_impar=sum(pasos_fraccion_impar)
    pasos_fraccion_impar.append(sum_impar)
    df1= pd.DataFrame(prob_pos,columns=['Fase 1 Posciones'])
    df2=pd.DataFrame(pasos_fraccion_par,columns=['Fase 2 Paso 1 Relevé'])
    df3=pd.DataFrame(pasos_fraccion_impar,columns=['Fase 2 Paso 2 Retiré'])
    df4=pd.DataFrame(prob_salida,columns=['Probabilidad de salida'])
    df_subjetiva2=pd.concat([df1,df2,df3,df4],axis=1)
    return df_subjetiva2

def conf_parametro():
    op=0
    while op<3:
        print('Escoja una opción')
        print('1. Ingresar nueva posicion    2. Eliminar posicion   3. Salir')
        op=int(input())
        if op==1:
            print('Estas son las posiciones de ballet: ')
            print(posiciones_ballet)
            pos_new=int(input('Ingresa posición de ballet: '))
            posiciones_ballet.append(pos_new)
            print('Se agrego la posicion ', posiciones_ballet)
        elif op==2:
            print('Estas son las posiciones de ballet: ')
            print(posiciones_ballet)
            pos_delete=int(input('Ingresa posición de ballet que deseas eliminar: '))
            posiciones_ballet.remove(pos_delete)
            print('Se eliminó la posición ',posiciones_ballet)

def empirico(equipo):
    num_equipo=np.array(equipo['Numero de equipo'])
    cont_pos=[]
    op=0
    while op==1 or op==2 or op==0:
        print('----------------------------------------------------')
        print('Escoja una opcion')
        print('1. Configurar simulación')
        print('2. Simular')
        print('3. Imprimir resultados')
        op=int(input())
        if(op==1):
            conf_parametro()
        if(op==2):
            repeticion=int(input('¿Cuantas veces quiere repetir la simulación? '))
            for i in range(repeticion):
                print('-----------------------------------------------------')
                print('Escogiendo equipo...')
                print('Te toco el equipo: ',random.choice(num_equipo))
                print('La posición se escogerá aleatoriamente')
                pos=random.choice(posiciones_ballet)
                cont_pos.append(pos)
                print('La bailarina principal hará un plié en la posicion: ', pos)
                if(pos%2==0):
                    print('La bailarina secundaria hará un: ',pasos_ballet[0])
                else:
                    print('La bailarina secundaria hará un: ',pasos_ballet[-1])
    return cont_pos

def resultados_simulacion(cont_pos):
    frec_pos_par=0
    frec_pos_impar=0
    frec_paso_releve=0
    frec_paso_retire=0
    for i in range(len(cont_pos)):
        if cont_pos[i]%2==0:
            frec_pos_par=frec_pos_par+1
            frec_paso_releve=frec_paso_releve+1
        else:
            frec_pos_impar=frec_pos_impar+1
            frec_paso_retire=frec_paso_retire+1
    frecuencia_total_pos=[frec_pos_par,frec_pos_impar]
    grafica_posicion=plt.bar(['par','impar'],frecuencia_total_pos)
    plt.title('Posiciones de ballet')
    plt.xlabel('Configuraciones')
    plt.ylabel('Frecuencia')
    plt.show()
    frecuencia_total_pasos=[frec_paso_releve,frec_paso_retire]
    grafica_pasos=plt.bar(['Relevé','Retiré'],frecuencia_total_pasos)
    plt.title('Pasos de ballet')
    plt.xlabel('Configuraciones')
    plt.ylabel('Frecuencia')
    plt.show()


permutaciones=permutaciones_bailarinas()
equipo=equipo_bailarinas()
equipo_select=dataframe_equipos_seleccionados()
cont_pos=empirico(equipo_select)
df_subjetivo1, array=probabilidad_subjetiva_tabla1(tabla_fases())

#tkinter
raiz=tk.Tk()
raiz.title('Bailarinas de Ballet')
raiz.geometry('1300x680')
raiz.pack_propagate(False)
raiz.config(bg='white',width=1300,height=680)
def run():
    df_salida,frecuencia=probabilidad_clasica(tabla_fases())
    label1=tk.Label(raiz,text='Proyecto probabilidad: Bailarinas de ballet',font=(200))
    label1.place(x=500,y=40)
    label2=tk.Label(raiz,text=permutaciones,font=(200))
    label2.place(x=900,y=180)
    label3=tk.Label(raiz,text='Equipos seleccionados',font=(50))
    label3.place(x=50,y=100)
    table1 = Text(raiz)
    table1.insert(INSERT,equipo_select.to_string())
    table1.place(x=20, y=140,height=150, width=600)
    table2 = Text(raiz)
    label4=tk.Label(raiz,text='Probabilidad Clásica',font=(50))
    label4.place(x=50,y=270)
    table2.insert(INSERT,tabla_fases().to_string())
    table2.place(x=20, y=310,height=150, width=300)
    table3 = Text(raiz)
    table3.insert(INSERT,df_salida.to_string())
    table3.place(x=350, y=310,height=90, width=300)
    label5=tk.Label(raiz,text='Probabilidad Subjetiva',font=(50))
    label5.place(x=50,y=450)
    table4 = Text(raiz)
    table4.insert(INSERT,df_subjetivo1.to_string())
    table4.place(x=20, y=500,height=150, width=450)
    table5 = Text(raiz)
    table5.insert(INSERT,probabilidad_subjetiva_tabla2(array, tabla_fases()).to_string())
    table5.place(x=500, y=500,height=150, width=750)
    label6=tk.Label(raiz,text='Resultados de simulación',font=(200))
    label6.place(x=880,y=300)
    tk.Button(raiz, text="Resultado en Graficas", command=lambda:resultados_simulacion(cont_pos)).place(x=930,y=350)

print('Imprimiendo probabilidades...')
run()
raiz.mainloop()