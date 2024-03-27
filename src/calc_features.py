import pandas as pd
import numpy as np
import os
import warnings



# All'inizio del tuo script o del tuo notebook, aggiungi queste linee:
warnings.simplefilter(action='ignore', category=FutureWarning)



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





def start(file_name,file_name_out,all_features,type_features):
    #se esiste lo elimina
    fp = open("conf/configurazione.txt","r")
    config = fp.read()
    fp.close()
    config = config.split("\n")

    frequenza = int(config[2])
    if os.path.exists(file_name_out):
        os.remove(file_name_out)
    # Carica i dati da data_stallo.csv
    df_stallo = pd.read_csv(file_name)
    # Converte tutte le colonne contenenti numeri salvati come stringhe in numeri float
    df_stallo = df_stallo.apply(pd.to_numeric, errors='coerce')
    values_stallo = pd.DataFrame(columns=all_features)
    for i in range(1, len(df_stallo), frequenza):  #ogni mezzo secondo 
        subset = df_stallo.iloc[i:i+frequenza]
        vector = calcola_feature(subset,type_features)
        error = 0
        for v in vector:
            if np.isnan(v).any() or np.isinf(v).any():
                error = 1
                break
        if error == 0:
                values_stallo = values_stallo.append(pd.Series(np.concatenate(vector),
                                                                index=values_stallo.columns), ignore_index=True)
    # Salva i risultati in values_stallo.csv
    values_stallo.to_csv(file_name_out, index=False)


