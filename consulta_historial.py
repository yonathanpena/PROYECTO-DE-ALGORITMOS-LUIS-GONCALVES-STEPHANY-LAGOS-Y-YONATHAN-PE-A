class ConsultaHistorial:
    """Clase para registrar las consultas de clima realizadas durante la sesión."""

    def __init__(self, municipio_nombre, localidad_nombre, temperatura):
        """Inicializa un nuevo registro en el historial de consultas de la sesión.

        Args:
            municipio_nombre (str): Nombre del municipio al que pertenece la localidad.
            localidad_nombre (str): Nombre de la localidad consultada.
            temperatura (float / int): Temperatura registrada en la consulta expresada en grados Celsius (°C).
        """
        self.municipio_nombre = municipio_nombre
        self.localidad_nombre = localidad_nombre
        self.temperatura = temperatura