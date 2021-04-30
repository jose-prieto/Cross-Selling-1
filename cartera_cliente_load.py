import pandas as pd
import pyodbc as pdbc

class cartera_cliente_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\Cartera_Cliente_Inicio_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"CedulaCliente"] = self.quitarCeros(fila["CedulaCliente"])
        return df
    
    def make_DF(self):
        print("Creando cartera")
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\José Prieto\Documents\Bancaribe\Enero\Cartera_Cliente_Inicio_Enero_2021.accdb')
        df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM Cartera_Clientes_Enero_2020 WHERE "Tipo de Persona" = ?', conn, params=["PJ"])
        df = self.recorrerDF(df)
        df.to_csv(r'C:\Users\José Prieto\Desktop\archivos csv\cartera.csv', index = False, header=True, sep='|')
        return df

#cartera = cartera_cliente_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero')
#writer = pd.ExcelWriter('cartera_juridico.xlsx')
#cartera.make_DF()
#writer.save()