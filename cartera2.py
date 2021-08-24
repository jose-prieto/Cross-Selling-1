import pandas as pd
import csv

df = pd.read_csv(r"C:\Users\bc221066\Documents\José Prieto\Base de Clientes\Julio\Info_Mis_Natural_reparado.txt", error_bad_lines=False, delimiter='|', index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE, nrows=1500000)
df.to_csv('C:\\Users\\bc221066\\Documents\\José Prieto\\Base de Clientes\\Julio\\Info_Mis_Natural_reparado.txt', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)