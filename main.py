from sistema_meteo_caracas import SistemaMeteoCaracas

def main():
    """
    Inicializa el sistema meteorológico cargando las zonas geográficas 
    desde el archivo JSON y controla el menú principal para la navegación 
    de las distintas funcionalidades.
    """
    zona_caracas = 'zonas_caracas.json'

    sistema = SistemaMeteoCaracas(zona_caracas)

    while True:
        print("\n\t<<< SISTEMA METEOCARACAS >>>\n")
        print("1. Ver Reporte de Carga de Datos")
        print("2. Consultar clima en tiempo real")
        print("3. Módulo de Reportes y Estadísticas")
        print("4. Consulta de Históricos por Período")
        print("5. Salir")
        
        try:
            opcion = int(input("\nElija una opción (1-5): "))

            if opcion == 1:
                sistema.mostrar_reporte_carga()
            elif opcion == 2:
                sistema.ejecutar_menu_consulta_tiempo_real()
            elif opcion == 3:
                sistema.ejecutar_menu_estadisticas()
            elif opcion == 4:
                sistema.procesar_y_mostrar_historico()
            elif opcion == 5:
                print("\n¡Gracias por usar MeteoCaracas! Hasta luego.")
                break
            else:
                print("\nOpción no válida. Por favor, ingrese un número del 1 al 5.")

        except ValueError:
            print("\nError: Debe ingresar únicamente números válidos, no letras ni símbolos.")

if __name__ == "__main__":
    main()