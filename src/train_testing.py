import combination_features
import csv
import from_grezzi_to_retrain
import warnings
import pandas as pd
import joblib
from sklearn.metrics import confusion_matrix
import svuota_csv
import os
import grafico

# All'inizio del tuo script o del tuo notebook, aggiungi queste linee:
warnings.simplefilter(action='ignore', category=FutureWarning)

def start():
    first = 0
    combination_features.find_features()        
    # Apertura dei file CSV in modalità lettura
    with open("accuracy.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["type_features", "accuracy"])
    with open("features.csv", 'r') as file1, open("type_features.csv", 'r') as file2:
        # Creazione degli oggetti CSV reader
        reader1 = csv.reader(file1)
        reader2 = csv.reader(file2)
        # Lettura riga per riga da entrambi i file contemporaneamente
        for row1, row2 in zip(reader1, reader2):
            #se è una lista con almeno un elemento != ""
            if any(element != "" for element in row1):
                acc,lista_label,attivita = from_grezzi_to_retrain.run(row1, row2) #row1 sono tutte le features, row2 sono i tipi di features
                with open('accuracy.csv', 'a') as file:
                    if first == 0:
                        first = 1
                        print("DIMENSIONE TRAINING SET E TESTING SET")
                        lungh = len(lista_label)
                        for i in range(lungh):
                             print('Attività: '+ attivita[i])
                             print("Training set: "+ str(lista_label[i][0]))
                             print("Testing set: " + str(lista_label[i][1]))
                    writer = csv.writer(file)
                    writer.writerow([row2, acc])
                    print(f"Type Features = {row2}, Accuracy = {acc}")
            
                    

def find_best_solution():
    best_solution = None
    max_accuracy = 0 # Inizializza con un valore molto basso
    min_feature_length = 1000  # Inizializza con un valore molto alto

    with open('accuracy.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Salta l'intestazione
        for row in reader:
            type_features = eval(row[0])  # Converti la stringa a una lista
            accuracy = float(row[1])
            # Verifica se l'accuracy è maggiore o uguale al massimo attuale
            if accuracy > max_accuracy + 0.02:
                    min_feature_length = len(type_features)
                    max_accuracy = accuracy
                    best_solution = (type_features, accuracy)
            elif accuracy >= max_accuracy - 0.02 and len(type_features) < min_feature_length:
                    min_feature_length = len(type_features)
                    best_solution = (type_features, accuracy)

    return best_solution

def get_accuracy(attivita):
    name_model = "model/random_forest_model.pkl"
    model = joblib.load(name_model)
    training_data = pd.read_csv('data/training.csv')
    # Carica i dati di testing
    testing_data = pd.read_csv('data/testing.csv')
    # Separazione delle features (X) e delle etichette (y) per il training
    X_train = training_data.drop('Label', axis=1)  # Rimuovi la colonna 'label' per ottenere le features
    y_train = training_data['Label']  # Usa solo la colonna 'label' per ottenere le etichette
    # Separazione delle features (X) e delle etichette (y) per il testing
    X_test = testing_data.drop('Label', axis=1)  # Rimuovi la colonna 'label' per ottenere le features
    y_test = testing_data['Label']  # Usa solo la colonna 'label' per ottenere le etichette
    # Calcola l'accuracy del modello
    y_pred = model.predict(X_test)
    # Calcolare la matrice di confusione
    conf_matrix = confusion_matrix(y_test, y_pred)

    correct_counts = []
    incorrect_counts = []
    incorrect_labels = []  # Etichette sbagliate predette dal modello
    


    # Contare i casi corretti e sbagliati per ogni label
    for i in range(len(conf_matrix)):
        correct_predictions = conf_matrix[i, i]
        correct_counts.append(correct_predictions)
        # Trova gli indici delle previsioni errate per questa etichetta
        incorrect_indices = [j for j in range(len(y_test)) if y_test.iloc[j] == i and y_pred[j] != i]
        # Stampa le istanze errate
        diz_label = {}
        for idx in incorrect_indices:
            if attivita[y_pred[idx]] in diz_label:
                diz_label[attivita[y_pred[idx]]] += 1
            else:
                diz_label[attivita[y_pred[idx]]] = 1
        if len(diz_label) > 0:
            vl = []
            vk = []
            for key in diz_label.keys():
                vl.append(diz_label[key])
                vk.append(key)
            incorrect_counts.append(vl)
            incorrect_labels.append(vk)
        else:
             incorrect_counts.append([0])
             incorrect_labels.append([''])
    return correct_counts, incorrect_counts, incorrect_labels



if __name__ == "__main__":
    #svuota_csv.svuota()
    #start()
    best_solution = find_best_solution()
    if best_solution:
        type_features, accuracy = best_solution
        with open('best_solution.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow([type_features])
        features = combination_features.add_feature(type_features)
        acc,lista_label,attivita  = from_grezzi_to_retrain.run(features, type_features)
        lungh = len(lista_label)
        correct_counts, incorrect_counts, incorrect_labels = get_accuracy(attivita)
        grafico.run(correct_counts, incorrect_counts, incorrect_labels, acc)
        with open('output/size_testing.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["Attività", "Training set", "Testing set"])
            for i in range(lungh):
                writer.writerow([attivita[i], lista_label[i][0], lista_label[i][1]])
        os.system("cp best_solution.csv output/features_used.csv")
    else:
        print("Nessuna soluzione trovata nel file.")
