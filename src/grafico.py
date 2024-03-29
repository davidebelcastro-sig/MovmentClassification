import numpy as np
import matplotlib.pyplot as plt

def plot_accuracy(attivita, correct_counts, incorrect_counts, incorrect_labels, accuracy):
    num_labels = len(attivita)
    labels = np.arange(num_labels)

    # Plot dell'accuratezza complessiva del modello
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(['Accuracy'], [accuracy], color='blue')
    plt.title('Total accuracy')

    # Plot dei casi corretti e sbagliati per ogni label
    plt.subplot(1, 2, 2)
    bar_width = 0.35
    plt.bar(labels, correct_counts, bar_width, label='Correct', color='green')
    plt.bar(labels + bar_width, [sum(sublist) for sublist in incorrect_counts], bar_width, label='Incorrect', color='red')
    plt.xlabel('Activity')
    plt.ylabel('Cases number')
    plt.title('Correct and incorrect cases for each activity')
    # Traduzione delle attività in inglese


    plt.xticks(labels + bar_width / 2, attivita, rotation=45)
    
    # Aggiungi etichette sbagliate
    for i, count in enumerate([sum(sublist) for sublist in incorrect_counts]):
        incorrect_label = incorrect_labels[i]
        if count > 0:
            if isinstance(incorrect_label, list):  # Se ci sono più etichette sbagliate
                 for j, label in enumerate(incorrect_label):
                    if j == 0:
                        plt.text(labels[i] + bar_width, count, f'{label} ({incorrect_labels[i].count(label)})', ha='center', va='bottom', color='black')
                    else:
                        plt.text(labels[i] + bar_width, count+3*(j+1), f'{label} ({incorrect_labels[i].count(label)})', ha='center', va='bottom', color='black')
            else:
                plt.text(labels[i] + bar_width, count, incorrect_label, ha='center', va='bottom', color='black')

    plt.legend()

    plt.tight_layout()
    plt.savefig('output/accuracy.png')




# Dati forniti
fp = open("conf/configurazione.txt","r")
config = fp.read()
fp.close()
config = config.split("\n")
att = config[3]
att = att.split(":")
attivita = att[1].split(",")

def run(correct_counts, incorrect_counts, incorrect_labels, accuracy):
    plot_accuracy(attivita, correct_counts, incorrect_counts, incorrect_labels, accuracy)


