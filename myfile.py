# -- coding: utf-8 --
"""myfile

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15e-V4gddIhN9kVunjOiHNkcsxjzHTuap
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Huellas de la deforestación')
st.header("Rastreando el impacto de la pérdida forestal en Perú a travez del tiempo")
st.write('La deforestación en Perú es un fenómeno alarmante que ha capturado la atención de ambientalistas, científicos y gobiernos por igual. Este país, hogar de una de las partes más ricas en biodiversidad del planeta, enfrenta una creciente amenaza debido a la tala indiscriminada de bosques, impulsada por actividades como la minería y la expansión urbana. En este caso, analizaremos un registro de monitoreo de la Deforestación en el ámbito de las Áreas Naturales, para dar conocimiento especificos sobre ello y generar un análisis.')
st.write("El Registro de Monitoreo de la Deforestación en el ámbito de las Áreas Naturales Protegidas es una herramienta fundamental gestionada por el Servicio Nacional de Áreas Naturales Protegidas por el Estado (SERNANP) en Perú. Este organismo, adscrito al Ministerio del Ambiente, tiene como misión asegurar la conservación de las áreas protegidas del país, así como la diversidad biológica y el mantenimiento de sus servicios ambientales. A través de sistemas de información geográfica y técnicas de monitoreo biológico, SERNANP recopila y analiza datos sobre la deforestación y otros cambios en el uso del suelo dentro de estas áreas. Este registro no solo permite identificar las tendencias de pérdida de cobertura forestal, sino que también facilita la implementación de estrategias de conservación y gestión sostenible, contribuyendo así a la protección de los ecosistemas y a la mitigación de los efectos del cambio climático. La información obtenida es crucial para la toma de decisiones informadas y para el foralecimiento de las políticas ambientales en el país.")
st.write("De tal forma, nos enfocaremos en el monitoreo de la deforestación dentro de las Áreas Naturales Protegidas. Examinaremos datos generales que ilustran la tasa de deforestación y las tendencias a lo largo del tiempo, así como las implicancias de estas pérdidas en la conservación de la biodiversidad.")

archivo = "Dataset_DeforestacionAnp_SERNANP.csv"
data = pd.read_csv(archivo)

# Mostrar los datos
st.write("Vista previa de los datos:")
st.dataframe(data)

# Función para filtrar y procesar los datos por año
def procesar_datos_por_anio(data, anio):
    datos_anio = data[data['ANIO_REPORTE'] == anio]
    area_por_mes = datos_anio.groupby('MES_IMAG')['AREA_DEFO'].sum().reset_index()
    area_por_mes = area_por_mes.sort_values(by='MES_IMAG')  
    return area_por_mes, datos_anio 

# Filtrar y procesar datos para 2022 y 2023
data_2022, datos_filtrados_2022 = procesar_datos_por_anio(data, 2022)
data_2023, datos_filtrados_2023 = procesar_datos_por_anio(data, 2023)

# Lista de número de mes a nombres 
meses = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

# Combo box (año)
seleccion_anio = st.selectbox("Selecciona el año para mostrar el gráfico", [2022, 2023])

# Función: mostrar gráficos y tablas

if seleccion_anio == 2022:
    # Reemplazar números de meses por nombres
    data_2022['MES_NOMBRE'] = data_2022['MES_IMAG'].map(meses)

    # Gráfico de área deforestada en 2022
    st.write("Gráfico del área deforestada por mes en 2022:")
    fig1, ax1 = plt.subplots()
    ax1.plot(data_2022['MES_NOMBRE'], data_2022['AREA_DEFO'], marker='o', linestyle='-', color='green')
    ax1.set_title('Área deforestada por mes en 2022')
    ax1.set_xlabel('Mes')
    ax1.set_ylabel('Área Deforestada (ha)')
    ax1.grid(True)
    plt.xticks(rotation=45) 
    st.pyplot(fig1)

    # Tabla MES_IMAG, ANIO_REPORTE y AREA_DEFO
    datos_filtrados_2022 = datos_filtrados_2022[['MES_IMAG', 'ANIO_REPORTE', 'AREA_DEFO']]
    st.write("Datos filtrados para el año 2022:")
    st.dataframe(datos_filtrados_2022)  

elif seleccion_anio == 2023:

    # De número a mes
    data_2023['MES_NOMBRE'] = data_2023['MES_IMAG'].map(meses)

    # Gráfico de área deforestada en 2023
    st.write("Gráfico del área deforestada por mes en 2023:")
    fig2, ax2 = plt.subplots()
    ax2.plot(data_2023['MES_NOMBRE'], data_2023['AREA_DEFO'], marker='o', linestyle='-', color='blue')

    ax2.set_title('Área deforestada por mes en 2023')
    ax2.set_xlabel('Mes')
    ax2.set_ylabel('Área Deforestada (ha)')
    ax2.grid(True) # Cuadrícula

    plt.xticks(rotation=45)  
    st.pyplot(fig2)

    # Tabla MES_IMAG, ANIO_REPORTE y AREA_DEFO
    datos_filtrados_2023 = datos_filtrados_2023[['MES_IMAG', 'ANIO_REPORTE', 'AREA_DEFO']]
    st.write("Datos filtrados para el año 2023:")
    st.dataframe(datos_filtrados_2023)
    

# Gráfico de pastel para causa de deforestación

st.write("Causa de la deforestación")

area_causa = data.groupby('DEFO_CAUSA')['AREA_DEFO'].sum().reset_index()
area_causa = area_causa.sort_values('AREA_DEFO', ascending=False)  # Ordenar por área

# Colores 
colores = plt.cm.Paired(range(len(area_causa)))

fig3, ax3 = plt.subplots()

# Gráfico de pastel
ax3.pie(area_causa['AREA_DEFO'], labels=area_causa['DEFO_CAUSA'], autopct='%1.1f%%', startangle=90, colors=colores, wedgeprops={'edgecolor': 'black'})
ax3.axis('equal')  

# Leyenda
ax3.legend(area_causa['DEFO_CAUSA'], title="Causas de la deforestación", bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig3)

# Tabla DEFO_CAUSA
st.write("Datos de causa de deforestación y área deforestada:")
st.dataframe(area_causa)


# Gráfico de barras horizontales para zonificación
st.write("Distribución de la deforestación por zonificación en el Área Natural Protegida (ANP)")

area_zonificacion = data.groupby("ZONIFI_ANP")['AREA_DEFO'].sum().reset_index()

area_zonificacion = area_zonificacion.sort_values('AREA_DEFO', ascending=True)

#  gráfico
fig4, ax4 = plt.subplots(figsize=(8, 6))
ax4.barh(area_zonificacion['ZONIFI_ANP'], area_zonificacion['AREA_DEFO'], color='teal')
ax4.set_title('Área deforestada por zonificación', fontsize=16)
ax4.set_xlabel('Área deforestada (km²)', fontsize=12)
ax4.set_ylabel('Zonificación ANP', fontsize=12)
ax4.grid(axis='x', linestyle='--', alpha=0.7)

st.pyplot(fig4)

area_zonificacion_renombrada = area_zonificacion[['ZONIFI_ANP', 'AREA_DEFO_KM2']].rename(columns={
    'ZONIFI_ANP': 'Zonificación ANP',
    'AREA_DEFO_KM2': 'Área deforestada (km²)'
})

# Mostrar tabla 
st.write("Datos de área deforestada por zonificación:")
st.dataframe(area_zonificacion_renombrada)
