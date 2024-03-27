import serial
import csv
import time


fp = open("conf/configurazione.txt","r")
config = fp.read()
fp.close()
config = config.split("\n")

ser = serial.Serial(config[1], int(config[0]))  # Assicurati di impostare la porta seriale corretta

i = 0
    # Leggi e scrivi i dati dalla porta seriale al file CSV
now =  time.time()
while True:    
    #dopo un secondo chiudo
    if time.time() - now > 1.2:

        print(i)
        now =  time.time()
        break
    try:
        data = ser.readline().decode('utf-8').strip()
        if data:
            i+=1
            continue
    except:
        pass

        
#OGNI SECONDO VENGONO INVIATI CIRCA 200 CAMPIONI CON FREQUENZA 115200.
