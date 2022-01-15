# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 12:06:48 2021

@author: ppa16
"""
import pandas
import requests
import os
import pandas as pd
from io import StringIO

os.chdir("D:/MTC_OGPPOE/04_Actividades/04_Automatizacion/01_Automatizacion_J")


def proceso_bcrp(cod_serie,periodo="/2005-1/2021-07"):
    
    url_base="https://estadisticas.bcrp.gob.pe/estadisticas/series/api/"
    cod_ser=cod_serie
    formato="/csv"
    per=periodo
    url=url_base+cod_ser+formato+per
    
    response=requests.get(url)
    plain_txt = (response.text).replace('<br>',"\n")
    
    # db
    df = pd.read_csv(StringIO(plain_txt))
    indicador = df.columns.tolist()[1]
    df.columns = ['fecha_bcrp','Mensual']
    df[['Mes','Year']] = df.fecha_bcrp.str.split(".",expand=True)
    
    meses2n = {'Ene':'01', 'Feb':'02', 'Mar':'03', 'Abr':'04', 'May':'05', 'Jun':'06',
                   'Jul':'07', 'Ago':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dic':'12'}
    df['Mes'] = df['Mes'].map(meses2n)
    
    df['Fecha'] = '01-'+(df.Mes)+'-'+df.Year
    df['Fecha'] = pd.to_datetime(df['Fecha'], format="%d-%m-%Y")
    df.drop(columns=['fecha_bcrp'],inplace=True)
    df = df[df.Fecha>"2011-12-01"]
    df['Indicador'] = indicador
    df = df[['Mensual','Fecha','Indicador']]  
    
    return df

db_test = proceso_bcrp(cod_serie="PN01705BM")