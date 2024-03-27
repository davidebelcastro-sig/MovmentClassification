import pandas as pd
import itertools
import csv
import os

def generate_binary_combinations(length):
    combinations = list(itertools.product([0, 1], repeat=length))
    return combinations




def remove_feature(lista, ls_feature):
    ls = [i for i in lista if any(i.startswith(feature) for feature in ls_feature)]
    return ls


def type_features():
    ls = ['Varianza','Deviazione_Standard','Massima_Ampiezza','Minima_Ampiezza','Ampiezza_Media','TF','der','rappA/G','CF']
    return len(ls),ls


def all_features():
    ls = ['Varianza_Pitch', 'Varianza_Roll', 'Varianza_AccelerometerX', 'Varianza_AccelerometerY', 
        'Varianza_AccelerometerZ', 'Varianza_GyroscopeX', 'Varianza_GyroscopeY', 'Varianza_GyroscopeZ',
        'Deviazione_Standard_Pitch', 'Deviazione_Standard_Roll', 'Deviazione_Standard_AccelerometerX', 
        'Deviazione_Standard_AccelerometerY', 'Deviazione_Standard_AccelerometerZ', 'Deviazione_Standard_GyroscopeX', 
        'Deviazione_Standard_GyroscopeY', 'Deviazione_Standard_GyroscopeZ', 'Massima_Ampiezza_Pitch', 'Massima_Ampiezza_Roll',
        'Massima_Ampiezza_AccelerometerX', 'Massima_Ampiezza_AccelerometerY', 'Massima_Ampiezza_AccelerometerZ',
        'Massima_Ampiezza_GyroscopeX', 'Massima_Ampiezza_GyroscopeY', 'Massima_Ampiezza_GyroscopeZ', 'Minima_Ampiezza_Pitch',
        'Minima_Ampiezza_Roll', 'Minima_Ampiezza_AccelerometerX', 'Minima_Ampiezza_AccelerometerY', 'Minima_Ampiezza_AccelerometerZ',
        'Minima_Ampiezza_GyroscopeX', 'Minima_Ampiezza_GyroscopeY', 'Minima_Ampiezza_GyroscopeZ', 'Ampiezza_Media_Pitch', 'Ampiezza_Media_Roll',
        'Ampiezza_Media_AccelerometerX', 'Ampiezza_Media_AccelerometerY', 'Ampiezza_Media_AccelerometerZ', 'Ampiezza_Media_GyroscopeX',
        'Ampiezza_Media_GyroscopeY', 'Ampiezza_Media_GyroscopeZ','TF1','TF2','TF3','TF4','TF5','TF6','der11','der12','der13','der14',
        'der15','der16','der21','der22','der23','der24','der25','der26','der31','der32','der33','der34','der35','der36',
        'rappA/G1','rappA/G2','rappA/G3','CF1','CF2','CF3','CF4','CF5','CF6']
    return ls


def add_feature(lista):
    f = all_features()
    new_ls = []
    for el in f:
        for x in lista:
            if el.startswith(x):
                new_ls.append(el)
    return new_ls





def find_features():
    #se esiste lo elimina
    if os.path.exists('features.csv'):
        os.remove('features.csv')
    if os.path.exists('type_features.csv'):
        os.remove('type_features.csv')
    cop = type_features()
    number = cop[0]
    typef = cop[1]
    binary_combinations = generate_binary_combinations(number)
    for elin in binary_combinations:
        ls_feature = []
        for i in range(len(elin)):
            if elin[i] == 1:
                ls_feature.append(typef[i])
        feature_to_analize = add_feature(ls_feature)
        
        with open ('features.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(feature_to_analize)
        with open ('type_features.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(ls_feature)


