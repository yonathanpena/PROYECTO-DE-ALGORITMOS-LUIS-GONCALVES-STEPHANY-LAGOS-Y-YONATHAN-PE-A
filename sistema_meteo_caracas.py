import json
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from localidad import Localidad
from municipio import Municipio
from clima_actual import ClimaActual
from consulta_historial import ConsultaHistorial
from clima_historico import ClimaHistorico

class SistemaMeteoCaracas:
    """Clase principal encargada de la lógica del sistema y gestión de datos."""

    def __init__(self, zona_caracas):
        """Args:
                zona_caracas (str): Nombre del archivo JSON que contiene la información geográfica de los municipios y localidades.
        """
        self.zona_caracas = zona_caracas
        self.lista_municipios = []
        self.lista_historial_consultas = []
        self.cargar_datos_json()

    def cargar_datos_json(self):
        """Lee el archivo json zonas_caracas y transforma la información en objetos de las clases Municipio y Localidad."""
        self.lista_municipios = []
        
        try:
            archivo = open(self.zona_caracas, 'r', encoding='utf-8')
            datos = json.load(archivo)
            archivo.close()
            
            for nombre_municipio in datos:
                municipio = Municipio(nombre_municipio)
                lista_locs = datos[nombre_municipio]
                
                for datos_localidad in lista_locs:
                    nombre_loc = datos_localidad.get("localidad")
                    latitud = datos_localidad.get("latitud")
                    longitud = datos_localidad.get("longitud")
                    
                    localidad = Localidad(nombre_loc, latitud, longitud)
                    municipio.agregar_localidad(localidad)
                    
                self.lista_municipios.append(municipio)
                
        except Exception as error:
            print(f"Ocurrió un error al cargar el archivo: {error}")

    def mostrar_reporte_carga(self):
        """Imprime un resumen con los municipios y localidades cargados en el sistema."""
        print("\n\t=== REPORTE DE CARGA DE DATOS ===")
        for municipio in self.lista_municipios:
            municipio.mostrar_datos_municipio()

    def consultar_clima_api(self, localidad):
        """Consulta la API de Open-Meteo y obtiene en tiempo real la temperatura, humedad, velocidad del viento y 
        el código del tiempo, guardándolos como un objeto de la clase ClimaActual."""

        if not localidad.tiene_coordenadas():
            print("La localidad no posee coordenadas válidas.")
            return None

        url = "https://api.open-meteo.com/v1/forecast"
        parametros = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
        }

        try:
            respuesta = requests.get(url, params=parametros)
            
            if respuesta.status_code == 200:
                datos_api = respuesta.json()                 
                
                temperatura = datos_api["current"]["temperature_2m"]
                humedad = datos_api["current"]["relative_humidity_2m"]
                velocidad_viento = datos_api["current"]["wind_speed_10m"]
                codigo_tiempo = datos_api["current"]["weather_code"]

                clima_objeto = ClimaActual(temperatura, humedad, velocidad_viento, codigo_tiempo)

                return clima_objeto
            else:
                print(f"Error al consultar la API. Código HTTP: {respuesta.status_code}")
                return None

        except Exception as error:
            print(f"Error al conectar con la API: {error}")
            return None

    def obtener_descripcion_clima(self, codigo):
        """Traduce el código numérico de estado del tiempo otorgado por la API a una descripción textual comprensible por el usuario."""
        
        tabla_codigos = [
            [0, "Cielo despejado"],
            [1, "Principalmente despejado"],
            [2, "Parcialmente nublado"],
            [3, "Nublado"],
            [45, "Niebla"],
            [48, "Niebla con escarcha"],
            [51, "Llovizna ligera"],
            [53, "Llovizna moderada"],
            [55, "Llovizna intensa"],
            [56, "Llovizna helada ligera"],
            [57, "Llovizna helada intensa"],
            [61, "Lluvia leve"],
            [63, "Lluvia moderada"],
            [65, "Lluvia fuerte"],
            [66, "Lluvia helada leve"],
            [67, "Lluvia helada fuerte"],
            [71, "Nevada leve"],
            [73, "Nevada moderada"],
            [75, "Nevada fuerte"],
            [77, "Granos de nieve"],
            [80, "Lluvia leve"],
            [81, "Lluvia moderada"],
            [82, "Lluvia violenta"],
            [85, "Lluvia de nieve leve"],
            [86, "Lluvia de nieve fuerte"],
            [95, "Tormenta eléctrica leve o moderada"],
            [96, "Tormenta eléctrica con granizo ligero"],
            [99, "Tormenta eléctrica con granizo fuerte"]
        ]

        for elemento in tabla_codigos:
            numero = elemento[0]
            descripcion = elemento[1]
            
            if codigo == numero:
                return descripcion

        return "Estado del tiempo no especificado"   
    
    def registrar_consulta(self, municipio_nombre, localidad_nombre, temperatura):
        """Guarda un registro de la consulta en la lista_historial_consultas de la sesión mediante un objeto ConsultaHistorial."""

        nueva_consulta = ConsultaHistorial(municipio_nombre, localidad_nombre, temperatura)
        self.lista_historial_consultas.append(nueva_consulta)

    def mostrar_detalle_clima(self, municipio_nombre, localidad, clima):
        """Imprime en pantalla los datos del clima actual para una localidad específica."""
        if clima is None:
            print("\nNo se pudieron obtener los datos del clima.")
            return

        self.registrar_consulta(municipio_nombre, localidad.nombre, clima.temperatura)

        descripcion = self.obtener_descripcion_clima(clima.codigo_tiempo)

        print("\n\t=== DETALLES METEOROLÓGICOS ===\n")
        print(f"Municipio:           {municipio_nombre}")
        print(f"Localidad:           {localidad.nombre}")
        print(f"Coordenadas:         Lat: {localidad.latitud} | Lon: {localidad.longitud}")
        print(f"Temperatura actual:  {clima.temperatura} °C")
        print(f"Humedad relativa:    {clima.humedad} %")
        print(f"Velocidad viento:    {clima.velocidad_viento} km/h")
        print(f"Estado del tiempo:   {descripcion}")
        print()
    
    def seleccionar_localidad_menu(self):
        """Método auxiliar para seleccionar un municipio y una localidad con coordenadas."""
        print("\n\t=== SELECCIONE UN MUNICIPIO ===")
        posicion = 1
        for municipio in self.lista_municipios:
            print(f"{posicion}. {municipio.nombre}")
            posicion += 1

        try:
            opcion = int(input("\nIngrese el número del municipio: "))
            indice_municipio = opcion - 1

            if indice_municipio < 0 or indice_municipio >= len(self.lista_municipios):
                print("Número fuera de rango.")
                return None
        except ValueError:
            print("Opción inválida. Debe ingresar un número entero válido.")
            return None

        municipio_seleccionado = self.lista_municipios[indice_municipio]

        lista_localidades_validas = []
        for localidad in municipio_seleccionado.localidades:
            if localidad.tiene_coordenadas():
                lista_localidades_validas.append(localidad)

        if len(lista_localidades_validas) == 0:
            print(f"\nEl municipio {municipio_seleccionado.nombre} no tiene localidades con coordenadas registradas.")
            return None

        print(f"\n\t=== LOCALIDADES DISPONIBLES EN {municipio_seleccionado.nombre.upper()} ===")
        posicion_localidad = 1
        for localidad in lista_localidades_validas:
            print(f"{posicion_localidad}. {localidad.nombre}")
            posicion_localidad += 1

        try:
            opcion_localidad = int(input("\nIngrese el número de la localidad: "))
            indice_localidad = opcion_localidad - 1
            if indice_localidad < 0 or indice_localidad >= len(lista_localidades_validas):
                print("Número fuera de rango.")
                return None
        except ValueError:
            print("Opción inválida. Debe ingresar un número entero válido.")

        return municipio_seleccionado.nombre, lista_localidades_validas[indice_localidad]

    def consultar_por_municipio(self):
        """Permite interactuar con el menú para seleccionar un municipio y una de sus localidades válidas. 
        Una vez elegida la localidad, obtiene sus datos meteorológicos en tiempo real mediante la API y lo imprime en pantalla.
        """
        resultado = self.seleccionar_localidad_menu()
        if resultado is None:
            return

        municipio_nombre, localidad_seleccionada = resultado

        print(f"\nConsultando clima para {localidad_seleccionada.nombre}...")
        clima = self.consultar_clima_api(localidad_seleccionada)
        self.mostrar_detalle_clima(municipio_nombre, localidad_seleccionada, clima)
    
    def consultar_por_busqueda_directa(self):
        """Filtra y busca localidades por coincidencia en el nombre y muestra su clima actual."""
        texto_busqueda = input("\nIngrese el nombre (o parte del nombre) de la localidad: ").strip().lower()

        if texto_busqueda == "":
            print("No ingresó ningún texto.")
            return

        lista_coincidencias = []

        for municipio in self.lista_municipios:
            for localidad in municipio.localidades:
                if texto_busqueda in localidad.nombre.lower() and localidad.tiene_coordenadas():
                    lista_coincidencias.append((municipio.nombre, localidad))

        if len(lista_coincidencias) == 0:
            print(f"\nNo se encontraron localidades válidas que coincidan con \"{texto_busqueda}\".")
            return

        print(f"\n\t=== RESULTADOS DE LA BÚSQUEDA ===")
        posicion = 1
        for item in lista_coincidencias:
            municipio_nombre = item[0]
            localidad_objeto = item[1]
            print(f"{posicion}. {localidad_objeto.nombre} (Municipio: {municipio_nombre})")
            posicion += 1

        try:
            opcion = int(input("\nSeleccione el número de la localidad deseada: "))
            indice = opcion - 1

            if indice < 0 or indice >= len(lista_coincidencias):
                print("Número fuera de rango.")
                return
        except ValueError:
            print("Opción inválida. Debe ingresar un número entero válido.")
            return

        municipio_seleccionado, localidad_seleccionada = lista_coincidencias[indice]

        clima = self.consultar_clima_api(localidad_seleccionada)
        self.mostrar_detalle_clima(municipio_seleccionado, localidad_seleccionada, clima)

    def ejecutar_menu_consulta_tiempo_real(self):
        """Despliega un submenú interactivo para consultar el clima en tiempo real por municipio o búsqueda directa."""
        while True:
            try:
                print("\n\t=== ¿CÓMO DESEA CONSULTAR EL CLIMA? ===")
                print("1. Por Municipio y Localidad")
                print("2. Por Búsqueda Directa (Nombre)")
                print("3. Volver al menú principal")

                sub_opcion = int(input("\nElija una opción (1-3): "))

                if sub_opcion == 1:
                    self.consultar_por_municipio()
                elif sub_opcion == 2:
                    self.consultar_por_busqueda_directa()
                elif sub_opcion == 3:
                    break
                else:
                    print("\nOpción no válida.")

            except Exception as error:
                print(f"\nEntrada o proceso inválido: {error}")

    def mostrar_ranking_temperatura(self):
        """Muestra la localidad más cálida y más fría consultadas en la sesión."""
        if len(self.lista_historial_consultas) == 0:
            print("\nAún no se ha realizado ninguna consulta en esta sesión.")
            return

        localidad_mas_calida = self.lista_historial_consultas[0]
        localidad_mas_fria = self.lista_historial_consultas[0]

        for consulta in self.lista_historial_consultas:
            if consulta.temperatura > localidad_mas_calida.temperatura:
                localidad_mas_calida = consulta
            
            if consulta.temperatura < localidad_mas_fria.temperatura:
                localidad_mas_fria = consulta

        print("\n\t=== RANKING DE TEMPERATURA ===")
        print(f"Localidad más cálida: {localidad_mas_calida.localidad_nombre} ({localidad_mas_calida.municipio_nombre}) con {localidad_mas_calida.temperatura} °C")
        print(f"Localidad más fría: {localidad_mas_fria.localidad_nombre} ({localidad_mas_fria.municipio_nombre}) con {localidad_mas_fria.temperatura} °C")

    def mostrar_cobertura_geografica(self):
        """Muestra las localidades sin coordenadas agrupadas por municipio."""
        print("\n\t=== COBERTURA GEOGRÁFICA (LOCALIDADES SIN COORDENADAS) ===")
        
        for municipio in self.lista_municipios:
            print(f"\nMunicipio: {municipio.nombre}")
            contador_sin_coordenadas = 0
            
            for localidad in municipio.localidades:
                if not localidad.tiene_coordenadas():
                    print(f" - {localidad.nombre}")
                    contador_sin_coordenadas += 1
            
            if contador_sin_coordenadas == 0:
                print("Todas las localidades tienen coordenadas registradas")
    
    def mostrar_promedio_general(self):
        """Calcula y muestra el promedio de temperatura de las localidades consultadas utilizando un arreglo NumPy."""
        if len(self.lista_historial_consultas) == 0:
            print("\nAún no se ha realizado ninguna consulta en esta sesión.")
            return

        lista_temperaturas = []
        for consulta in self.lista_historial_consultas:
            lista_temperaturas.append(consulta.temperatura)

        array_temperaturas = np.array(lista_temperaturas)
        promedio = np.mean(array_temperaturas)

        print("\n\t=== PROMEDIO GENERAL DE LA SESIÓN ===")
        print(f"Total de consultas realizadas: {len(lista_temperaturas)}")
        print(f"Promedio de temperatura: {promedio:.2f} °C")

    def ejecutar_menu_estadisticas(self):
        """Imprime un submenú interactivo para acceder a los reportes y estadísticas."""
        while True:
            try:
                print("\n\t=== MÓDULO DE REPORTES Y ESTADÍSTICAS ===\n")
                print("1. Ranking de Temperatura (Más cálida y más fría)")
                print("2. Cobertura Geográfica (Localidades sin coordenadas)")
                print("3. Promedio General de Temperatura de las localidades consultadas")
                print("4. Volver al menú principal")

                opcion = int(input("\nElija una opción (1-4): "))

                if opcion == 1:
                    self.mostrar_ranking_temperatura()
                elif opcion == 2:
                    self.mostrar_cobertura_geografica()
                elif opcion == 3:
                    self.mostrar_promedio_general()
                elif opcion == 4:
                    break
                else:
                    print("\nOpción no válida. Por favor, intente de nuevo.")

            except Exception as error:
                print(f"\nOcurrió un error inesperado en el módulo de estadísticas: {error}")
    
    def consultar_historico_api(self, localidad, fecha_inicio, fecha_fin):

        """Consulta la API de Open-Meteo para obtener variables climáticas históricas en un rango de fechas y las convierte en una lista de objetos ClimaHistorico.
        """

        url = "https://archive-api.open-meteo.com/v1/archive"
        parametros = {
            "latitude": localidad.latitud,
            "longitude": localidad.longitud,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": ["temperature_2m_mean", "relative_humidity_2m_mean", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "auto"
        }

        try:
            respuesta = requests.get(url, params=parametros)
            if respuesta.status_code == 200:
                res = respuesta.json()["daily"]
                lista_historicos = []
                
                fechas = res["time"]
                temps = res["temperature_2m_mean"]
                humedades = res["relative_humidity_2m_mean"]
                precips = res["precipitation_sum"]
                vientos = res["wind_speed_10m_max"]

                for i in range(len(fechas)):
                    fecha = fechas[i]
                    temperatura = temps[i]
                    humedad = humedades[i]
                    precipitacion = precips[i]
                    velocidad_viento = vientos[i]

                    obj_hist = ClimaHistorico(fecha, temperatura, humedad, precipitacion, velocidad_viento)
                    lista_historicos.append(obj_hist)

                return lista_historicos
            else:
                print(f"\nError al obtener históricos. Código HTTP: {respuesta.status_code}")
                return None
        except Exception as error:
            print(f"\nError al conectar con la API de archivo: {error}")
            return None

    def procesar_y_mostrar_historico(self):
    
        """ Solicita al usuario la localidad y el rango de fechas, realiza la consulta a la API  de datos históricos y procesa la información para:

        1. Mostrar métricas agrupadas mensualmente (temperatura, humedad, precipitación acumulada y viento) 
            almacenando los objetos en una tabla y aplicando agrupamientos con la librería Pandas.
        2. Calcular y mostrar los promedios de las variables meteorológicas haciendo uso de la librería NumPy.
        3. Determinar los años más calurosos, más frescos, con mayor precipitación y mayor humedad utilizando 
            funciones de agregación e identificación de índices extremos con Pandas.
        4. Generar y mostrar subgráficos comparativos de la evolución anual de las variables utilizando la librería Matplotlib.
        """

        resultado = self.seleccionar_localidad_menu()
        if resultado is None:
            return

        muni_nombre, localidad = resultado

        print("\n\t=== CONSULTA HISTÓRICA POR PERÍODO DE TIEMPO ===")
        fecha_inicio = input("Ingrese la fecha de inicio (siguiendo el formato AAAA-MM-DD): ").strip()
        fecha_fin = input("Ingrese la fecha de fin (siguiendo el formato AAAA-MM-DD): ").strip()

        print("\nDescargando datos históricos...")
        registros = self.consultar_historico_api(localidad, fecha_inicio, fecha_fin)

        if not registros or len(registros) == 0:
            print("No se obtuvieron registros para las fechas especificadas.")
            return

        datos_lista = []
        for registro in registros:
            datos_lista.append([
                registro.fecha, registro.temperatura, registro.humedad, registro.precipitacion, registro.velocidad_viento
            ])

        df = pd.DataFrame(datos_lista, columns=["Fecha", "Temperatura", "Humedad", "Precipitacion", "Viento"])
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Año"] = df["Fecha"].dt.year
        df["Mes_Año"] = df["Fecha"].dt.to_period("M")

        print(f"\n\t=== ANÁLISIS HISTÓRICO: {localidad.nombre.upper()} ({muni_nombre}) ===")
        print("\n\t=== RESUMEN MENSUAL ===")
        resumen_mes = df.groupby("Mes_Año").agg({
            "Temperatura": "mean",
            "Humedad": "mean",
            "Precipitacion": "sum", 
            "Viento": "mean"
        })

        for mes, fila in resumen_mes.iterrows():
            print(f"Mes: {mes} | Temp Prom: {fila['Temperatura']:.2f} °C | Humedad Prom: {fila['Humedad']:.2f}% | Precip Acum: {fila['Precipitacion']:.2f} mm | Viento Prom: {fila['Viento']:.2f} km/h")

        arr_temps = np.array(df["Temperatura"])
        arr_hums = np.array(df["Humedad"])
        arr_precs = np.array(df["Precipitacion"])
        arr_viens = np.array(df["Viento"])

        print("\n\t=== VALORES PROMEDIOS GENERALES ===")
        print(f"Temperatura promedio:  {np.nanmean(arr_temps):.2f} °C")  
        print(f"Humedad rel. promedio: {np.nanmean(arr_hums):.2f} %")
        print(f"Precipitación diaria promedio: {np.nanmean(arr_precs):.2f} mm")
        print(f"Velocidad viento promedio: {np.nanmean(arr_viens):.2f} km/h")

        resumen_anio = df.groupby("Año").agg({
            "Temperatura": "mean",
            "Humedad": "mean",
            "Precipitacion": "sum"
        })

        anio_mas_caluroso = resumen_anio["Temperatura"].idxmax()
        anio_mas_fresco = resumen_anio["Temperatura"].idxmin()
        anio_mas_lluvioso = resumen_anio["Precipitacion"].idxmax()
        anio_mas_humedo = resumen_anio["Humedad"].idxmax()

        print("\n\t=== EXTRACTO ANUAL DE EXTREMOS ===")
        print(f"Año más caluroso:           {anio_mas_caluroso} ({resumen_anio.loc[anio_mas_caluroso, 'Temperatura']:.2f} °C)")
        print(f"Año más fresco:             {anio_mas_fresco} ({resumen_anio.loc[anio_mas_fresco, 'Temperatura']:.2f} °C)")
        print(f"Año de mayor precipitación: {anio_mas_lluvioso} ({resumen_anio.loc[anio_mas_lluvioso, 'Precipitacion']:.2f} mm)")
        print(f"Año de mayor humedad:       {anio_mas_humedo} ({resumen_anio.loc[anio_mas_humedo, 'Humedad']:.2f} %)")

        """Generación de gráficos de líneas con Matplotlib. Crea 4 subgráficos para comparar la evolución anual (día a día) de
        cada una de las cuatro variables meteorológicas evaluadas.
        """
        
        print("\nEstamos generando los gráficos comparativos... (Debe cerrar el gráfico para poder regresar al menú principal).")
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f"Evolución Meteorológica Histórica - {localidad.nombre}", fontsize=14)

        for anio, grupo in df.groupby("Año"):
            axes[0, 0].plot(grupo["Fecha"].dt.dayofyear, grupo["Temperatura"], label=str(anio))
        axes[0, 0].set_title("Evolución de Temperatura (°C)")
        axes[0, 0].set_xlabel("Día del Año")
        axes[0, 0].legend()

        for anio, grupo in df.groupby("Año"):
            axes[0, 1].plot(grupo["Fecha"].dt.dayofyear, grupo["Humedad"], label=str(anio))
        axes[0, 1].set_title("Evolución de Humedad Relativa (%)")
        axes[0, 1].set_xlabel("Día del Año")
        axes[0, 1].legend()

        for anio, grupo in df.groupby("Año"):
            axes[1, 0].plot(grupo["Fecha"].dt.dayofyear, grupo["Precipitacion"], label=str(anio))
        axes[1, 0].set_title("Precipitación Acumulada (mm)")
        axes[1, 0].set_xlabel("Día del Año")
        axes[1, 0].legend()

        for anio, grupo in df.groupby("Año"):
            axes[1, 1].plot(grupo["Fecha"].dt.dayofyear, grupo["Viento"], label=str(anio))
        axes[1, 1].set_title("Velocidad del Viento (km/h)")
        axes[1, 1].set_xlabel("Día del Año")
        axes[1, 1].legend()

        plt.tight_layout()
        plt.show()