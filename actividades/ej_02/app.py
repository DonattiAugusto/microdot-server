# Aplicacion del servidor
# Importo las funciones esenciales para la conectividad, servidor web, control de pines y LEDs
from boot import establecer_conexion
from microdot import Microdot, send_file
import machine
import neopixel
import time

# Establecer conexión WiFi
establecer_conexion()

# Inicializamos la aplicación Microdot para manejar las rutas
app = Microdot()

# Configuramos tres LEDs individuales en los pines 32, 33 y 25
led1 = machine.Pin(32, machine.Pin.OUT)
led2 = machine.Pin(33, machine.Pin.OUT)
led3 = machine.Pin(25, machine.Pin.OUT)

# Configuramos una tira de 8 LEDs Neopixel en el pin 27
tira_led = neopixel.NeoPixel(machine.Pin(27), 8)

# Ruta principal que envía el archivo HTML de inicio
@app.route('/')
async def inicio(solicitud):
    return send_file('index.html')

# Ruta para servir archivos estáticos
@app.route('/<carpeta>/<archivo>')
async def archivo_estatico(solicitud, carpeta, archivo):
    return send_file(f"/{carpeta}/{archivo}")

# Ruta para controlar los LEDs individuales
@app.route('/led')
async def control_led(solicitud):
    # Obtener el número de LED y su estado (encendido o apagado) desde los parámetros de la URL
    numero_led = int(solicitud.args.get('led'))
    estado = solicitud.args.get('estado') == 'true'

    # Mostrar en la consola qué LED estamos controlando y su estado
    print(f"Controlando LED {numero_led}, su estado es: {estado}")

    # Seleccionar el LED correcto basado en el número (1, 2 o 3)
    led_seleccionado = [led1, led2, led3][numero_led - 1]

    # Encender o apagar el LED según el estado proporcionado
    if estado:
        led_seleccionado.on()
    else:
        led_seleccionado.off()

    # Retornar una respuesta con el estado del LED
    return f'LED {numero_led} {"Encendido" si estado else "Apagado"}'

# Ruta para controlar el color de la tira LED
@app.route('/color')
async def control_color(solicitud):
    # Obtener los valores RGB desde los parámetros de la URL
    rojo = int(solicitud.args.get('r'))
    verde = int(solicitud.args.get('g'))
    azul = int(solicitud.args.get('b'))

    # Mostrar los valores RGB en la consola
    print(f"Estableciendo color de la tira LED: Rojo:{rojo}, Verde:{verde}, Azul:{azul}")
    
    # Configurar todos los LEDs de la tira al color especificado
    tira_led.fill((rojo, verde, azul))
    tira_led.write()

    # Retornar una respuesta con el color establecido
    return f'Color establecido a Rojo:{rojo}, Verde:{verde}, Azul:{azul}'

# Iniciar la aplicación web en el puerto 80
app.run(port=80)
