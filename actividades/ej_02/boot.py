def establecer_conexion():
    import network
    from time import sleep
    interfaz_wifi = network.WLAN(network.STA_IF)
    if not interfaz_wifi.isconnected():
        print("Conectando a la red...")
        interfaz_wifi.active(True)
          interfaz_wifi.connect("Cooperadora Alumnos", "")
          while not interfaz_wifi.isconnected():
            print(".", end="")
            sleep(0.25)
    print("Configuración de la red:", interfaz_wifi.ifconfig())

establecer_conexion()
