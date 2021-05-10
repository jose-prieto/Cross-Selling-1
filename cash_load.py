import pandas as pd
import csv
from cash.pap_load import pap_load
from cash.nom_load import nom_load
from cash.dedicheq_load import dedicheq_load
from cash.pet_load import pet_load
from cash.ppt_load import ppt_load
from cash.dom_load import dom_load
from cash.edi_dom_load import edi_dom_load
from cash.edi_nom_load import edi_nom_load
from cash.edi_pap_load import edi_pap_load

class cash_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando cash")
        self.crear_excel(ruta)
        input("Vacíe la información necesaria en el archivo de excel recién creado 'cash_llena.xlsx' en la ruta:\n\n" + ruta + "\n\ny luego presione Enter")
        self.ruta = ruta
        self.dfPap = pap_load(ruta, cartera, fecha).df
        self.dfnom = nom_load(ruta, cartera, fecha).df
        self.dfdedicheq = dedicheq_load(ruta, cartera, fecha).df
        self.dfpet = pet_load(ruta, cartera, fecha).df
        self.dfppt = ppt_load(ruta, cartera, fecha).df
        self.dfdom = dom_load(ruta, cartera, fecha).df
        self.dfedidom = edi_dom_load(ruta, cartera, fecha).df
        self.dfedinom = edi_nom_load(ruta, cartera, fecha).df
        self.dfedipap = edi_pap_load(ruta, cartera, fecha).df
        
        self.dfPap = self.dfPap.assign(fecha = fecha)
        self.dfnom = self.dfnom.assign(fecha = fecha)
        self.dfdedicheq = self.dfdedicheq.assign(fecha = fecha)
        self.dfpet = self.dfpet.assign(fecha = fecha)
        self.dfppt = self.dfppt.assign(fecha = fecha)
        self.dfdom = self.dfdom.assign(fecha = fecha)
        self.dfedidom = self.dfedidom.assign(fecha = fecha)
        self.dfedinom = self.dfedinom.assign(fecha = fecha)
        self.dfedipap = self.dfedipap.assign(fecha = fecha)
        
    def get_monto(self):
        dfPap = self.dfPap.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfPap['monto'] = dfPap['monto'].astype(str)
        for i in range(len(dfPap['monto'])):
            dfPap['monto'][i]=dfPap['monto'][i].replace('.',',')
            
        dfnom = self.dfnom.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfnom['monto'] = dfnom['monto'].astype(str)
        for i in range(len(dfnom['monto'])):
            dfnom['monto'][i]=dfnom['monto'][i].replace('.',',')
            
        dfdedicheq = self.dfdedicheq.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfdedicheq['monto'] = dfdedicheq['monto'].astype(str)
        for i in range(len(dfdedicheq['monto'])):
            dfdedicheq['monto'][i]=dfdedicheq['monto'][i].replace('.',',')
            
        dfPet = self.dfpet.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfPet['monto'] = dfPet['monto'].astype(str)
        for i in range(len(dfPet['monto'])):
            dfPet['monto'][i]=dfPet['monto'][i].replace('.',',')
            
        dfppt = self.dfppt.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfppt['monto'] = dfppt['monto'].astype(str)
        for i in range(len(dfppt['monto'])):
            dfppt['monto'][i]=dfppt['monto'][i].replace('.',',')
            
        dfdom = self.dfdom.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfdom['monto'] = dfdom['monto'].astype(str)
        for i in range(len(dfdom['monto'])):
            dfdom['monto'][i]=dfdom['monto'][i].replace('.',',')
        
        dfMonto = pd.merge(dfPap.rename(columns={'monto': 'Pagos a Proveedores'}), dfnom.rename(columns={'monto': 'Nómina'}), how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfdedicheq.rename(columns={'monto': 'Dedicheq'}), how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfPet.rename(columns={'monto': 'Pagos Especiales a Terceros'}), how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfppt.rename(columns={'monto': 'Pagos por Taquilla'}), how='outer', right_on='mis', left_on='mis')
        return pd.merge(dfMonto, dfdom.rename(columns={'monto': 'Domiciliación'}), how='outer', right_on='mis', left_on='mis').groupby(['mis'], as_index=False).agg({'Pagos a Proveedores': 'first', 'Nómina': 'first', 'Dedicheq': 'first', 'Pagos Especiales a Terceros': 'first', 'Pagos por Taquilla': 'first', 'Domiciliación': 'first'})
    
    def get_usable(self):
        dfPap = self.dfPap.assign(uso = 1)
        dfPap = dfPap.rename(columns={'uso': 'Pagos a Proveedores'}).groupby(['mis'], as_index=False).agg({'Pagos a Proveedores': 'first'})
        
        dfnom = self.dfnom.assign(uso = 1)
        dfnom = dfnom.rename(columns={'uso': 'Nómina'}).groupby(['mis'], as_index=False).agg({'Nómina': 'first'})
        
        dfdedicheq = self.dfdedicheq.assign(uso = 1)
        dfdedicheq = dfdedicheq.rename(columns={'uso': 'Dedicheq'}).groupby(['mis'], as_index=False).agg({'Dedicheq': 'first'})
        
        dfpet = self.dfpet.assign(uso = 1)
        dfpet = dfpet.rename(columns={'uso': 'Pagos Especiales a Terceros'}).groupby(['mis'], as_index=False).agg({'Pagos Especiales a Terceros': 'first'})
        
        dfppt = self.dfppt.assign(uso = 1)
        dfppt = dfppt.rename(columns={'uso': 'Pagos por Taquilla'}).groupby(['mis'], as_index=False).agg({'Pagos por Taquilla': 'first'})
        
        dfdom = self.dfdom.assign(uso = 1)
        dfdom = dfdom.rename(columns={'uso': 'Domiciliación'}).groupby(['mis'], as_index=False).agg({'Domiciliación': 'first'})
        
        dfMonto = pd.merge(dfPap, dfnom, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfdedicheq, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfpet, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfppt, how='outer', right_on='mis', left_on='mis')
        return pd.merge(dfMonto, dfdom, how='outer', right_on='mis', left_on='mis').groupby(['mis'], as_index=False).agg({'Pagos a Proveedores': 'first', 'Nómina': 'first', 'Dedicheq': 'first', 'Pagos Especiales a Terceros': 'first', 'Pagos por Taquilla': 'first', 'Domiciliación': 'first'})
        
    def crear_excel(self, ruta):
        writer = pd.ExcelWriter(ruta + '\cash_llena.xlsx')
        df = pd.DataFrame(columns = ['mis', 'monto'])
        df.to_excel(writer, sheet_name="PAP", index=False)
        df.to_excel(writer, sheet_name="PET", index=False)
        df.to_excel(writer, sheet_name="NOM", index=False)
        df.to_excel(writer, sheet_name="DOM", index=False)
        df.to_excel(writer, sheet_name="PPT", index=False)
        df.to_excel(writer, sheet_name="Dedicheq", index=False)
        df.to_excel(writer, sheet_name="EDIPAP", index=False)
        df.to_excel(writer, sheet_name="EDIDOM", index=False)
        df.to_excel(writer, sheet_name="EDINOM", index=False)
        writer.save()
    
    def to_csv(self):
        self.dfPap.df['monto'] = self.dfPap.df['monto'].astype(str)
        for i in range(len(self.dfPap.df['monto'])):
            self.dfPap.df['monto'][i]=self.dfPap.df['monto'][i].replace('.',',')
        self.dfPap.df.to_csv(self.ruta + '\\rchivos csv\\pap.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfnom.df['monto'] = self.dfnom.df['monto'].astype(str)
        for i in range(len(self.dfnom.df['monto'])):
            self.dfnom.df['monto'][i]=self.dfnom.df['monto'][i].replace('.',',')
        self.dfnom.df.to_csv(self.ruta + '\\rchivos csv\\nom.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfdedicheq.df['monto'] = self.dfdedicheq.df['monto'].astype(str)
        for i in range(len(self.dfdedicheq.df['monto'])):
            self.dfdedicheq.df['monto'][i]=self.dfdedicheq.df['monto'][i].replace('.',',')
        self.dfdedicheq.df.to_csv(self.ruta + '\\rchivos csv\\dedicheq.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfpet.df['monto'] = self.dfpet.df['monto'].astype(str)
        for i in range(len(self.dfpet.df['monto'])):
            self.dfpet.df['monto'][i]=self.dfpet.df['monto'][i].replace('.',',')
        self.dfpet.df.to_csv(self.ruta + '\\rchivos csv\\pet.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfppt.df['monto'] = self.dfppt.df['monto'].astype(str)
        for i in range(len(self.dfppt.df['monto'])):
            self.dfppt.df['monto'][i]=self.dfppt.df['monto'][i].replace('.',',')
        self.dfppt.df.to_csv(self.ruta + '\\rchivos csv\\ppt.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfdom.df['monto'] = self.dfdom.df['monto'].astype(str)
        for i in range(len(self.dfdom.df['monto'])):
            self.dfdom.df['monto'][i]=self.dfdom.df['monto'][i].replace('.',',')
        self.dfdom.df.to_csv(self.ruta + '\\rchivos csv\\dom.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfedidom.df['monto'] = self.dfedidom.df['monto'].astype(str)
        for i in range(len(self.dfedidom.df['monto'])):
            self.dfedidom.df['monto'][i]=self.dfedidom.df['monto'][i].replace('.',',')
        self.dfedidom.df.to_csv(self.ruta + '\\rchivos csv\\edidom.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfedinom.df['monto'] = self.dfedinom.df['monto'].astype(str)
        for i in range(len(self.dfedinom.df['monto'])):
            self.dfedinom.df['monto'][i]=self.dfedinom.df['monto'][i].replace('.',',')
        self.dfedinom.df.to_csv(self.ruta + '\\rchivos csv\\edinom.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
        self.dfedipap.df['monto'] = self.dfedipap.df['monto'].astype(str)
        for i in range(len(self.dfedipap.df['monto'])):
            self.dfedipap.df['monto'][i]=self.dfedipap.df['monto'][i].replace('.',',')
        self.dfedipap.df.to_csv(self.ruta + '\\rchivos csv\\edipap.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
    """def insertDfAccess(self,df):
        try:
            cursor = self.conn.cursor()
            for indice_fila, fila in df.iterrows():
                print("hola")
                cursor.execute("INSERT INTO UNIFICA ([mis], [rif_cedula], [tipo_persona], [estatus_operacion], [producto], [categoria], [monto contable]) VALUES(?,?,?,?,?,?,?)", fila[" MIS "], fila["Cedula/RIF "], fila[" Tipo Persona "], fila[" Estatus de la Operacion "], fila[" Producto "], fila[" Categoria "], fila[" Monto Contable "])
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        finally:
            self.conn.commit()
            self.conn.close()"""
    
#todo = cash_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Febrero')
#ccBs = todo.cc_unifica.dfBs
#ahBs = todo.ah_unifica.dfBs
#Bs = todo.dfBs