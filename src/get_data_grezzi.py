import serial
import csv
import os



fp = open("conf/configurazione.txt","r")
config = fp.read()
fp.close()
config = config.split("\n")

ser = serial.Serial(config[1], int(config[0]))  # Assicurati di impostare la porta seriale corretta
situation = input("Inserire situazione: ")
volontario = input("Inserire volontario: ")
#sensor = input("Inserire sensore: ")
sensor = "coscia_dx"
# Apri un file CSV per scrivere
file_name = "csv/" + volontario + "/" + sensor + "/data_grezzi/grezzi_data_" + situation + ".csv"
#controlla se esiste il file
if not os.path.exists(file_name):
    with open(file_name, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Pitch', 'Roll', 'AccelerometerX', 'AccelerometerY', 'AccelerometerZ', 'GyroscopeX', 'GyroscopeY', 'GyroscopeZ'])
        while True:
            try:
                data = ser.readline().decode('utf-8').strip()
                fp = open("src/capture.txt", "r",encoding="utf-8")
                capture = fp.read()
                if data and capture.startswith("1"):
                    data_list = data.split(',')
                    if data_list[0] != "nan": 
                        csv_writer.writerow(data_list)
                        print(data_list)
                fp.close()
            except:
                pass
            
    # Chiudi la porta seriale
    ser.close()

else:
    with open(file_name, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        while True:
            try:
                data = ser.readline().decode('utf-8').strip()
                fp = open("src/capture.txt", "r",encoding="utf-8")
                capture = fp.read()
                if data and capture.startswith("1"):
                    data_list = data.split(',')
                    if data_list[0] != "nan": 
                        csv_writer.writerow(data_list)
                        print(data_list)
                fp.close()
            except:
                pass
            
    # Chiudi la porta seriale
    ser.close()

