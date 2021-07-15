from psycopg2.errors import ForeignKeyViolation
from cash.edi_dom_load import edi_dom_load
from cash.edi_nom_load import edi_nom_load
from cash.edi_pap_load import edi_pap_load
from cash.pap_load import pap_load
from cash.nom_load import nom_load
from cash.pet_load import pet_load
from cash.ppt_load import ppt_load
from cash.dom_load import dom_load
import pandas as pd
import csv

class cash_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando cash")
        self.crear_excel(ruta)
        input("Vacíe la información necesaria en el archivo de excel recién creado 'cash_llena.xlsx' en la ruta:\n\n" + ruta + "\n\ny luego presione Enter")
        self.ruta = ruta
        self.EdiDom = edi_dom_load(ruta, cartera, fecha).df
        self.EdiPap = edi_pap_load(ruta, cartera, fecha).df
        self.EdiNom = edi_nom_load(ruta, cartera, fecha).df
        
        self.dfPap = pd.concat([pap_load(ruta, cartera, fecha).df.dropna(axis=0, how='any'), 
                                self.EdiPap.dropna(axis=0, how='any')]).groupby(['mis']).sum().reset_index()
        self.dfnom = pd.concat([nom_load(ruta, cartera, fecha).df.dropna(axis=0, how='any'), 
                                self.EdiNom.dropna(axis=0, how='any')]).groupby(['mis']).sum().reset_index()
        #self.dfdedicheq = dedicheq_load(ruta, cartera, fecha).df.dropna(axis=0, how='any')
        self.dfpet = pet_load(ruta, cartera, fecha).df.dropna(axis=0, how='any')
        self.dfppt = ppt_load(ruta, cartera, fecha).df.dropna(axis=0, how='any')
        self.dfdom = pd.concat([dom_load(ruta, cartera, fecha).df.dropna(axis=0, how='any'), 
                                self.EdiDom.dropna(axis=0, how='any')]).groupby(['mis']).sum().reset_index()
        
        self.dfEdi = pd.concat([self.EdiDom, self.EdiNom, 
                                self.EdiPap]).groupby(['mis']).sum().reset_index().dropna(axis=0, how='any')
        """self.dfedidom = edi_dom_load(ruta, cartera, fecha).df
        self.dfedinom = edi_nom_load(ruta, cartera, fecha).df
        self.dfedipap = edi_pap_load(ruta, cartera, fecha).df"""
        
        self.dfPap = self.dfPap.assign(fecha = fecha)
        self.dfnom = self.dfnom.assign(fecha = fecha)
        #self.dfdedicheq = self.dfdedicheq.assign(fecha = fecha)
        self.dfpet = self.dfpet.assign(fecha = fecha)
        self.dfppt = self.dfppt.assign(fecha = fecha)
        self.dfdom = self.dfdom.assign(fecha = fecha)
        self.EdiDom = self.EdiDom.assign(fecha = fecha)
        self.EdiPap = self.EdiPap.assign(fecha = fecha)
        self.EdiNom = self.EdiNom.assign(fecha = fecha)
        """self.dfedidom = self.dfedidom.assign(fecha = fecha)
        self.dfedinom = self.dfedinom.assign(fecha = fecha)
        self.dfedipap = self.dfedipap.assign(fecha = fecha)"""
        
    def get_monto(self):
        dfPap = self.dfPap
        dfPap['monto'] = dfPap['monto'].astype(str)
        for i in range(len(dfPap['monto'])):
            dfPap['monto'][i]=dfPap['monto'][i].replace('.',',')
            
        dfnom = self.dfnom
        dfnom['monto'] = dfnom['monto'].astype(str)
        for i in range(len(dfnom['monto'])):
            dfnom['monto'][i]=dfnom['monto'][i].replace('.',',')
            
        """dfdedicheq = self.dfdedicheq.groupby(['mis'], as_index=False).agg({'mis': 'first', 'monto': sum})
        dfdedicheq['monto'] = dfdedicheq['monto'].astype(str)
        for i in range(len(dfdedicheq['monto'])):
            dfdedicheq['monto'][i]=dfdedicheq['monto'][i].replace('.',',')"""
            
        dfPet = self.dfpet
        dfPet['monto'] = dfPet['monto'].astype(str)
        for i in range(len(dfPet['monto'])):
            dfPet['monto'][i]=dfPet['monto'][i].replace('.',',')
            
        dfppt = self.dfppt
        dfppt['monto'] = dfppt['monto'].astype(str)
        for i in range(len(dfppt['monto'])):
            dfppt['monto'][i]=dfppt['monto'][i].replace('.',',')
            
        dfdom = self.dfdom
        dfdom['monto'] = dfdom['monto'].astype(str)
        for i in range(len(dfdom['monto'])):
            dfdom['monto'][i]=dfdom['monto'][i].replace('.',',')
            
        dfEdiDom = self.EdiDom
        dfEdiDom['monto'] = dfEdiDom['monto'].astype(str)
        for i in range(len(dfEdiDom['monto'])):
            dfEdiDom['monto'][i]=dfEdiDom['monto'][i].replace('.',',')
            
        dfEdiPap = self.EdiPap
        dfEdiPap['monto'] = dfEdiPap['monto'].astype(str)
        for i in range(len(dfEdiPap['monto'])):
            dfEdiPap['monto'][i]=dfEdiPap['monto'][i].replace('.',',')
            
        dfEdiNom = self.EdiNom
        dfEdiNom['monto'] = dfEdiNom['monto'].astype(str)
        for i in range(len(dfEdiNom['monto'])):
            dfEdiNom['monto'][i]=dfEdiNom['monto'][i].replace('.',',')
        
        dfMonto = pd.merge(dfPap.rename(columns={'monto': 'Pagos a Proveedores'}), 
                           dfnom.rename(columns={'monto': 'Nómina'}), how='outer', right_on='mis', left_on='mis')
        #dfMonto = pd.merge(dfMonto, dfdedicheq.rename(columns={'monto': 'Dedicheq'}), how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfPet.rename(columns={'monto': 'Pagos Especiales a Terceros'}), 
                           how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfppt.rename(columns={'monto': 'Pagos por Taquilla'}), 
                           how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfdom.rename(columns={'monto': 'Domiciliación'}), 
                           how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfEdiDom.rename(columns={'monto': 'Domiciliación con EDI'}), 
                           how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfEdiPap.rename(columns={'monto': 'Pagos a Proveedores con EDI'}), 
                           how='outer', right_on='mis', left_on='mis')
        return pd.merge(dfMonto, dfEdiNom.rename(columns={'monto': 'Pago de nóminas con EDI'}), 
                        how='outer', right_on='mis', left_on='mis').groupby(['mis'], 
                            as_index=False).agg({'Pagos a Proveedores': 'first', 'Nómina': 'first', 
                                'Pagos Especiales a Terceros': 'first', 'Pagos por Taquilla': 'first', 
                                'Domiciliación': 'first', 'Domiciliación con EDI': 'first', 
                                'Pagos a Proveedores con EDI': 'first', 'Pago de nóminas con EDI': 'first'})
        
        
    
    def get_usable(self):
        dfPap = self.dfPap.assign(uso = 1)
        dfPap = dfPap.rename(columns={'uso': 'Pagos a Proveedores'}).groupby(['mis'], as_index=False).agg({'Pagos a Proveedores': 'first'})
        
        dfnom = self.dfnom.assign(uso = 1)
        dfnom = dfnom.rename(columns={'uso': 'Nómina'}).groupby(['mis'], as_index=False).agg({'Nómina': 'first'})
        
        """dfdedicheq = self.dfdedicheq.assign(uso = 1)
        dfdedicheq = dfdedicheq.rename(columns={'uso': 'Dedicheq'}).groupby(['mis'], as_index=False).agg({'Dedicheq': 'first'})"""
        
        dfpet = self.dfpet.assign(uso = 1)
        dfpet = dfpet.rename(columns={'uso': 'Pagos Especiales a Terceros'}).groupby(['mis'], as_index=False).agg({'Pagos Especiales a Terceros': 'first'})
        
        dfppt = self.dfppt.assign(uso = 1)
        dfppt = dfppt.rename(columns={'uso': 'Pagos por Taquilla'}).groupby(['mis'], as_index=False).agg({'Pagos por Taquilla': 'first'})
        
        dfdom = self.dfdom.assign(uso = 1)
        dfdom = dfdom.rename(columns={'uso': 'Domiciliación'}).groupby(['mis'], as_index=False).agg({'Domiciliación': 'first'})
        
        dfEdi = self.dfEdi.assign(uso = 1)
        dfEdi = dfEdi.rename(columns={'uso': 'EDI'}).groupby(['mis'], as_index=False).agg({'EDI': 'first'})
        
        dfMonto = pd.merge(dfPap, dfnom, how='outer', right_on='mis', left_on='mis')
        #dfMonto = pd.merge(dfMonto, dfdedicheq, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfpet, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfppt, how='outer', right_on='mis', left_on='mis')
        dfMonto = pd.merge(dfMonto, dfdom, how='outer', right_on='mis', left_on='mis')
        return pd.merge(dfMonto, dfEdi, how='outer', right_on='mis', left_on='mis').groupby(['mis'], as_index=False).agg({'Pagos a Proveedores': 'first', 'Nómina': 'first', 'Pagos Especiales a Terceros': 'first', 'Pagos por Taquilla': 'first', 'Domiciliación': 'first', 'EDI': 'first'})
        
    def crear_excel(self, ruta):
        writer = pd.ExcelWriter(ruta + '\cash_llena.xlsx')
        df = pd.DataFrame(columns = ['mis', 'monto'])
        df.to_excel(writer, sheet_name="PAP", index=False)
        df.to_excel(writer, sheet_name="PET", index=False)
        df.to_excel(writer, sheet_name="NOM", index=False)
        df.to_excel(writer, sheet_name="DOM", index=False)
        df.to_excel(writer, sheet_name="PPT", index=False)
        #df.to_excel(writer, sheet_name="Dedicheq", index=False)
        df.to_excel(writer, sheet_name="EDIPAP", index=False)
        df.to_excel(writer, sheet_name="EDIDOM", index=False)
        df.to_excel(writer, sheet_name="EDINOM", index=False)
        writer.save()
    
    def to_csv(self):
        self.dfPap['monto'] = self.dfPap['monto'].astype(str)
        self.dfPap.to_csv(self.ruta + '\\rchivos csv\\pap.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        self.dfnom['monto'] = self.dfnom['monto'].astype(str)
        self.dfnom.to_csv(self.ruta + '\\rchivos csv\\nom.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        """self.dfdedicheq.df['monto'] = self.dfdedicheq.df['monto'].astype(str)
        self.dfdedicheq.df.to_csv(self.ruta + '\\rchivos csv\\dedicheq.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)"""
        
        self.dfpet['monto'] = self.dfpet['monto'].astype(str)
        self.dfpet.to_csv(self.ruta + '\\rchivos csv\\pet.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        self.dfppt['monto'] = self.dfppt['monto'].astype(str)
        self.dfppt.to_csv(self.ruta + '\\rchivos csv\\ppt.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        self.dfdom.to_csv(self.ruta + '\\rchivos csv\\dom.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        
        self.dfEdi['monto'] = self.dfEdi['monto'].astype(str)
        self.dfEdi.to_csv(self.ruta + '\\rchivos csv\\edi.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    def insertPg(self, conector):
        print("Insertando pap")
        for indice_fila, fila in self.dfPap.iterrows():
            try:
                conector.cursor.execute("INSERT INTO PAP (pap_mis, pap_monto, pap_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando nom")
        for indice_fila, fila in self.dfnom.iterrows():
            try:
                conector.cursor.execute("INSERT INTO NOM (nom_mis, nom_monto, nom_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando pet")
        for indice_fila, fila in self.dfpet.iterrows():
            try:
                conector.cursor.execute("INSERT INTO PET (pet_mis, pet_monto, pet_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando ppt")
        for indice_fila, fila in self.dfppt.iterrows():
            try:
                conector.cursor.execute("INSERT INTO PPT (ppt_mis, ppt_monto, ppt_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando dom")
        for indice_fila, fila in self.dfdom.iterrows():
            try:
                conector.cursor.execute("INSERT INTO DOM (dom_mis, dom_monto, dom_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando Edi_DOM")
        for indice_fila, fila in self.EdiDom.iterrows():
            try:
                conector.cursor.execute("INSERT INTO EDI_DOM (edi_dom_mis, edi_dom_monto, edi_dom_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando Edi_PAP")
        for indice_fila, fila in self.EdiPap.iterrows():
            try:
                conector.cursor.execute("INSERT INTO EDI_PAP (edi_pap_mis, edi_pap_monto, edi_pap_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
        
        print("Insertando Edi_NOM")
        for indice_fila, fila in self.EdiNom.iterrows():
            try:
                conector.cursor.execute("INSERT INTO EDI_NOM (edi_nom_mis, edi_nom_monto, edi_nom_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
            finally:
                conector.conn.commit()
    
#todo = cash_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Febrero')
#ccBs = todo.cc_unifica.dfBs
#ahBs = todo.ah_unifica.dfBs
#Bs = todo.dfBs