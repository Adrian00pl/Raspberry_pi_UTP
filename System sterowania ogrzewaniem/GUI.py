import json
import threading
import time
from datetime import datetime
from tkinter import *
from tkinter import messagebox as mb
from tkinter.ttk import Treeview

import bme680
import board
import neopixel
import paho.mqtt.client as mqtt

pixels = neopixel.NeoPixel(board.D10, 7)
temp_sensor = 0
temp_desire = 0
state = False
list = []
list1 = []
Broker = ""
sub_topic = "sensor/temp"
heatLevel = 0
windowState = "Zamkniete"
sensor = bme680.BME680()
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)


def sens():
    while True:
        if sensor.get_sensor_data():
            temp_sensor_1 = (sensor.data.temperature)
            global temp_sensor
            temp_sensor = temp_sensor_1
            if float(temp_desire) <= temp_sensor and state == True:
                temperatureLed(0)
            elif float(temp_desire) > temp_sensor and state == False:
                temperatureLed(int(temp_desire))
            lbl0.config(text=str(temp_sensor) + '°C')
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tree1.insert('', '0', values=(date, str(temp_sensor) + '°C', heatLevel, windowState))
            list1.append((str(date), str(temp_sensor) + '°C', heatLevel, windowState))
        time.sleep(5)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(sub_topic)


def on_message(client, userdata, msg):
    global windowState
    message = str(msg.payload)
    message = message.replace("b", "")
    message = message.replace("'", "")
    if int(message) == 0:
        windowState = "Zamkniete"
        lbl44.config(text="Zamkniete")
    else:
        windowState = "Otwarte"
        lbl44.config(text="Otwarte")


def connection():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(Broker, 1883, 60)
    client.loop_start()


def temperatureLed(temp):
    global state
    global temp_sensor
    if int(temp) <= temp_sensor and state == True:
        state = False
        temperatureChange(temp)
        mb.showinfo(title="Alert", message="Ogrzewanie wyłączone")
        lbl11.config(text="OFF", fg='red')
    elif int(temp) > temp_sensor and state == False:
        state = True
        temperatureChange(temp)
        mb.showinfo(title="Alert", message="Ogrzewanie włączone")
        lbl11.config(text="ON", fg='green')


def temperatureChange(temp):
    global heatLevel
    if temp <= 0:
        pixels.fill((0, 0, 255))
        heatLevel = 0
        lbl22.config(text=0)
    elif temp > 0 and temp <= 6:
        pixels.fill((0, 255, 0))
        heatLevel = 1
        lbl22.config(text=1)
    elif temp > 6 and temp <= 12:
        pixels.fill((180, 255, 0))
        heatLevel = 2
        lbl22.config(text=2)
    elif temp > 12 and temp <= 18:
        pixels.fill((255, 255, 0))
        heatLevel = 3
        lbl22.config(text=3)
    elif temp > 18 and temp <= 24:
        pixels.fill((255, 144, 0))
        heatLevel = 4
        lbl22.config(text=4)
    elif temp > 24:
        pixels.fill((255, 0, 0))
        heatLevel = 5
        lbl22.config(text=5)
    pixels.write()


def temperatureButton():
    global temp_sensor
    global temp_desire
    try:
        temp_desire = int(txtfld.get())
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tree.insert('', 0, values=(str(date), str(temp_desire) + '°C', windowState))
        list.append((str(date), str(temp_desire) + '°C', windowState))
        lbl33.config(text=str(temp_desire) + '°C')
        temperatureLed(int(temp_desire))
    except ValueError:
        mb.showinfo(title="Alert", message="Wprowadz liczbe")


def saveFile():
    with open("historia.json", "w") as outfile:
        json.dump(list, outfile)


def openFile():
    with open("historia.json") as outfile:
        data = json.load(outfile)
    tree.delete(*tree.get_children())
    for n in data:
        tree.insert('', 0, values=(n))


