 # -- coding: utf-8 --
"""myfile

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15e-V4gddIhN9kVunjOiHNkcsxjzHTuap
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuración de la página de Streamlit
st.set_page_config(page_title="Deforestación en Áreas Naturales Protegidas", page_icon="🌳", initial_sidebar_state="expanded", layout='wide')

# Cargar datos
archivo = "Dataset_DeforestacionAnp_SERNANP.csv"
data = pd.read_csv(archivo)

# Configuración del menú
with st.sidebar:
    menu = option_menu(
        menu_title="Menú Principal",
        options=["Inicio", "Deforestación por año", "Causas de Deforestación", "Comparativo", "Zonificación", "Área Deforestada por ANP", "Conoce más"],
        icons=["house", "calendar-alt", "pie-chart", "bar-chart", "map", "globe", "info-circle"],
        menu_icon="menu-app",
        default_index=0
    )

# Sección: Inicio
if menu == "Inicio":
    st.title('Huellas de la deforestación')
    st.header("Rastreando el impacto de la pérdida forestal en Perú a través del tiempo")
    st.image("https://raw.githubusercontent.com/mcamilaa/streamlit_app/main/imagenes/defo_1.jpg", caption="Deforestación en áreas protegidas", use_column_width=False)
    st.write('La deforestación en Perú es un fenómeno alarmante que ha capturado la atención de ambientalistas, científicos y gobiernos por igual. Este país, hogar de una de las partes más ricas en biodiversidad del planeta, enfrenta una creciente amenaza debido a la tala indiscriminada de bosques, impulsada por actividades como la minería y la expansión urbana. En este caso, analizaremos un registro de monitoreo de la Deforestación en el ámbito de las Áreas Naturales, para dar conocimiento especificos sobre ello y generar un análisis.')
    st.write("El Registro de Monitoreo de la Deforestación en el ámbito de las Áreas Naturales Protegidas es una herramienta fundamental gestionada por el Servicio Nacional de Áreas Naturales Protegidas por el Estado (SERNANP) en Perú. Este organismo, adscrito al Ministerio del Ambiente, tiene como misión asegurar la conservación de las áreas protegidas del país, así como la diversidad biológica y el mantenimiento de sus servicios ambientales. A través de sistemas de información geográfica y técnicas de monitoreo biológico, SERNANP recopila y analiza datos sobre la deforestación y otros cambios en el uso del suelo dentro de estas áreas. Este registro no solo permite identificar las tendencias de pérdida de cobertura forestal, sino que también facilita la implementación de estrategias de conservación y gestión sostenible, contribuyendo así a la protección de los ecosistemas y a la mitigación de los efectos del cambio climático. La información obtenida es crucial para la toma de decisiones informadas y para el foralecimiento de las políticas ambientales en el país.")
    st.write("De tal forma, nos enfocaremos en el monitoreo de la deforestación dentro de las Áreas Naturales Protegidas. Examinaremos datos generales que ilustran la tasa de deforestación y las tendencias a lo largo del tiempo, así como las implicancias de estas pérdidas en la conservación de la biodiversidad.")

# Sección: Deforestación por año
if menu == "Deforestación por año":
    st.header("Área deforestada por año")

    # Crear un filtro para seleccionar el año
    years = data['ANIO_REPORTE'].unique()
    selected_year = st.selectbox("Selecciona el año para mostrar el gráfico:", years)

    # Función para procesar y filtrar datos por año
    def procesar_datos_por_anio(data, anio):
        meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
                 7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
        
        # Filtrar datos por año
        datos_anio = data[data['ANIO_REPORTE'] == anio]
        
        # Verifica si hay datos después del filtrado
        if datos_anio.empty:
            st.warning(f"No hay datos para el año seleccionado: {anio}")
            return pd.DataFrame(), pd.DataFrame()

        # Agrupar área deforestada por mes
        area_por_mes = datos_anio.groupby('MES_IMAG')['AREA_DEFO'].sum().reset_index()
        area_por_mes['MES_NOMBRE'] = area_por_mes['MES_IMAG'].map(meses)  # Mapear nombres de los meses
        
        return area_por_mes, datos_anio

    # Procesar datos para el año seleccionado
    data_anio, datos_filtrados = procesar_datos_por_anio(data, selected_year)

    # Verificar si hay datos antes de crear el gráfico
    if not data_anio.empty:
        # Colores para cada año
        color_map = {2021: 'orange', 2022: 'green', 2023: 'blue'}
        selected_color = color_map.get(selected_year, 'gray')

        # Crear gráfico con Plotly
        fig = px.line(data_anio, x='MES_NOMBRE', y='AREA_DEFO', title=f'Área deforestada por mes en {selected_year}')
        fig.update_traces(
            mode='lines+markers',
            marker=dict(symbol='circle', size=8, color=selected_color),
            line=dict(color=selected_color, width=2)
        )
        fig.update_layout(
            title=dict(
                text=f'Área deforestada por mes en {selected_year}',
                font=dict(size=20, color='darkblue')
            ),
            xaxis=dict(
                title='Mes',
                titlefont=dict(size=16, color='darkblue'),
                tickfont=dict(size=14, color='black'),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title='Área Deforestada (ha)',
                titlefont=dict(size=16, color='darkblue'),
                tickfont=dict(size=14, color='black'),
                showgrid=True,
                gridcolor='lightgrey'
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            hovermode='x unified'
        )

        # Mostrar gráfico en Streamlit
        st.plotly_chart(fig)

        # Mostrar tabla de datos filtrados
        datos_filtrados.index = datos_filtrados.index + 1
        st.write(datos_filtrados[['MES_IMAG', 'ANIO_REPORTE', 'AREA_DEFO']])
        st.markdown("*La tabla muestra los datos de deforestación mensuales para el año seleccionado.*")
        st.info("Este gráfico ilustra la cantidad de área deforestada (en hectáreas) por mes en el año seleccionado.")
    else:
        st.warning("No hay datos suficientes para generar el gráfico.")
     

# Sección: Causas de Deforestación (Gráfico Interactivo)
if menu == "Causas de Deforestación":
    st.header("Causas de la Deforestación")
    
    # Agrupación de datos por causa
    area_causa = data.groupby('DEFO_CAUSA')['AREA_DEFO'].sum().reset_index()
    area_causa = area_causa.sort_values('AREA_DEFO', ascending=False)  # Ordenar por área


    # Paleta de colores
    custom_colors = [
     "#6BAED6",  # Azul claro
     "#FDD835",  # Amarillo dorado
     "#A1D490",  # Verde suave
     "#FF6F61",  # Rojo coral
     "#9575CD"   # Morado
    ]

    # Crear gráfico de pastel interactivo con Plotly
    fig = px.pie(
        area_causa,
        values='AREA_DEFO',
        names='DEFO_CAUSA',
        title=' ',
        color_discrete_sequence=custom_colors,
        hole=0.3  # Gráfico de dona
    )
    
    # Personalizar la visualización de etiquetas
    fig.update_traces(
        textinfo='percent+label',
        hoverinfo='label+value+percent',
        textfont_size=14
    )

    # Configuración del diseño
    fig.update_layout(
        legend=dict(
            title='Causas',
            font=dict(size=14),
            bordercolor='lightgrey',
            borderwidth=1
        )
    )

    # Mostrar el gráfico interactivo en Streamlit
    st.plotly_chart(fig)

    # Tabla de datos
    st.write("Datos de causa de deforestación y área deforestada:")
    st.dataframe(area_causa)

    st.markdown(
        """
        **Nota:** Estos datos reflejan las principales causas identificadas en el período de análisis. 
        Es importante considerar medidas específicas para abordar cada factor.
        """
    )
   

# Sección: Comparativo
if menu == "Comparativo":
    st.header("Comparación entre Años")
    promedios = pd.DataFrame({
        "Año": ["2021", "2022", "2023"],
        "Promedio Mensual (ha)": [
            data[data['ANIO_REPORTE'] == 2021]['AREA_DEFO'].mean(),
            data[data['ANIO_REPORTE'] == 2022]['AREA_DEFO'].mean(),
            data[data['ANIO_REPORTE'] == 2023]['AREA_DEFO'].mean()
        ]
    })

    fig, ax = plt.subplots()
    ax.bar(promedios['Año'], promedios['Promedio Mensual (ha)'], color=['orange', 'green', 'blue'])
    ax.set_title('Promedio mensual de área deforestada (2021-2023)')
    ax.set_xlabel('Año')
    ax.set_ylabel('Área Deforestada (ha)')
    st.pyplot(fig)
    st.write(promedios)

# Sección: Zonificación
if menu == "Zonificación":
    st.header("Zonificación de Deforestación")
    area_zonificacion = data.groupby("ZONIFI_ANP")['AREA_DEFO'].sum().reset_index()
    area_zonificacion = area_zonificacion.sort_values('AREA_DEFO', ascending=True)
    
    fig, ax = plt.subplots()
    ax.barh(area_zonificacion['ZONIFI_ANP'], area_zonificacion['AREA_DEFO'], color='teal')
    ax.set_title('Área deforestada por zonificación')
    ax.set_xlabel('Área Deforestada (ha)')
    st.pyplot(fig)
    st.dataframe(area_zonificacion.rename(columns={
        'ZONIFI_ANP': 'Zonificación',
        'AREA_DEFO': 'Área Deforestada (ha)'
    }))

# Sección: Área Deforestada por Categoría de ANP
if menu == "Área Deforestada por ANP":
    st.header("Área Deforestada por Categoría de ANP (2021-2023)")
    
    # Filtrar datos para el periodo 2021-2023
    filtered_data = data[(data["ANIO_REPORTE"] >= 2021) & (data["ANIO_REPORTE"] <= 2023)].copy()

    # Limpieza de la columna "CATEGORIA" (quitar espacios y uniformar formato)
    filtered_data["CATEGORIA"] = filtered_data["CATEGORIA"].str.strip().str.title()

    # Verificar si hay datos después del filtrado
    if filtered_data.empty:
        st.warning("No se encontraron datos para el período 2021-2023.")
    else:
        # Agrupar datos por categoría y ANP, sumando el área deforestada
        sum_area_deforestation = filtered_data.groupby(["CATEGORIA", "ANP"])["AREA_DEFO"].sum().reset_index()

        # Obtener las categorías únicas
        categorias = sum_area_deforestation["CATEGORIA"].unique()

        # Combo box para seleccionar la categoría
        categoria_seleccionada = st.selectbox("Selecciona una categoría", categorias)

        # Filtrar datos por la categoría seleccionada
        categoria_data = sum_area_deforestation[sum_area_deforestation["CATEGORIA"] == categoria_seleccionada]

        # Verificar si hay datos para la categoría seleccionada
        if categoria_data.empty:
            st.warning(f"No hay datos para la categoría: {categoria_seleccionada}")
        else:
            # Crear gráfico de dispersión
            fig = px.scatter(
                categoria_data,
                x="ANP",
                y="AREA_DEFO",
                size="AREA_DEFO",
                color="ANP",
                hover_name="ANP",
                title=f"Área Deforestada (ha) en {categoria_seleccionada} (2021-2023)",
                labels={"ANP": "Área Natural Protegida", "AREA_DEFO": "Área Deforestada (ha)"},
                size_max=60,
                color_discrete_sequence=px.colors.qualitative.Set3
            )

            # Mostrar gráfico en Streamlit
            st.plotly_chart(fig)

        # Mostrar información adicional
        st.markdown(f"*Mostrando datos para la categoría: {categoria_seleccionada}.*")


# Sección: Conoce más
if menu == "Conoce más":
    st.header("¿Cómo ayudo a frenar la deforestación?")
    st.write("¡Conoce a SOSelva!")
    

