import normalization
import calc_features
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# All'inizio del tuo script o del tuo notebook, aggiungi queste linee:
warnings.simplefilter(action='ignore', category=FutureWarning)

def test_classifier(model_filename,X_test,y_test):
    # Carica il modello durante la fase di testing
    loaded_model = joblib.load(model_filename)
    predictions = loaded_model.predict(X_test)
     # Calcola e visualizza l'accuratezza
    accuracy = accuracy_score(y_test, predictions)
    accuracy_percent = (accuracy * 100).round(2)
    return accuracy_percent
    


def from_grezzi_to_features(all_features, type_features):
    for volontario in os.listdir("csv"):
        for posizione in os.listdir(f"csv/{volontario}"):
            for type_data in os.listdir(f"csv/{volontario}/{posizione}"):
                #entro dentro dati grezzi
                if "data_grezzi" ==  type_data:
                    for file in os.listdir(f"csv/{volontario}/{posizione}/{type_data}"):
                        file_norm = normalization.normalize_csv(f"csv/{volontario}/{posizione}/{type_data}/{file}",volontario,posizione)
                        file_features = file_norm.split("normalized_")[1]
                        calc_features.start(file_norm, f"csv/{volontario}/{posizione}/data_features/features_{file_features}", all_features, type_features)
                  


def take_all_features():
    vector = []
    for volontario in os.listdir("csv"):
        for posizione in os.listdir(f"csv/{volontario}"):
            for type_data in os.listdir(f"csv/{volontario}/{posizione}"):
                #entro dentro dati features
                if "data_features" ==  type_data:
                    #mi prendo tutti i file     
                    for file in os.listdir(f"csv/{volontario}/{posizione}/{type_data}"):
                        vector.append(f"csv/{volontario}/{posizione}/{type_data}/{file}")

    return vector




def combine(situation,vector):
    union = []
    for el in vector:
        index = el.find("features_data_")
        name = el[index+14:]
        if situation in name:
            union.append(el)
    # Crea un DataFrame vuoto per contenere i dati combinati
    combined_data = pd.DataFrame()

    # Itera sui percorsi dei file e li concatena nel DataFrame combinato
    for percorso in union:
        df = pd.read_csv(percorso)
        combined_data = pd.concat([combined_data, df], ignore_index=True)

    # Salva il DataFrame combinato in un nuovo file CSV
    combined_data.to_csv("data/" + situation + ".csv", index=False)


def all_combine(attivita):
    vector = take_all_features()
    for el in attivita:
        combine(el,vector)



def from_features_to_train_testing():
    for situation in os.listdir("data"):
        if os.path.isdir(f"data/{situation}") or situation == "training.csv" or situation == "testing.csv":
            continue
        #divido 80% train 20% test per ogni situazione
        df = pd.read_csv(f"data/{situation}")
        df_train = df.sample(frac=0.7, random_state=200)
        df_test = df.drop(df_train.index)
        df_train.to_csv(f"data/Train/train_{situation}", index=False)
        df_test.to_csv(f"data/Test/test_{situation}", index=False)


def union_train_testing(ls_att):
    
    combined_train = pd.DataFrame()
    for situation in os.listdir("data/Train"):
            label = ls_att.index(situation.split("_")[1][:-4])
            data = pd.read_csv(f'data/Train/{situation}')
            data['Label'] = label
            combined_train = combined_train.append(data, ignore_index=True)
            # Salva il DataFrame combinato in un nuovo file CSV
    combined_train.to_csv("data/training.csv", index=False)

    combined_test = pd.DataFrame()
    for situation in os.listdir("data/Test"):
            label = ls_att.index(situation.split("_")[1][:-4])
            data = pd.read_csv(f'data/Test/{situation}')
            data['Label'] = label
            combined_test = combined_test.append(data, ignore_index=True)
            # Salva il DataFrame combinato in un nuovo file CSV
    combined_test.to_csv("data/testing.csv", index=False)

def training_random_forest():
        # Carica i dati di training
    training_data = pd.read_csv('data/training.csv')

    # Carica i dati di testing
    testing_data = pd.read_csv('data/testing.csv')

    # Separazione delle features (X) e delle etichette (y) per il training
    X_train = training_data.drop('Label', axis=1)  # Rimuovi la colonna 'label' per ottenere le features
    y_train = training_data['Label']  # Usa solo la colonna 'label' per ottenere le etichette

    # Separazione delle features (X) e delle etichette (y) per il testing
    X_test = testing_data.drop('Label', axis=1)  # Rimuovi la colonna 'label' per ottenere le features
    y_test = testing_data['Label']  # Usa solo la colonna 'label' per ottenere le etichette
    # Crea il modello RandomForest
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Addestra il modello
    model.fit(X_train, y_train)

    # Salva il modello in formato pkl
    model_filename = './model/random_forest_model.pkl'
    joblib.dump(model, model_filename)
    return model_filename, X_test, y_test,X_train,y_train



def run(all_features, type_features):
    fp = open("conf/configurazione.txt","r")
    config = fp.read()
    fp.close()
    config = config.split("\n")
    att = config[3]
    att = att.split(":")
    ls_att = att[1].split(",")
    from_grezzi_to_features(all_features, type_features)
    all_combine(ls_att)
    from_features_to_train_testing()
    union_train_testing(ls_att)
    model_filename,X_test,y_test,X_train,y_train = training_random_forest()
    #testing_model(model_filename,X_test,y_test)
    acc = test_classifier(model_filename,X_test,y_test)
    lunghezza = len(ls_att)
    lista_label = []
    for i in range(lunghezza):
        label0 = len(y_train[y_train == i])
        label00 = len(y_test[y_test == i])
        coppia = (label0,label00)
        lista_label.append(coppia)


    return acc,lista_label,ls_att

