import pandas as pd
from src.services.service_calculator import Calculator

class DataProcessor:
    def __init__(self, excel_handler):
        self.excel_handler = excel_handler
        self.results = []

    def process_data(self):
        df = self.excel_handler.df

        for _, row in df.iterrows():
            stock = int(row['Stock']) if pd.notna(row['Stock']) else None
            last_sales_day = int(row['VtaUltDiasCant']) if pd.notna(row['VtaUltDiasCant']) else None
            ddi_packqty = row['DDI_Packqty']
            ddi_innerpack = row['DDI_Innerpack']
            ddi_master_pack = row['DDI_Masterpack']

            validate_packqty = Calculator.evaluate_packqty(ddi_packqty, 60, stock, last_sales_day)
            validate_innerpack = Calculator.evaluate_innerpack(ddi_innerpack, 60, stock, last_sales_day)
            validate_masterpack = Calculator.evaluate_masterpack(ddi_master_pack, 60, stock, last_sales_day)
            ideal_size = Calculator.calculate_ideal_size(28, last_sales_day, 60, 7)
            
            results = {
                'Fecha': row['Fecha'].strftime('%d/%m/%Y') if pd.notna(row['Fecha']) else '',
                'idtienda': row['idtienda'],
                'TdaNombre': row['TdaNombre'],
                'DistNombre': row['DistNombre'],
                'TdaClasifOper': row['TdaClasifOper'],
                'IdProducto': row['IdProducto'],
                'ProdNombre': row['ProdNombre'],
                'DptoProd': row['DptoProd'],
                'ClaseProd': row['ClaseProd'],
                'BloqueoGeneral': row['BloqueoGeneral'],
                'BloqueoTiendaCompra': row['BloqueoTiendaCompra'],
                'Idproveedor': row['Idproveedor'],
                'ProveeNombre': row['ProveeNombre'],
                'Stock': stock,
                'DDI_Packqty': Calculator.safe_round(ddi_packqty),
                'DDI_Innerpack': Calculator.safe_round(ddi_innerpack),
                'DDI_Masterpack': Calculator.safe_round(ddi_master_pack),
                'Valida_Packqty': validate_packqty,
                'Valida_IP': validate_innerpack,
                'Valida_MP': validate_masterpack,
                'Tamaño ideal (unidades)': ideal_size
            }
            self.results.append(results)

    def get_results_dataframe(self):
        return pd.DataFrame(self.results)
