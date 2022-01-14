# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 14:01:07 2021

@author: ppa16
"""

## Libraries
import pandas as pd
import ftplib
import os
import time
import datetime
import numpy as np
import re
import shutil


### Working directory ###
origen = "D:\\MTC_OGPPOE\\04_Actividades\\04_Automatizacion\\00_Automatizacion_FTP\\ftp_ps"
#os.getcwd()
os.chdir(origen)
os.listdir()

#%% descargar

### Connection ###
# FTP host
FTP_host = "####"

# create an instance FTP
FTP = ftplib.FTP()

# connect
FTP.connect(FTP_host)
FTP.login('usuario', 'clave')

# current directory
files_ftp = []
FTP.dir(files_ftp.append)
md_files = []
for file in files_ftp:
    md_files.append((file[29:].strip().split(' ')))

md_files = pd.DataFrame(md_files)
md_files.columns = ['weight','mes', 'dia', 'hora','file']
md_files['dia'] = md_files['dia'].astype(int)

### Parametros para filtrar los actualizados
param_month = datetime.datetime.now().strftime("%b")
#param_month = 'May'
param_day = datetime.datetime.now().day
#param_day = 31

# crear estado
md_files['estado'] = np.where(((md_files.mes == param_month) & (md_files.dia == param_day)),'actualizado','no actualizado')

# filtramos los archivos que están actualizados
download_list = md_files[md_files['estado']=='actualizado']

# cambiar tipo de variable
download_list['weight'] = download_list.weight.astype(float)

## Ordenamos de menor peso a mayor peso
download_list = download_list.sort_values(['weight'])

# descargar
loop_time = time.time()
for file in list(download_list.file):
    start_time = time.time()
    print("Downloading..." + file)
    ####Carga del archivo
    with open(file, 'wb') as fp:
        FTP.retrbinary('RETR '+ file, fp.write)
    total_time = time.time() - start_time
    print('Tiempo descarga:', total_time/60, 'minutes')

total_loop_time = time.time() - loop_time
print('Tiempo descarga Total:', total_loop_time /60, 'minutes')

FTP.quit()

#%% eliminar

files = os.listdir()

lista = ["mtc_pia_pim.csv",
         "mtc_certificado.csv",
         "mtc_ejecucion.csv",
         "mtc_gasto.csv",
         "mtc_gasto_2.csv",
         "mtc_meta_fisica.csv",
         "mtc_gasto_2_mes.csv",
         "mtc_meta_fisica_mes.csv",
         "mtc_ingreso.csv",
         "mtc_ingreso_mes.csv",
         "mtc_registra_plaza.csv",
         "mtc_remunera_plaza.csv",
         "mtc_notas_modificatorias.zip",
         "mtc_formato12b.csv",
         "mtc_proyecto_inv.csv",
         "mtc_estado_situacion.csv",
         "mtc_proceso_seleccion.csv"]

listarutas=[".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\1. Gastos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\2. Ingresos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\2. Ingresos",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\3. AIRHSP",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\3. AIRHSP",
            ".\\Automatizacion\\1. SIAF_AIRHSP\\5. Notas Modificatorias",
            ".\\Automatizacion\\2. INVERSIONES\\1. Formato 12B",
            ".\\Automatizacion\\2. INVERSIONES\\2. Inversiones_detalle",
            ".\\Automatizacion\\2. INVERSIONES\\2. Inversiones_detalle",
            ".\\Automatizacion\\2. INVERSIONES\\2. Inversiones_detalle"]
ubicaciones = dict(zip(lista, listarutas))

# delete old files:
for file in files:
    sep_archivo = file.split('.')
    arch_destino = os.listdir(ubicaciones[file])
    arch_delete  = [e for e in arch_destino if bool(re.search(sep_archivo[0]+'_\d{4}',e))]
    for arch in arch_delete:
        os.remove(ubicaciones[file]+'\\'+arch)


#%% renombrar

files = os.listdir()
tiempo_real = datetime.datetime.now()
tiempo_ftp1 = tiempo_real- datetime.timedelta(hours=24, minutes=0)
fecha_real = str(tiempo_ftp1.day).zfill(2)+str(tiempo_ftp1.month).zfill(2)+str(tiempo_ftp1.year)

pre = ['1. ','2. ','3. ','4. ','5. ','6. ','7. ','8. ','1. ','2. ','1. ','2. ', '1. ','1 . ', '1. ','2. ','3. ']
pre = dict(zip(lista, pre))

for file in files:    
    sep_archivo = file.split('.')
    nuevo = pre[file]+sep_archivo[0]+'_'+fecha_real+'.'+sep_archivo[1]
    os.rename(file,nuevo)
    
#%% traslado

files = os.listdir()
for file in files:
    sep_archivo = file.split('.')
    clave = re.search(r"(?<=^).*?(?=_\d{8})", sep_archivo[1].strip()).group(0)+'.'+sep_archivo[2]
    shutil.move(origen+'\\'+file,ubicaciones[clave])