import machine 
import ssd1306
import network  
import urequests
import ujson as json
import time

scl = machine.Pin(15, machine.Pin.OUT, machine.Pin.PULL_UP)
sda = machine.Pin(14, machine.Pin.OUT, machine.Pin.PULL_UP)
i2c = machine.I2C(scl=scl, sda=sda, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
def print_text(msg, x, y, clr):
    if clr:
        oled.fill(0)
    oled.text(msg, x, y)
    oled.show()



sta = network.WLAN(network.STA_IF) 
if not sta.isconnected():  
  print('connecting to network...')  
  sta.active(True)  
  sta.connect('Doris gerald', '15031996')  
  while not sta.isconnected():  
    pass  
print('network config:', sta.ifconfig()) 


BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "52a3b3450ba5c2a4cf7f67f9edec63e1" 
CITY_NAME = "chennai" 
URL = BASE_URL + "q=" + CITY_NAME + "&appid=" + API_KEY

UPDATE_INTERVAL_ms = 5000 
last_update = time.ticks_ms()



while True:
    if time.ticks_ms() - last_update >= UPDATE_INTERVAL_ms:
        response = urequests.get(URL)

        if response.status_code == 200: 
            
            data = response.json() 

           
            main = data['main'] 

            
            temperature = main['temp'] - 273.15 

            
            humidity = main['humidity'] 

            
            pressure = main['pressure'] 

           
            report = data['weather'] 

            
            print_text('**OpenWeather**', 3, 5, 1)
            print_text('City:{}' .format(CITY_NAME), 3, 15, 0)
            print_text('Temp:{} oC' .format(temperature), 3, 25, 0)
            print_text('Humi:{} %' .format(humidity), 3, 35, 0)
            print_text('Pres:{} hPa' .format(pressure), 3, 45, 0)
            print_text('"{}."' .format(report[0]['description']), 3, 55, 0)

          
            print('')
            print('**OpenWeather**')
            print('City:{}' .format(CITY_NAME))
            print('Temperature:{} oC' .format(temperature)) 
            print('Humidity:{} %' .format(humidity)) 
            print('Pressure:{} hPa' .format(pressure)) 
            print('Weather Report:{}.' .format(report[0]['description'])) 
        else: 
           
            print_text('Error in HTTP request.', 3, 20, 1)
            print('Error in HTTP request.')

        led.value(not led.value())
        last_update = time.ticks_ms()
