import combination_features
import csv
import from_grezzi_to_retrain
import warnings
import svuota_csv


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




if __name__ == "__main__":
    #svuota_csv.svuota()
    start()
    best_solution = find_best_solution()
    if best_solution:
        type_features, accuracy = best_solution
        print(f"Migliore soluzione: Type Features = {type_features}, Accuracy = {accuracy}")
        with open('best_solution.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow([type_features])
        features = combination_features.add_feature(type_features)
        acc,lista_label,attivita  = from_grezzi_to_retrain.run(features, type_features)
        print(f"Accuracy = {acc}" + "%")
        print(f"Features = {type_features}")
        lungh = len(lista_label)
        for i in range(lungh):
                print('Attività: '+ attivita[i])
                print("Training set: "+ str(lista_label[i][0]))
                print("Testing set: " + str(lista_label[i][1]))

    else:
        print("Nessuna soluzione trovata nel file.")
