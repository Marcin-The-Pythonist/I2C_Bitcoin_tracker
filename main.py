import network
import urequests
from machine import Pin, SoftI2C
from pico_i2c_lcd import I2cLcd
from time import sleep

### Initializing LCD
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
    
i2c = SoftI2C(sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

### Giving raspberry a moment to turn on
def overwrite(text, where_x, where_y):
    lcd.move_to(where_x, where_y)
    lcd.putstr(text)
    
throbber = ['Loading.  ','Loading..','Loading...']

for i in range(4):
    for j in throbber:
        overwrite(j,0,0)
        sleep(0.5)    
lcd.move_to(0,0)
### Connecting to the internet
ssid = "" # Put router's name here
password = "" # Put router's password here

while True:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        ### IF connection is established
        if wlan.isconnected() == True:
            lcd.putstr(f"WLAN Status:{int(wlan.isconnected())}")
        ### IF connection is not established
        else:
            lcd.putstr(f"WLAN Status:{int(wlan.isconnected())}")
            overwrite("Attempting again",0,1)
            sleep(2)
            lcd.move_to(0,0)
            lcd.clear()
            sleep(2)
            continue
        sleep(2)
        lcd.move_to(0,0)
        lcd.clear()
        break

### Getting data from the API
lcd.putstr(f"Bitcoin price:")

time = 0 # Time since last price update
btc_usd_prev = 0

while True:
        r = urequests.get("https://api.coindesk.com/v1/bpi/currentprice.json") # Server that returns the current GMT+0 time.
        json = r.json()
        btc_usd = json["bpi"]["USD"]["rate"]
        
        ### Reset timer IF price changed
        if btc_usd != btc_usd_prev:
            time = 0
            lcd.move_to(12,1)
            lcd.putstr("    ")
        
        lcd.move_to(0,1)
        lcd.putstr(f"{btc_usd}$")
        lcd.move_to(12,1)
        lcd.putstr(str(time) + "s")
        
        time = time + 1
        btc_usd_prev = btc_usd
        sleep(0.5)