window = Tk()
window.title('Zarzadzanie')
window.geometry("1500x300+1000+20")

lbl0 = Label(window, text=str(temp_sensor) + '°C', fg='black', font=("Helvetica", 16))
lbl0.place(x=70, y=30)

lbl1 = Label(window, text='Ogrzewanie:', fg='black', font=("Helvetica", 10))
lbl1.place(x=180, y=10)
lbl11 = Label(window, text='OFF', fg='red', font=("Helvetica", 10))
lbl11.place(x=400, y=10)

lbl2 = Label(window, text='Stopień ogrzewania:', fg='black', font=("Helvetica", 10))
lbl2.place(x=180, y=30)
lbl22 = Label(window, text='0', fg='black', font=("Helvetica", 10))
lbl22.place(x=400, y=30)

lbl3 = Label(window, text='Wymagana temperatura:', fg='black', font=("Helvetica", 10))
lbl3.place(x=180, y=50)
lbl33 = Label(window, text='0°C', fg='black', font=("Helvetica", 10))
lbl33.place(x=400, y=50)

lbl4 = Label(window, text='Stan okna:', fg='black', font=("Helvetica", 10))
lbl4.place(x=180, y=70)
lbl44 = Label(window, text='Zamknięte', fg='black', font=("Helvetica", 10))
lbl44.place(x=400, y=70)
txtfld = Entry(window, text="Szukaj", bd=5, width=12)
txtfld.place(x=50, y=80)

btn = Button(window, text="Ustaw", fg='blue', width=10, command=temperatureButton)
btn.place(x=50, y=120)
btn1 = Button(window, text="Zapisz", fg='blue', width=10, command=saveFile)
btn1.place(x=50, y=155)
btn2 = Button(window, text="Odczyt", fg='blue', width=10, command=openFile)
btn2.place(x=50, y=190)

lblTree = Label(window, text='Archiwum ustawionych temperatur:', fg='black', font=("Helvetica", 10))
lblTree.place(x=620, y=10)
cols = ('data', 'temp', 'window')
tree = Treeview(window, columns=cols, show='headings')
vsb = Scrollbar(window, orient='vertical', command=tree.yview)
vsb.place(x=900, y=40, height=220)
tree.configure(yscrollcommand=vsb.set)
tree.heading('data', text='Data', anchor=CENTER)
tree.column('data', minwidth=0, width=200, stretch=NO)
tree.heading('temp', text='Temp', anchor=CENTER)
tree.column('temp', minwidth=0, width=50, stretch=NO)
tree.heading('window', text='Okno', anchor=CENTER)
tree.column('window', minwidth=0, width=150, stretch=NO)
tree.grid(row=0, column=0, sticky='nsew')
tree.place(x=500, y=40)

lblTree1 = Label(window, text='Archiwum zmiany temperatur:', fg='black', font=("Helvetica", 10))
lblTree1.place(x=1170, y=10)
cols1 = ('data', 'temp', 'so', 'window')
tree1 = Treeview(window, columns=cols1, show='headings')
vsb = Scrollbar(window, orient='vertical', command=tree1.yview)
vsb.place(x=1450, y=40, height=220)
tree1.configure(yscrollcommand=vsb.set)
tree1.heading('data', text='Data', anchor=CENTER)
tree1.column('data', minwidth=0, width=200, stretch=NO)
tree1.heading('temp', text='Temp', anchor=CENTER)
tree1.column('temp', minwidth=0, width=50, stretch=NO)
tree1.heading('so', text='Stopien ogrzewania', anchor=CENTER)
tree1.column('so', minwidth=0, width=50, stretch=NO)
tree1.heading('window', text='Okno', anchor=CENTER)
tree1.column('window', minwidth=0, width=150, stretch=NO)
tree1.grid(row=0, column=0, sticky='nsew')
tree1.place(x=1000, y=40)

t1 = threading.Thread(target=sens)
t1.daemon = True
t1.start()
connection()
window.mainloop()
