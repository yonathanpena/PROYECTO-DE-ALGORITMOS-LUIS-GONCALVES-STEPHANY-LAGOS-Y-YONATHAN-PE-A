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