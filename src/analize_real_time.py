import serial
import csv
import pandas as pd
import numpy as np
import joblib
import warnings


# Salva il modello in formato pkl
model_filename = 'model/random_forest_model.pkl'
# Carica il modello durante la fase di testing
model = joblib.load(model_filename)

# All'inizio del tuo script o del tuo notebook, aggiungi queste linee:
warnings.simplefilter(action='ignore', category=FutureWarning)

def calcola_CF(colonna):
    return np.max(colonna) / np.sqrt(np.mean(colonna**2))


def calcola_feature(subset,type_features):
    #subset è una matrice di 8 colonne e io devo prendere le ultime 6
    # Creare una nuova lista senza le prime due colonne
    six_axes = [row[2:] for row in subset]
    lista_features = []
    for features in type_features:
        if features == 'Varianza':
            varianza = np.var(subset,axis=0)
            lista_features.append(varianza)
        if features == 'Deviazione_Standard':
            deviazione_standard = np.std(subset,axis=0)
            lista_features.append(deviazione_standard)
        if features == 'Massima_Ampiezza':
            massima_ampiezza = np.max(subset,axis=0)
            lista_features.append(massima_ampiezza)
        if features == 'Minima_Ampiezza':
            minima_ampiezza = np.min(subset,axis=0)
            lista_features.append(minima_ampiezza)
        if features == 'Ampiezza_Media':
            ampiezza_media = np.mean(subset,axis=0)
            lista_features.append(ampiezza_media)
        if features == 'TF':
            trasformata = np.fft.fft(six_axes, axis=0)
            trasformata = trasformata.real
            trasformata = np.mean(trasformata, axis=0)
            lista_features.append(trasformata)
        if features == 'der':
            six_axes_media = np.mean(six_axes, axis=0)
            derivata_prima = np.gradient(six_axes_media) 
            derivata_seconda = np.gradient(derivata_prima)
            derivata_terza = np.gradient(derivata_seconda)
            lista_features.append(derivata_prima)
            lista_features.append(derivata_seconda)
            lista_features.append(derivata_terza)
        if features == 'rappA/G':
            six_axes_media = np.mean(six_axes, axis=0)
            rapporto = six_axes_media[0:3]/six_axes_media[3:6]
            lista_features.append(rapporto)
        if features == 'CF':
            CF = np.apply_along_axis(calcola_CF, axis=0, arr=six_axes)
            lista_features.append(CF)
    return lista_features

fp = open("conf/configurazione.txt","r")
config = fp.read()
fp.close()
config = config.split("\n")

frequenza = int(config[2])

ser = serial.Serial(config[1], int(config[0]))  # Assicurati di impostare la porta seriale corretta
data_values = []
#devo sapere quali sono le feature da analizzare
with open('best_solution.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        type_features = eval(row[0])


while True:
    try:
        data = ser.readline().decode('utf-8').strip()
        if data:
            data_list = data.split(',')
            if len(data_list) == 8:
                data_values.append(data_list)
                if len(data_values) == frequenza: #circa mezzo secondo
                    np_data_values = np.array(data_values, dtype=float)
                    feature = calcola_feature(np_data_values, type_features)
                    data_values = []
                    for i in range(len(feature)):
                        if not isinstance(feature[i], np.ndarray):
                            feature[i] = np.array([feature[i]])
                    feature = np.concatenate(feature)
                    prediction = model.predict(feature.reshape(1, -1))
                    print(f"Prediction = {prediction[0]}")
                    
    except Exception as e:
        print(f"Error: {e}")
        pass
    
# Chiudi la porta seriale
ser.close()


