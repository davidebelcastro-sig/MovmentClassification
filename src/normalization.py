import csv


def normalize_csv(file_name,volontario,posizione):
    with open(file_name, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        file_name = file_name.replace(f"csv/{volontario}/{posizione}/data_grezzi/grezzi_data_", f"csv/{volontario}/{posizione}/data_normalized/normalized_data_")
        with open(file_name, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for row in csv_reader:
                appo = row[:8]
                #se un valore è "" salto la riga
                if ("" not in appo and "nan" not in appo and "0" not in appo and 0 not in appo):
                    csv_writer.writerow(appo)

                

    return file_name


