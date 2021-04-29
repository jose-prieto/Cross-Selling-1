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
        while (aux[0] == '0'):
            if(len(aux) < 2):
                return rifCliente
            aux = aux[1:]
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"CedulaCliente"] = self.quitarCeros(fila["CedulaCliente"])
        return df
    
    def make_DF(self):
        print("Creando cartera")
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\José Prieto\Documents\Bancaribe\Enero\Cartera_Cliente_Inicio_Enero_2021.accdb')
        df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM Cartera_Clientes_Enero_2020 WHERE "Tipo de Persona" = ?', conn, params=["PJ"])
        return self.recorrerDF(df)

#cartera = cartera_cliente_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#writer = pd.ExcelWriter('cartera_juridico.xlsx')
#cartera.make_DF().to_excel(writer, sheet_name='Montos por Producto Cliente', index=False)
#writer.save()