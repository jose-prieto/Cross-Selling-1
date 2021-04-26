import pandas as pd
import pyodbc as pdbc

class cartera_cliente_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\Cartera_Cliente_Inicio_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero\Cartera_Cliente_Inicio_Enero_2021.accdb')
        #df = pd(cursor.execute('select * from Cartera_Clientes_Enero_2020'))
        df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM Cartera_Clientes_Enero_2020 WHERE "Tipo de Persona" = ?', conn, params=["PJ"])
        #pandas.read_sql(('select * from Test where value = %(par)s'),
              # db,params={"par":'p'})
        return df