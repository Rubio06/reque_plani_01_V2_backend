import tkinter as tk
from tkinter import filedialog, messagebox
from src.services.service_excel_handler import ExcelHandler
from src.services.service_processor import DataProcessor

class LogicalSize():
    def __init__(self):
        self.excel_handler = None
        self.processor = None
        self.df_results = None
        self.filepath = None

    def upload_file(self, file_label, sheet_name, btn_process):
        self.filepath = filedialog.askopenfilename(
            title="Seleccionar archivo Excel", 
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        
        if self.filepath:
            file_label.config(text=self.filepath.split("/")[-1])
            
            sheet_name.config(state=tk.NORMAL)
            btn_process.config(state=tk.NORMAL)
            messagebox.showinfo("Archivo seleccionado", "Archivo Excel cargado correctamente.")

    def clean_selection(self, file_label, sheet_name, btn_process, btn_save):
        self.filepath = None
        file_label.config(text="No se ha cargado ningún archivo.")
        sheet_name.delete(0, tk.END)  
        sheet_name.config(state=tk.DISABLED) 
        btn_process.config(state=tk.DISABLED)  
        btn_save.config(state=tk.DISABLED)  

    def process_file(self, sheet_name, btn_save, processing_label):
        sheet_name_text = sheet_name.get()

        if not sheet_name_text:
            messagebox.showerror("Error", "Debe ingresar el nombre de la hoja.")
            return

        processing_label.config(text="Procesando archivo...")
        processing_label.pack(pady=10)

        self.excel_handler = ExcelHandler(filename=self.filepath, sheet_name=sheet_name_text)
        self.excel_handler.read_excel()

        self.processor = DataProcessor(self.excel_handler)
        self.processor.process_data()

        self.df_results = self.processor.get_results_dataframe()
        btn_save.config(state=tk.NORMAL)

        messagebox.showinfo("Archivo procesado", "El archivo ha sido procesado correctamente.")

    def save_file(self, df_results):
        if df_results is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
            if save_path:
                messagebox.showinfo("Éxito", f"El archivo ha sido guardado en: {save_path}")
        else:
            messagebox.showerror("Error", "No hay resultados para guardar.")