# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:47:59 2021

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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pretty_html_table import build_table

#%% Descargar

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
md_files.sort_values(by="estado",inplace=True,ascending=False)

FTP.quit()

#%% Enviar correo

# correo y contraseña
sender_address = 'senderg@gmail.com'
sender_pass = 'clave_Sender'
receivers = "r1@gmail.com,r2@gmail.com,r3@gmail.com,r4@gmail.com,r5@gmail.com"
  
# agregar contenido del mail    
message = MIMEMultipart("alternative", None)

# agregar tabla
message.attach(MIMEText(build_table(md_files, 'blue_light'), 'html'))

# crear marco para el correo
message['From'] = sender_address
message['To'] = receivers
message['Subject'] = "Asunto"  

# crear una sesion smtp para enviar correos
session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login(sender_address, sender_pass)
text = message.as_string()
session.sendmail(sender_address, receivers.split(","), text)
session.quit()
print('Mail Sent')