class ClimaHistorico:
    """Clase que almacena un registro meteorológico diario dentro del período consultado."""
    
    def __init__(self, fecha, temperatura, humedad, precipitacion, velocidad_viento):
        """Inicializa una lectura meteorológica diaria para la fecha consultada.

        Args:
            fecha (str): Fecha de la medición en formato 'AAAA-MM-DD'.
            temperatura (float / int): Temperatura media diaria en grados Celsius (°C).
            humedad (float / int): Humedad relativa media diaria (%).
            precipitacion (float / int): Precipitaciones acumuladas del día expresadas en milímetros (mm).
            velocidad_viento (float / int): Velocidad media del viento registrada en el día (km/h).
        """
        self.fecha = fecha                 
        self.temperatura = temperatura       
        self.humedad = humedad           
        self.precipitacion = precipitacion 
        self.velocidad_viento = velocidad_viento  