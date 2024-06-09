import pandas as pd
import matplotlib.pyplot as plt
import requests
from zipfile import ZipFile
from io import BytesIO  

#'http://www.dgis.salud.gob.mx/descargas/datosabiertos/muerteMaterna/mortalidad_materna.zip?V=2024.01.16'


#Descargar el archivo zip y extraerlo
url = 'http://www.dgis.salud.gob.mx/descargas/datosabiertos/muerteMaterna/mortalidad_materna.zip?'

r = requests.get(url)
if r.status_code == 200:
    z = ZipFile(BytesIO(r.content))
    z.extractall()
z.extractall()
print(z.namelist())

#Crear el dataframe
df = pd.read_excel('mortalidad_materna_2002_2022.xlsx')

#Seleccionar las columnas de interes
df_interes = df[['ANIO_NACIMIENTO','MES_NACIMIENTO','DIA_NACIMIENTO','EDAD','ENTIDAD_OCURRENCIAD','MUNICIPIO_OCURRENCIAD','ANIO_DEFUNCION','MES_DEFUNCION','DIA_DEFUNCION']]
print(df.columns)

#Crear columna de fecha de nacimiento y de fecha de defunción
#Cuando no se tiene el dato, el conjunto de datos pone 0, entonces los vamos a reemplazar por NA

#NACIMIENTO
df_interes['ANIO_NACIMIENTO']=df_interes['ANIO_NACIMIENTO'].replace(0,pd.NA)
df_interes['MES_NACIMIENTO']=df_interes['MES_NACIMIENTO'].replace(0,pd.NA)
df_interes['DIA_NACIMIENTO']=df_interes['DIA_NACIMIENTO'].replace(0,pd.NA)

df_interes['Fecha_nacimiento']= pd.to_datetime(df_interes[['ANIO_NACIMIENTO','MES_NACIMIENTO','DIA_NACIMIENTO']].rename(
    columns={'ANIO_NACIMIENTO': 'year', 'MES_NACIMIENTO': 'month', 'DIA_NACIMIENTO': 'day'}),errors='coerce')

#DEFUNCION
df_interes['ANIO_DEFUNCION'] = df_interes['ANIO_DEFUNCION'].replace(0, pd.NA)
df_interes['MES_DEFUNCION'] = df_interes['MES_DEFUNCION'].replace(0, pd.NA)
df_interes['DIA_DEFUNCION'] = df_interes['DIA_DEFUNCION'].replace(0, pd.NA)


df_interes['Fecha_defuncion'] = pd.to_datetime(df_interes[['ANIO_DEFUNCION', 'MES_DEFUNCION', 'DIA_DEFUNCION']].rename(
    columns={'ANIO_DEFUNCION': 'year', 'MES_DEFUNCION': 'month', 'DIA_DEFUNCION': 'day'}), errors='coerce')

#El dataframe con timestamps

df_actualizada = df_interes[['Fecha_nacimiento','EDAD','ENTIDAD_OCURRENCIAD','MUNICIPIO_OCURRENCIAD','Fecha_defuncion']]
print(df_actualizada.head(5))
print(df_actualizada.describe())

############################################################################################################################

#¿Cuantas menores de edad murieron?
#El dataframe de mujeres menores de 18 años
df_menores_18 = df_actualizada[df_actualizada['EDAD']<18]

#Por el tamaño de este, murieron al menos 1341
print(df_menores_18.shape)

#La menor más pequeña tenia 11 años
print(df_menores_18['EDAD'].min())

###########################################################################################################################

#Calcular el número de muertes maternas por año en hmo

df_hmo = df_actualizada[df_actualizada['MUNICIPIO_OCURRENCIAD']=='HERMOSILLO']
df_hmo_anio = df_hmo.groupby(df_hmo['Fecha_defuncion'].dt.year)['Fecha_defuncion']
df_hmo_anio = df_hmo.groupby(df_hmo['Fecha_defuncion'].dt.year)['Fecha_defuncion'].count().reset_index(name='count')
print(df_hmo_anio.head(2))


with plt.style.context(('ggplot')):
    plt.bar(df_hmo_anio['Fecha_defuncion'], df_hmo_anio['count'], color='blue')
    plt.xlabel('Año')
    plt.ylabel('Muertes')
    plt.title('Muertes maternas por año en hmo (2002-2022)')
    plt.show()
#Los años con más muertes maternas en hmo tienen 13 muertes

#############################################################################################################################

df_hmo_2020 = df_hmo[df_hmo['Fecha_defuncion'].dt.year == 2020]



