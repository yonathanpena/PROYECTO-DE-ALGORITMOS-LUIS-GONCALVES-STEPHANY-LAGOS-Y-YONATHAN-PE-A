class Localidad:
    """Clase que representa una localidad geográfica dentro de un municipio."""
    
    def __init__(self, nombre, latitud=None, longitud=None):
        """Inicializa una instancia de una localidad con sus coordenadas geográficas opcionales.

        Args:
            nombre (str): Nombre de la localidad.
            latitud (float, opcional): Coordenada de latitud geográfica. 
            longitud (float, opcional): Coordenada de longitud geográfica.
        """
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """Verifica si la localidad posee coordenadas geográficas válidas.
        
        Returns:
            bool: True si posee latitud y longitud distintas de None, False en caso contrario.
            """
        if self.latitud is not None and self.longitud is not None:
            return True
        else:
            return False