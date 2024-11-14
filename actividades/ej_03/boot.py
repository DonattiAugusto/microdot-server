# Configuracion inicial
# Configuración de conexión Wi-Fi al iniciar la placa

def do_connect():
    import network
    # Configuración de la interfaz Wi-Fi en modo estación
    wifi_interface = network.WLAN(network.STA_IF)

    # Verificación de conexión; si no está conectado, intenta conectarse
    if not wifi_interface.isconnected():
        print('Conectando a la red Wi-Fi...')
        wifi_interface.active(True)
        wifi_interface.connect('Cooperadora Alumnos', '')  # Nombre de la red Wi-Fi y contraseña

        # Espera hasta establecer conexión
        while not wifi_interface.isconnected():
            pass

    # Muestra la configuración de la red si la conexión fue exitosa
    print('Configuración de red:', wifi_interface.ifconfig())

# Llama a la función de conexión Wi-Fi al iniciar la placa
do_connect()
