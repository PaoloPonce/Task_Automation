# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 11:11:25 2020

@author: ppa16
"""

#%% import libreries

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import pandas as pd
import PyPDF2
import re

#%% set working directories

origen = 'C:\\Users\\ppa16\\OneDrive\\Escritorio\\Separar_GN'
destino = 'C:\\Users\\ppa16\\OneDrive\\Escritorio\\Separar_GN\\Anexo3'
os.getcwd()
os.chdir(origen)
os.listdir()

#%% process file xlsx with key names

pliegos = pd.read_excel('MaestroPliegos.xlsx')
pliegos['PLIEGO'] = pliegos['PLIEGO'].str.replace('\d+\.', '', regex=True)
pliegos['PLIEGO'] = pliegos['PLIEGO'].str.strip() 
pliegos['PLIEGO'] = pliegos['PLIEGO'].str.replace(' ', '', regex=True)

#%% read pdf

pdf_document = "Anexo 3 - GN UE, Generica10062020.PDF"
pdf = PdfFileReader(pdf_document)

os.chdir(destino)

#%% start process

for k in range(pliegos.shape[0]):
    cuenta = 0
    pdf_writer = PdfFileWriter()
    for page in range(pdf.getNumPages()):
        current_page = pdf.getPage(page)
        
        Text = current_page.extractText()
        Text = Text.replace(" ", "")
        ResSearch = re.search(pliegos.loc[k, "PLIEGO"], Text)
        
        if ResSearch is not None:
            pdf_writer.addPage(current_page)
            cuenta = cuenta + 1
        else:
            next
    if cuenta > 0:
        outputFilename = 'ANEXO 3 '+pliegos.loc[k, "PLIEGO2"]+'.pdf'
        with open(outputFilename, "wb") as out:
            pdf_writer.write(out)
            print("created", outputFilename)
    else:
        next
