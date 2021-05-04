import pandas as pd
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
        self.dfPap = pap_load(ruta, cartera, fecha)
        self.dfnom = nom_load(ruta, cartera, fecha)
        self.dfdedicheq = dedicheq_load(ruta, cartera, fecha)
        self.dfpet = pet_load(ruta, cartera, fecha)
        self.dfppt = ppt_load(ruta, cartera, fecha)
        self.dfdom = dom_load(ruta, cartera, fecha)
        self.dfedidom = edi_dom_load(ruta, cartera, fecha)
        self.dfedinom = edi_nom_load(ruta, cartera, fecha)
        self.dfedipap = edi_pap_load(ruta, cartera, fecha)
        
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
        self.dfPap.df.to_csv(self.ruta + '\\rchivos csv\\pap.csv', index = False, header=True, sep='|')
        self.dfnom.df.to_csv(self.ruta + '\\rchivos csv\\nom.csv', index = False, header=True, sep='|')
        self.dfdedicheq.df.to_csv(self.ruta + '\\rchivos csv\\dedicheq.csv', index = False, header=True, sep='|')
        self.dfpet.df.to_csv(self.ruta + '\\rchivos csv\\pet.csv', index = False, header=True, sep='|')
        self.dfppt.df.to_csv(self.ruta + '\\rchivos csv\\ppt.csv', index = False, header=True, sep='|')
        self.dfdom.df.to_csv(self.ruta + '\\rchivos csv\\dom.csv', index = False, header=True, sep='|')
        self.dfedidom.df.to_csv(self.ruta + '\\rchivos csv\\edidom.csv', index = False, header=True, sep='|')
        self.dfedinom.df.to_csv(self.ruta + '\\rchivos csv\\edinom.csv', index = False, header=True, sep='|')
        self.dfedipap.df.to_csv(self.ruta + '\\rchivos csv\\edipap.csv', index = False, header=True, sep='|')
        
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