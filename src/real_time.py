import serial
import numpy as np
import warnings
import pandas as pd
import joblib
from sklearn.exceptions import DataConversionWarning
import turtle


# Ignora gli avvisi di tipo UserWarning
warnings.filterwarnings("ignore", category=UserWarning)

# Ignora gli avvisi di tipo DataConversionWarning
warnings.filterwarnings("ignore", category=DataConversionWarning)




def get_att(pred,ls_att):
    return ls_att[pred]
   
def calcola_CF(colonna):
    return np.max(colonna) / np.sqrt(np.mean(colonna**2))

def calcola_feature(subset,type_features):
    six_axes = subset[['AccelerometerX', 'AccelerometerY', 'AccelerometerZ', 'GyroscopeX', 'GyroscopeY', 'GyroscopeZ']].values
    lista_features = []
    for features in type_features:
        if features == 'Varianza':
            varianza = subset.var().values
            lista_features.append(varianza)
        if features == 'Deviazione_Standard':
            deviazione_standard = subset.std().values
            lista_features.append(deviazione_standard)
        if features == 'Massima_Ampiezza':
            massima_ampiezza = subset.max().values
            lista_features.append(massima_ampiezza)
        if features == 'Minima_Ampiezza':
            minima_ampiezza = subset.min().values
            lista_features.append(minima_ampiezza)
        if features == 'Ampiezza_Media':
            ampiezza_media = subset.mean().values
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

att = config[3]
att = att.split(":")
ls_att = att[1].split(",")
model_filename = './model/random_forest_model.pkl'

# Carica il modello durante la fase di testing
loaded_model = joblib.load(model_filename)




with open("best_solution.csv", 'r') as file:
        type_features = pd.read_csv(file)

a = type_features.columns[0]
#splitto per quello che c'è tra due apici
type_features = a.split("'")
appo = []
for el in type_features:
    if el == '[' or el == ']' or ',' in el:
        pass
    else:
        appo.append(el)

type_features = appo
ser = serial.Serial(config[1], int(config[0]))  # Assicurati di impostare la porta seriale corretta
freq = int(config[2])
subset = []
file_attivita = open("attivita/attivita.txt","w")
while True:
    try:
        data = ser.readline().decode('utf-8').strip()
        data_list = data.split(',')
        if data_list[0] != "nan" and data_list[1] != "nan" and len(data_list) == 8: 
            if len(subset) < freq:
                subset.append(data_list)
            else:
                df_stallo = pd.DataFrame(subset, columns=['Pitch', 'Roll','AccelerometerX', 'AccelerometerY', 'AccelerometerZ', 'GyroscopeX', 'GyroscopeY', 'GyroscopeZ'])
                df_stallo = df_stallo.apply(pd.to_numeric, errors='coerce')
                vector = calcola_feature(df_stallo,type_features)
                error = 0
                for v in vector:
                    if np.isnan(v).any() or np.isinf(v).any():
                        error = 1
                        break
                if error == 0:
                    #faccio predizione
                    vector = np.concatenate(vector)
                    predictions = loaded_model.predict(vector.reshape(1, -1))
                    attivita = get_att(predictions[0],ls_att)
                    print(attivita)
                    file_attivita.write(attivita + "\n")


                else:
                    print("Errore in predizione ...")
                subset = []
                subset.append(data_list)


    except Exception as e:
        print(e)
        pass
# Chiudi la porta seriale
ser.close()
file_attivita.close()
