# -*- coding: utf-8 -*-
"""
Created on Thu May 27 00:50:05 2021

@author: ppa16
"""

# import modules
import findspark
findspark.init()
import os
from time import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import warnings
warnings.filterwarnings("ignore")

total_time = time()
span_parametro = ["5 minutes","10 minutes","15 minutes", "30 minutes"]

# directorio
path = 'D:\\MTC_OGPPOE\\Tareas\\ModeloSutran\\00_Inputs\\2019-01\\'
os.chdir(path)
files = os.listdir(path)

spark_time = time()
spark = SparkSession.builder.getOrCreate()

count_file=0

for file in files:
    
    count_file+=1
    # import, filter, drop duplicated and sort
    df=spark.read.options(header=False,inferSchema=False,delimiter=',').csv(path+file).select('_c1','_c2','_c3','_c4','_c5','_c6')
    df=df.filter(df['_c2'].rlike("\d\d/\d\d/\d\d\d\d")).dropDuplicates().orderBy(["_c2", "_c1","_c3"], ascending=[True,True,True])
    
    # create columns as datetime and change format to _c4 (velocidad)
    df = df.withColumn('new_date', F.to_timestamp((F.concat(F.col("_c2"), F.lit(" "), F.col("_c3"))),'dd/MM/yyyy HH:mm:ss'))
    df = df.withColumn('_c4',df['_c4'].cast("float"))
    
    for span in span_parametro:

        # reduce by xx minutes and compute velocity sum, and first and last by latitud y longitud
        span_time = time()
        df1 = df.groupBy('_c1', F.window("new_date", span)).agg(F.sum("_c4").alias('velocidad_sum'),
                                                                        F.last("_c5").alias('latitud_fin'),
                                                                        F.last("_c6").alias('longitud_fin'))
        df1 = df1.select('_c1','window.*','velocidad_sum','latitud_fin','longitud_fin').orderBy(['_c1', 'end'], ascending=[True,True])
        ruta = "D:\\MTC_OGPPOE\\Tareas\\ModeloSutran\\Pedido_Reduccion\\"+"file"+str(count_file)+"\\"+span.replace(" ","")
        os.chdir(ruta)
        df1.repartition(1).write.csv(path=ruta, mode="append", header="true")
        del df1
        time_span=time() - span_time
        print("Agrupacion del archivo "+file+" por " + span +"culminada en "+ str(time_span/60)+" minutos")
    
    del df
    
    time_spark=time() - spark_time
    print("Archivo "+file+" culminado en "+ str(time_spark/60)+" minutos")

time_spark=time() - spark_time

spark.stop()

