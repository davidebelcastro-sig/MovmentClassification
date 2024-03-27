import os


def svuota():
        for volontario in os.listdir("csv"):
            for posizione in os.listdir(f"csv/{volontario}/"):
                for type_data in os.listdir(f"csv/{volontario}/{posizione}/"):
                    if "data_features" ==  type_data or "data_normalized" ==  type_data:
                        for file in os.listdir(f"csv/{volontario}/{posizione}/{type_data}/"):
                            os.remove(f"csv/{volontario}/{posizione}/{type_data}/{file}")