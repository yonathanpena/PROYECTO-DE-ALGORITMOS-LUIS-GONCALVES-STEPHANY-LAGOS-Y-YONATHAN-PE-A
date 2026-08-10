class ClimaActual:
    """Clase que almacena los detalles meteorológicos de una consulta realizada en tiempo real."""
    
    def __init__(self, temperatura, humedad, velocidad_viento, codigo_tiempo):
        """Inicializa un nuevo registro con los datos climáticos actuales de una localidad.

        Args:
            temperatura (float / int): Temperatura actual en grados Celsius (°C).
            humedad (float / int): Porcentaje de humedad relativa (%).
            velocidad_viento (float / int): Velocidad del viento expresada en kilómetros por hora (km/h).
            codigo_tiempo (int): Código numérico que representa el estado del tiempo.
        """
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad_viento = velocidad_viento
        self.codigo_tiempo = codigo_tiempo