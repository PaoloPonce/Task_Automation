# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:37:36 2021

@author: ppa16
"""
# librerias
import os
import datetime
from pathlib import Path
import requests
from camelot import utils
import camelot
import pandas as pd
import re

# ruta
os.chdir("D:\\MTC_OGPPOE\\Tareas\\Automatizacion_J")
os.listdir()

# url
s = "https://www.inei.gob.pe/media/MenuRecursivo/boletines/II-informe-tecnico-produccion-nacional-MM-AAAA.pdf"

# dictionario de mese e informes
m2i = {'01':'nov','02':'dic','03':'ene','04':'feb','05':'mar','06':'abr',
       '07':'may','08':'jun','09':'jul','10':'ago','11':'set','12':'oct'}

# fechas
tiempo_real = datetime.datetime.now()-datetime.timedelta(hours=72, minutes=0)
mes_nombre  = m2i[str(tiempo_real.month).zfill(2)]
mes_numero  = str(tiempo_real.month).zfill(2)
year_numero = str(tiempo_real.year)

# reemplazo en el url
s = s.replace("II",mes_numero).replace("MM",mes_nombre).replace("AAAA",year_numero)
s

# descargar pdf
file=re.search(r"(?<=boletines/).*?(?=.pdf)", s).group(0)
filename = Path(file+'.pdf')
response = requests.get(s)
filename.write_bytes(response.content)

# ver dimensiones
#layout, dim = utils.get_page_layout(file)

# scan tabla
tables = camelot.read_pdf(file+'.pdf',pages='1',flavor='stream',table_regions=['100,280,600,100'])
print("Total tables extracted:", tables.n)
print(tables[0].df)

# pasar a dataframe
data=pd.DataFrame(tables[0].df,)
data = data.iloc[1:].reset_index(drop=True)
data.columns=['sector','ponderacion','mar (20-21)','ene-mar (20-21)','Abr 20-Mar 21/Marzo Enero-Marzo Abr 19-Mar 20']
numeric_names = ['ponderacion','mar (20-21)','ene-mar (20-21)','Abr 20-Mar 21/Marzo Enero-Marzo Abr 19-Mar 20']
data.dtypes

# cambiar formato a numericas
def cambiar(x):
    x=x.str.replace(",",".")
    return x
data[numeric_names]=data[numeric_names].apply(cambiar)  

convert_dict = {'ponderacion':float,
                'mar (20-21)':float,
                'ene-mar (20-21)':float,
                'Abr 20-Mar 21/Marzo Enero-Marzo Abr 19-Mar 20':float}  
data = data.astype(convert_dict)

data.to_excel(file+'.xlsx',index=False)