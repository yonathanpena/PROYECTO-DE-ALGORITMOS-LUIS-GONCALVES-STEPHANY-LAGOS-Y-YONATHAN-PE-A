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