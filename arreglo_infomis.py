import pandas as pd
import csv

#34
df = pd.read_csv(r"C:\Users\bc221066\Documents\José Prieto\Base de Clientes\Julio\Info_Mis_Natural.txt", engine='python',lineterminator="*", sep="☻", index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE, nrows=1000000)

for i in df.index: 
    print(i)
    tamano = len(df[0][i])
    string = df[0][i]
    posicion_ult_barra = len(string) - 1
    contador = 0
    aux = 0
    while (aux == 0):
        if(string[posicion_ult_barra] == "|"):
            aux = 1
        elif(posicion_ult_barra < 1):
            aux = 1
        else:
            posicion_ult_barra = posicion_ult_barra - 1
    while (contador < 33 and posicion_ult_barra > 0):
        for x, caracter in enumerate(df[0][i]):
            if (x > posicion_ult_barra):
                pass
            elif (contador < 32):
                if(caracter == "|"):
                    contador = contador + 1
            elif (contador == 32 and x == posicion_ult_barra):
                contador = 33
            elif (contador == 32 and x < posicion_ult_barra and caracter == "|"):
                caracter = "-"

df.to_csv('C:\\Users\\bc221066\\Documents\\José Prieto\\Base de Clientes\\Julio\\Info_Mis_Natural_reparado.csv', sep="┼", index=False, header=None, encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
df = pd.read_csv(r"C:\Users\bc221066\Documents\José Prieto\Base de Clientes\Julio\Info_Mis_Natural_reparado.txt", error_bad_lines=False, delimiter='|', index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
df.to_csv('C:\\Users\\bc221066\\Documents\\José Prieto\\Base de Clientes\\Julio\\Info_Mis_Natural_reparado.txt', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)