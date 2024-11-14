# Aplicacion del servidor
# Servidor para control de temperatura con Microdot
from boot import do_connect
from microdot import Microdot, send_file
from machine import Pin, ADC
import ds18x20
import onewire
import time

# Configuración de pines
buzzer = Pin(14, Pin.OUT)  # Buzzer para alarmas
sensor_pin = Pin(19)       # Pin del sensor de temperatura
sensor_ds18b20 = ds18x20.DS18X20(onewire.OneWire(sensor_pin))

# Variables de estado
temperature_setpoint = 0   # Temperatura de referencia establecida por el usuario
temperature_current = 24   # Temperatura inicial

# Conexión Wi-Fi
do_connect()

# Inicialización de la aplicación Microdot
app = Microdot()

# Ruta principal: entrega la página HTML
@app.route('/')
async def index(request):
    return send_file('index.html')

# Ruta para archivos estáticos
@app.route('/<dir>/<file>')
async def static(request, dir, file):
    return send_file("/{}/{}".format(dir, file))

# Ruta para leer la temperatura actual del sensor
@app.route('/sensors/ds18b20/read')
async def read_temperature(request):
    global sensor_ds18b20, temperature_current
    sensor_ds18b20.convert_temp()
    time.sleep_ms(750)
    roms = sensor_ds18b20.scan()
    if roms:
        temperature_current = sensor_ds18b20.read_temp(roms[0])
    return {'temperature': temperature_current}

# Ruta para establecer el setpoint de temperatura
@app.route('/setpoint/set/<int:value>')
async def set_setpoint(request, value):
    global temperature_setpoint, temperature_current
    temperature_setpoint = value
    # Verificar si la temperatura actual supera el setpoint
    if temperature_current >= temperature_setpoint:
        buzzer.on()
        buzzer_state = 'On'
    else:
        buzzer.off()
        buzzer_state = 'Off'
    return {'buzzer': buzzer_state}

# Ruta para consultar el estado del buzzer
@app.route('/buzzer/status')
async def buzzer_status(request):
    return {'buzzer': 'On' if buzzer.value() else 'Off'}

# Ejecutar el servidor en el puerto 80
app.run(port=80)
