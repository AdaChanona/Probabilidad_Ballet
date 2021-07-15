from itertools import permutations
import random
import matplotlib.pyplot as plt
import numpy as np
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
pasos_ballet=['Retiré','Relevé']
bailarinas= [1,2,3,4,5,6,7,8,9,10]
equipo_ballet=[]

def permutaciones_bailarinas():
    equipo= permutations(bailarinas,2)
    for i in list(equipo):
        equipo_ballet.append(i)
    per=len(equipo_ballet)
    return per

def equipo_bailarinas(per):
    conf=per*len(posiciones_ballet)
    return conf

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
        
def probabilidad_clasica(df_ballet,conf):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
    cont_ret=0
    cont_rel=0
    for i in range(len(pasos)):
        if pasos[i]=='Retiré':
            cont_ret=cont_ret+1
        else:
            cont_rel=cont_rel+1
    prob_ret=Fraction(cont_ret/conf).limit_denominator()
    prob_rel=Fraction(cont_rel/conf).limit_denominator()
    prob_pasos=[prob_ret,prob_rel]
    conf=['P(Retiré)','P(Relevé)']
    df1=pd.DataFrame(conf,columns=['Salidas'])
    df2= pd.DataFrame(prob_pasos, columns=['Probabilidad'])
    df_salidas=pd.concat([df1,df2],axis=1)
    df_salidas.to_csv('./Resultados/Probabilidad_Clasica.csv')
    return df_salidas

def probabilidad_subjetiva_tabla1(df_ballet,conf):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
    prob_posiciones=[]
    frec_pasos_par=[]
    frec_pasos_impar=[]
    for i in range(len(posiciones_ballet)):
        frec=posiciones_ballet.count(i+1)
        frec=frec/conf
        frec=Fraction(frec).limit_denominator()
        prob_posiciones.append(frec)
        if pasos[i]=='Relevé':
            frec_pasos_impar.append(1)
        else:
            frec_pasos_impar.append(0)
        if pasos[i]=='Retiré':
            frec_pasos_par.append(1)
        else:
            frec_pasos_par.append(0)
        
    df_prob=pd.DataFrame(prob_posiciones,columns=['Fase 1 Posiciones'])
    df_par=pd.DataFrame(frec_pasos_par,columns=['Paso 1 Retiré'])
    df_impar=pd.DataFrame(frec_pasos_impar,columns=['Paso 2 Relevé'])
    df_subjetiva1=pd.concat([df_prob,df_par,df_impar],axis=1)
    suma=sum(prob_posiciones)
    prob_posiciones.append(suma)
    return df_subjetiva1,prob_posiciones

def probabilidad_subjetiva_tabla2(prob_pos, df_ballet,conf):
    pasos=np.array(df_ballet['FASE 2 PASOS'])
    pasos_fraccion_par=[]
    pasos_fraccion_impar=[]
    prob_salida=[]
    cont_par=0
    cont_impar=0
    for i in range(len(pasos)):
        if pasos[i]=='Relevé':
            cont_impar=1
            pasos_fraccion_impar.append(Fraction(cont_impar/conf).limit_denominator())
            prob_salida.append(pasos_fraccion_impar[i]*prob_pos[i])
            cont_impar=0
        else:
            pasos_fraccion_impar.append(0)
        if pasos[i]=='Retiré':
            cont_par=1
            pasos_fraccion_par.append(Fraction(cont_par/conf).limit_denominator())
            prob_salida.append(pasos_fraccion_par[i]*prob_pos[i])
            cont_par=0
        else:
            pasos_fraccion_par.append(0)
    suma_salida=sum(prob_salida)
    prob_salida.append(suma_salida)
    suma_par=sum(pasos_fraccion_par)
    pasos_fraccion_par.append(suma_par)
    sum_impar=sum(pasos_fraccion_impar)
    pasos_fraccion_impar.append(sum_impar)
    df1= pd.DataFrame(prob_pos,columns=['Fase 1 Posiciones'])
    df2=pd.DataFrame(pasos_fraccion_par,columns=['Fase 2 Paso 1 Retiré'])
    df3=pd.DataFrame(pasos_fraccion_impar,columns=['Fase 2 Paso 2 Relevé'])
    df4=pd.DataFrame(prob_salida,columns=['Probabilidad de salida'])
    df_subjetiva2=pd.concat([df1,df2,df3,df4],axis=1)
    df_subjetiva2.to_csv('./Resultados/Probabilidad_subjetiva.csv')
    return df_subjetiva2

def config_parametro():
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

