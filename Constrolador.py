from cross_selling import cross_selling
from cargaDatos import cargaDatos
from pathlib import Path
import pandas as pd
import numpy as np

class controlador:
    
    def __init__(self, ruta, rutadb, db, fecha):
        self.ruta = ruta + '\\rchivos csv'
        Path(self.ruta).mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta, rutadb, fecha)
        self.cartera = self.cargaDatos.cartera_cliente(db)
        self.crossSelling = cross_selling()
    
    def crear_excel(self):
        carteraMonto = pd.merge(self.cargaDatos.unifica().dfMonto, self.cargaDatos.tdv().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.mesa_cambio().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.exportacion().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.intervencion_tdc().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.custodia().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.inventario().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.linea_cir().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.cash().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.puntos_venta().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.ivr_conexion().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.p2c().dfMonto, how='outer', left_on='mis', right_on='mis')
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021.xlsx')
        carteraMonto = pd.merge(self.cartera, carteraMonto, how='inner', left_on='MisCliente', right_on='mis').to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,8))
        #carteraMonto.replace({'\d+': np.nan, 'nan': np.nan}, regex=True).astype('object')
        #https://stackoverflow.com/questions/49918259/replace-numeric-values-in-a-pandas-dataframe
        writer.save()
        
    def crear_csv(self):
        self.cargaDatos.unifica().dfMonto
        
    def insert_db(self):
        return self.cartera.to_db()
        
contro = controlador(r'C:\Users\José Prieto\Documents\Bancaribe\Enero', r'C:\Users\José Prieto\Documents\Bancaribe\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').crear_excel()
#contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()