in 2 minuti ne ho prese 2785 quindi 23,20 campioni al secondo
io analizzo ogni 35 campioni(quindi 1.5 secondi)
per ogni gruppo prendo deviazione standard e viarianza dei 3 assi di acceleroemtro e giroscipio e angolo picth e roll)
la dev standard mi dice quanto si discostano i dati dalla media ed è utili in caso di caduta perchè c'è un grosso cambiamento nei dati(anche la varianza è alta)
a questo punto calcolo la differenza tra gruppo i e gruppo i+1, se la differenze è alta potrebbe essere indice di caduta perchè vuoldire che ho avuto dati diversi nel primo momento 1.5 e nel successivo momento 1.5
modello random forest si allena su due file uno è camminata l'altro tutte cadute dove ogni record è la differenza tra record i+1 e i dei valori summurizzati ogni 1.5.