def empirico():
    cont_pos1000=[]
    cont_pos5000=[]
    cont_pos10000=[]
    cont_pos100000=[]
    op=0
    while op==1 or op==2 or op==0:
        print('----------------------------------------------------')
        print('Escoja una opcion')
        print('1. Configurar simulación')
        print('2. Simular')
        print('3. Imprimir resultados')
        op=int(input())
        if(op==1):
            config_parametro()
        if(op==2):
            for i in range(1000):
                print('-----------------------------------------------------')
                pos=random.choice(posiciones_ballet)
                cont_pos1000.append(pos)
                print('La bailarina principal hará un plié en la posicion: ', pos)
                if(pos%2==0):
                    print('La bailarina secundaria hará un: ',pasos_ballet[0])
                else:
                    print('La bailarina secundaria hará un: ',pasos_ballet[-1])
            for i in range(5000):
                print('-----------------------------------------------------')
                pos=random.choice(posiciones_ballet)
                cont_pos5000.append(pos)
                print('La bailarina principal hará un plié en la posicion: ', pos)
                if(pos%2==0):
                    print('La bailarina secundaria hará un: ',pasos_ballet[0])
                else:
                    print('La bailarina secundaria hará un: ',pasos_ballet[-1])
            for i in range(10000):
                print('-----------------------------------------------------')
                pos=random.choice(posiciones_ballet)
                cont_pos10000.append(pos)
                print('La bailarina principal hará un plié en la posicion: ', pos)
                if(pos%2==0):
                    print('La bailarina secundaria hará un: ',pasos_ballet[0])
                else:
                    print('La bailarina secundaria hará un: ',pasos_ballet[-1])
            for i in range(100000):
                print('-----------------------------------------------------')
                pos=random.choice(posiciones_ballet)
                cont_pos100000.append(pos)
                print('La bailarina principal hará un plié en la posicion: ', pos)
                if(pos%2==0):
                    print('La bailarina secundaria hará un: ',pasos_ballet[0])
                else:
                    print('La bailarina secundaria hará un: ',pasos_ballet[-1])
    return cont_pos1000,cont_pos5000,cont_pos10000,cont_pos100000

def resultados_simulacion(cont_pos):
    frec_pos_par=0
    frec_pos_impar=0
    frec_paso_releve=0
    frec_paso_retire=0
    prob_salida_paso1=0
    prob_salida_paso2=0
    for i in range(len(cont_pos)):
        if cont_pos[i]%2==0:
            frec_pos_par=frec_pos_par+1
            frec_paso_retire=frec_paso_retire+1
        else:
            frec_pos_impar=frec_pos_impar+1
            frec_paso_releve=frec_paso_releve+1
    prob_salida_paso1=Fraction(frec_pos_par/len(cont_pos)).limit_denominator()
    prob_salida_paso2=Fraction(frec_pos_impar/len(cont_pos)).limit_denominator()
    array_prob=[prob_salida_paso1,prob_salida_paso2]
    suma_prob=sum(array_prob)
    array_prob.append(suma_prob)
    array_resultados=[frec_paso_retire,frec_paso_releve]
    suma_result=sum(array_resultados)
    array_resultados.append(suma_result)
    index=pd.DataFrame(['Retiré','Relevé','total'],columns=['Salidas'])
    resultado_salidas=pd.DataFrame(array_resultados,columns=['Frecuencia'])
    resultado_prob=pd.DataFrame(array_prob,columns=['Probabilidad'])
    resultado_total=pd.concat([index,resultado_salidas,resultado_prob],axis=1)
    if len(cont_pos)==1000:
        resultado_total.to_csv('./Resultados/simulacion_1000.csv')
    elif len(cont_pos)==5000:
        resultado_total.to_csv('./Resultados/simulacion_5000.csv')
    elif len(cont_pos)==10000:
        resultado_total.to_csv('./Resultados/simulacion_10000.csv')
    else:
        resultado_total.to_csv('./Resultados/simulacion_100000.csv')
    grafica_pasos=plt.bar(['Retiré','Relevé'],[frec_paso_retire,frec_paso_releve])
    plt.title('Pasos de ballet')
    plt.xlabel('Salidas')
    plt.ylabel('Frecuencia')
    plt.show()

per=permutaciones_bailarinas()
cont_pos1000,cont_pos5000,cont_pos10000,cont_pos100000=empirico()
conf=equipo_bailarinas(per)
df_subjetivo1, array=probabilidad_subjetiva_tabla1(tabla_fases(),conf)

#tkinter
raiz=tk.Tk()
raiz.title('Bailarinas de Ballet')
raiz.geometry('1300x680')
raiz.pack_propagate(False)
raiz.config(bg='white',width=1300,height=680)
def run():
    df_salida=probabilidad_clasica(tabla_fases(),conf)
    label1=tk.Label(raiz,text='Proyecto probabilidad: Bailarinas de ballet',font=(200))
    label1.place(x=450,y=40)
    label2=tk.Label(raiz,text='Permutaciones: '+str(per),font=(50))
    label2.place(x=50,y=150)
    label7=tk.Label(raiz,text='Configuraciones totales: '+str(conf),font=(50))
    label7.place(x=300,y=150)
    label4=tk.Label(raiz,text='Probabilidad Clásica',font=(50))
    label4.place(x=50,y=270)
    table2 = Text(raiz)
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
    table5.insert(INSERT,probabilidad_subjetiva_tabla2(array, tabla_fases(),conf).to_string())
    table5.place(x=500, y=500,height=150, width=750)
    label6=tk.Label(raiz,text='Resultados de simulación',font=(200))
    label6.place(x=880,y=150)
    tk.Button(raiz, text="Resultado de simulacion 1000", command=lambda:resultados_simulacion(cont_pos1000)).place(x=930,y=200)
    tk.Button(raiz, text="Resultado de simulacion 5000", command=lambda:resultados_simulacion(cont_pos5000)).place(x=930,y=250)
    tk.Button(raiz, text="Resultado de simulacion 10,000", command=lambda:resultados_simulacion(cont_pos10000)).place(x=930,y=300)
    tk.Button(raiz, text="Resultado de simulacion 100,000", command=lambda:resultados_simulacion(cont_pos100000)).place(x=930,y=350)
print('Imprimiendo probabilidades...')
run()
raiz.mainloop()