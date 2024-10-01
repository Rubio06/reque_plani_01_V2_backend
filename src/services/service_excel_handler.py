import pandas as pd

class ExcelHandler:
    def __init__(self, filename):
        self.filename = filename
        # self.sheet_name = sheet_name
        self.df = pd.DataFrame()

    def read_excel(self):
        self.df = pd.read_excel(self.filename, sheet_name = 0, header = 1, index_col = None)
        print("Archivo Excel leído con éxito.")

    def write_excel(self, data, output_file):
        with pd.ExcelWriter(output_file, engine = 'xlsxwriter') as writer:
            data.to_excel(writer, sheet_name = 'Resultados', index = False, startrow = 1)
            
            worksheet = writer.sheets['Resultados']
            self.apply_format_to_excel(writer, worksheet, data)
        
        print("Datos guardados en el archivo Excel:", output_file)

    def apply_format_to_excel(self, writer, worksheet, data):
        format_data = writer.book.add_format({'border': 1, 'align': 'center'})
        green_format = writer.book.add_format({'bg_color': '#d0ece7', 'border': 1, 'align': 'center'})

        for col_num, col in enumerate(data.columns):
            max_length = max(data[col].astype(str).apply(len).max(), len(col))
            worksheet.set_column(col_num, col_num, max_length, format_data)
        
        start_row = 2
        end_row = start_row + len(data) - 1
        for col_num in range(data.columns.get_loc('Valida_Packqty'), data.columns.get_loc('Tamaño ideal (unidades)') + 1):
            for row_num in range(start_row, end_row + 1):
                worksheet.write(row_num, col_num, data.iloc[row_num - start_row, col_num], green_format)