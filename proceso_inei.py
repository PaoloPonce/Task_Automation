# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 10:41:59 2021

@author: ppa16
"""

import pandas as pd

file1 = "https://www.inei.gob.pe/media/MenuRecursivo/indices_tematicos/01_indice-precios_al_consumidor-lm_1.xlsx"
nombre1 = "Lima Metropolitana"
file2 = "https://www.inei.gob.pe/media/MenuRecursivo/indices_tematicos/02_indice-precios_al_consumidor-nivel_nacional_1.xlsx"
nombre2 = "Nacional"

def proceso_inei(enlace,saltar_ren,columnas,indicador):
    
    df = pd.read_excel(enlace, skiprows=saltar_ren,usecols=range(0,columnas))
    year_unicos = [str(e).split('.')[0] for e in df['Año'].unique().tolist() if e==e]
    
    year_columna = []
    for y in year_unicos:
        year_columna = year_columna+[y]*12
    
    df['Year'] = year_columna

    meses2n = {'Enero':'01', 'Febrero':'02', 'Marzo':'03', 'Abril':'04', 'Mayo':'05', 'Junio':'06',
               'Julio':'07', 'Agosto':'08', 'Setiembre':'09', 'Octubre':'10', 'Noviembre':'11', 'Diciembre':'12'}
    df['Mes'] = df['Mes'].map(meses2n)
    
    df['Fecha'] = '01-'+(df.Mes)+'-'+df.Year
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d-%m-%Y")
    df.drop(columns=['Año'],inplace=True)
    df = df[df.Fecha>"2011-12-01"]
    df['Indicador'] = indicador
    df = df[['Mensual','Fecha','Indicador']]    

    return df

db1 = proceso_inei(enlace=file1,saltar_ren=3,columnas=6,indicador=nombre1)
db2 = proceso_inei(enlace=file2,saltar_ren=3,columnas=6,indicador=nombre2)

db = pd.concat([db1,db2])

ruta = "D:/MTC_OGPPOE/04_Actividades/04_Automatizacion/01_Automatizacion_Josue"
db.to_excel(ruta+"/db_inei.xlsx")    
    
