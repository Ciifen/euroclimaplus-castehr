"""
This file allow to run the index cumpoute from aone estation,
form all thsi index are requiere mounthly meteological data
@ 2020
"""
import pandas as pd
import calendar
from datetime import datetime
from util import convert
import eto.computeETP as etp
import eto.thornthwaite as th
### main file to run.
#### run climate index
## cumpute eto


#### read example set from csv archive.
####read stations file
stations = pd.read_csv("/home/darwin/Documentos/Desarrollo/PythonProyects/indicesequia/datasets/stations.csv")
print(stations)
print(stations['nombre'])
      ## read file with needed data
### run pennman method
dataset = pd.read_csv("/home/darwin/Documentos/Desarrollo/PythonProyects/indicesequia/datasets/M0001_temp.csv")
"""Firts we need to iterate from all dataset and compute by each value de etp"""
dataset['fecha'] = pd.to_datetime(dataset['fecha'],dayfirst=False,yearfirst=True) ### convert to date
#dataset['fecha2'] = dataset['fecha'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
#print(dataset.head(5))
###### constantes para calculos diarios
"""day of year base on fecha  field"""

dataset['doy'] = dataset['fecha'].apply(lambda x: x.timetuple().tm_yday)
psychrometer = 1 ## allows values  1: ventilated, 2: natural ventilated psychrometer 3. non ventilated
latitude = stations['latitud'][0]
altitude = stations['altitud'][0]
albedo = 0.23 #
shf = 0.0 ### form daily values if you need mounthly values use monthly_soil_heat_flux2 function
#print(dataset.columns)

print("----- ** ETP PENMAN MONTEITH ** -----")
vec=[]
for x in range(0,len(dataset['fecha'])):
     #print(dataset['fecha'][x])
     etppm = etp.penman_monteith_daily_rtvh(dataset['tmn'][x], dataset['tmx'][x],
                                                        dataset['tmd'][x], dataset['vv'][x],
                                                        dataset['hf'][x],dataset['doy'][x],
                                                        psychrometer,latitude,altitude,
                                                        albedo,shf)
     #print(etppm)
     vec.append(etppm)
dataset['ETP_PM(mm/day)'] = pd.Series(vec)
print(dataset.head(10))
print("----- ** ETP HARGREAVES ** -----")
vec=[]
for x in range(0,len(dataset['fecha'])):
     #print(dataset['fecha'][x])
     etphar = etp.hargraves_daily_rtvh(dataset['tmn'][x], dataset['tmx'][x],
                                                        dataset['tmd'][x],latitude,dataset['doy'][x])
     #print(etppm)
     vec.append(etphar)
dataset['ETP_HAR(mm/day)'] = pd.Series(vec)
print(dataset.head(10))

print("----- ** ETP THORNTHWAITE ** -----")
### need compute mounthly data from daily
estacion = dataset["estacion"][0]
dataset['yearMounth']= dataset['fecha'].apply(lambda x: datetime.strptime(datetime.strftime(x,'%Y-%m-01'),'%Y-%m-%d'))
#meses = dataset.groupby(by='yearMounth')['yearMounth'].nunique()
meses = dataset['yearMounth'].drop_duplicates()

print("Mansualizando..")
list_rows = []
for r in meses:
    mes = dataset[dataset['yearMounth'] == r]
    days_month =  calendar._monthlen(r.year,r.month)
    list_rows.append( {'estacion': estacion, 'fecha' : r, 'rr':mes['rr'].sum(),
            'tmx':round(mes['tmx'].mean(),ndigits=1), 'tmn':round(mes['tmn'].mean(),ndigits=1),
            'tmd':round(mes['tmd'].mean(),ndigits=1),
           'hf':round(mes['hf'].mean(),ndigits=2), 'vv':round(mes['vv'].mean(),ndigits=2),
            'ETP_PM(mm/mes)':round((mes['ETP_PM(mm/day)'].mean()*days_month),ndigits=3),
                       'ETP_HAR(mm/mes)':round((mes['ETP_HAR(mm/day)'].mean()*days_month),ndigits=3)})
mDataset = pd.DataFrame(list_rows)
mDataset['year'] = mDataset['fecha'].apply(lambda x: int(datetime.strftime(x,'%Y')))

lye=mDataset['year'].drop_duplicates()
## run thorwait method
tho = []
for y in lye:
    dya = mDataset[mDataset['year']==y]
    etp_th = th.thornthwaite(dya['tmd'],dya['hf'])
    print(y)
    print(etp_th)
    tho.extend(etp_th)
mDataset=mDataset.drop(['year'], axis=1)
mDataset['ETP_THO(mm/mes)'] = pd.Series(tho).round(3)
print(mDataset.head(5))
dataset.to_csv("/home/darwin/Documentos/Desarrollo/PythonProyects/indicesequia/datasets/"+str(estacion)+"_daily_etp.csv",header=True,index=False)
mDataset.to_csv("/home/darwin/Documentos/Desarrollo/PythonProyects/indicesequia/datasets/"+str(estacion)+"_Mounthly_etp.csv",header=True,index=False)