class Municipio:
    """Clase que representa un municipio con sus respectivas localidades."""
    
    def __init__(self, nombre):
        """Inicializa una instancia municipio con su lista de localidades vacía.

        Args:
            nombre (str): Nombre del municipio.
        """
        self.nombre = nombre
        self.localidades = []

    def agregar_localidad(self, localidad):
        """Agrega un objeto localidad a la lista perteneciente al municipio.
        Args:
            localidad (Localidad): objeto localidad que se agregará a la lista.
        """
        self.localidades.append(localidad)

    def mostrar_datos_municipio(self):
        """Calcula e imprime el reporte del municipio sobre sus localidades"""
        total = len(self.localidades)
        con_coordenadas = 0
        sin_coordenadas = 0

        for localidad in self.localidades:
            if localidad.tiene_coordenadas():
                con_coordenadas += 1
            else:
                sin_coordenadas += 1

        if total > 0:
            porcentaje = (con_coordenadas / total) * 100
        else:
            porcentaje = 0.0

        print(f"\nMunicipio: {self.nombre}")
        print(f" - Total de localidades: {total}")
        print(f" - Localidades con coordenadas geográficas: {con_coordenadas}")
        print(f" - Localidades sin coordenadas geográficas conocidas: {sin_coordenadas}")
        print(f" - Porcentaje con coordenadas geográficas: {porcentaje:.2f}%")