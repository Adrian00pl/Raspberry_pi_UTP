
import utelegram
import network
import utime
from machine import Pin

debug = True

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.scan()
sta_if.connect('SSID', 'PASSWORD')
lampa=Pin(2, Pin.OUT)

if debug: print('WAITING FOR NETWORK - sleep 10')
utime.sleep(10)

def get_message(message):
    bot.send(message['message']['chat']['id'], 'Komenda nierozpoznana')

def zapal():
    lampa.value(0)
    
def zapalna(message):
    messagenew=message['message']['text']
    time=""
    for i in messagenew:
        if i.isdigit():
            time=time+i
    lampa.value(0)
    utime.sleep(int(time))
    lampa.value(1)
    
def zgas():
    lampa.value(1)
    

if sta_if.isconnected():
    bot = utelegram.ubot('TOKEN')
    bot.register('/zapal', zapal)
    bot.register('/zapalna', zapalna)
    bot.register('/zgas', zgas)
    bot.set_default_handler(get_message)

    print('BOT LISTENING')
    bot.listen()
else:
    print('NOT CONNECTED - aborting')