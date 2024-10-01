    def __init__(self, root) -> None:
        self.excel_handler = None
        self.processor = None
        self.df_results = None
        self.filepath = None

        self.root = root
        
        # Colocar el ícono en la barra de título (Windows)
        icon_path = self.resource_path("src/icon/icon_tambo.ico")  # Cambiado para usar la función resource_path
        self.root.iconbitmap(icon_path)  # Debe ser un archivo .ico

        # Colocar el ícono en la barra de tareas y la ventana
        icon_image = Image.open(icon_path)  # Usar la misma ruta para el ícono
        icon_photo = ImageTk.PhotoImage(icon_image)
        self.root.iconphoto(False, icon_photo)
        
        self.interface()
        self.center_window(510, 260)
    
    def resource_path(self, relative_path):
        """Obtiene la ruta absoluta del recurso, funciona en modo empaquetado o en modo desarrollo."""
        try:
            # Si estamos empaquetados, PyInstaller guarda los archivos en _MEIPASS
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
    
        return os.path.join(base_path, relative_path)

    def interface(self):
        self.root.title("Tamaño ideal de pedido")
        self.root.geometry("500x300")

        label_instruction = tk.Label(self.root, text="Evaluación del tamaño ideal de pedido", font=("Helvetica", 16, "bold"))
        label_instruction.pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        btn_load = tk.Button(frame, text="Cargar archivo Excel", command=self.upload_file, font=("Helvetica", 11), bg="#d2b4de")
        btn_load.pack(side=tk.LEFT, padx=(0, 10))

        self.file_label = tk.Label(frame, text="No se ha cargado ningún archivo.")
        self.file_label.pack(side=tk.LEFT)
        
        btn_download = tk.Button(frame, text="Descargar plantilla", command=self.descargar_plantilla, font=("Helvetica", 11), bg="#d2b4de")
        btn_download.pack(side=tk.LEFT, padx=(0, 10))

        frame_actions = tk.Frame(self.root)
        frame_actions.pack(pady=10)

        self.btn_process = tk.Button(frame_actions, text="Procesar archivo", bg="#fcf3cf", command=self.process_file, state=tk.DISABLED, font=("Helvetica", 11))
        self.btn_process.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_save = tk.Button(frame_actions, text="Guardar archivo procesado", bg="#fcf3cf", command=self.save_file, state=tk.DISABLED, font=("Helvetica", 11))
        self.btn_save.pack(side=tk.LEFT, padx=10, pady=5)

        frame_clean = tk.Frame(self.root)
        frame_clean.pack(pady=10)

        btn_clean = tk.Button(frame_clean, text="Limpiar selección", bg="#f2d7d5", command=self.clean_selection, font=("Helvetica", 11))
        btn_clean.pack(side=tk.TOP, pady=5)
    

    def descargar_plantilla(self):
        plantilla_path = self.resource_path("src/plantilla/plantilla.xlsx")  # Cambia la ruta a tu plantilla usando resource_path
        
        if not os.path.exists(plantilla_path):
            messagebox.showerror("Error", "La plantilla no se encuentra en la ruta especificada.")
            return

        destino = filedialog.asksaveasfilename(
            title="Guardar Plantilla Como",
            defaultextension=".xlsx",  
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")]
        )

        if destino:
            try:
                shutil.copy(plantilla_path, destino)
                messagebox.showinfo("Éxito", f"Plantilla descargada correctamente en: {destino}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo descargar la plantilla: {str(e)}")

    def upload_file(self):
        self.filepath = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )

        if self.filepath:
            self.file_label.config(text=self.filepath.split("/")[-1])
            self.btn_process.config(state=tk.NORMAL)
            messagebox.showinfo("Archivo seleccionado", "Archivo Excel cargado correctamente.")

    def clean_selection(self):
        self.filepath = None
        self.file_label.config(text="No se ha cargado ningún archivo.")
        self.btn_process.config(state=tk.DISABLED)
        self.btn_save.config(state=tk.DISABLED)

    def process_file(self):
        self.processing_label = tk.Label(self.root, text="Procesando archivo...", font=("Helvetica", 10, "italic"))
        self.processing_label.pack(pady=10)

        self.root.after(100, self.message_load)
        self.root.after(3000, self.processing_label.pack_forget)

    def message_load(self):
        try:
            self.excel_handler = ExcelHandler(filename=self.filepath, sheet_name=0)
            self.excel_handler.read_excel()
            self.processor = DataProcessor(self.excel_handler)
            self.processor.process_data()
            self.df_results = self.processor.get_results_dataframe()
            self.btn_save.config(state=tk.NORMAL)
            messagebox.showinfo("Archivo procesado", "El archivo ha sido procesado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", "Error procesando el archivo: " + str(e))

    def save_file(self):
        if self.df_results is not None:
            save_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos Excel", "*.xlsx")])
            if save_path:
                self.processing_label = tk.Label(self.root, text="Guardando archivo...", font=("Helvetica", 10, "italic"))
                self.processing_label.pack(pady=10)
                self.root.after(100, lambda: self._guardar_archivo(save_path))
                self.root.after(3000, self.processing_label.pack_forget)
        else:
            messagebox.showerror("Error", "No hay resultados para guardar.")

    def _guardar_archivo(self, save_path):
        try:
            self.excel_handler.write_excel(self.df_results, save_path)
            self.file_label.config(text="No se ha cargado ningún archivo.")
            messagebox.showinfo("Éxito", f"El archivo ha sido guardado en: {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")