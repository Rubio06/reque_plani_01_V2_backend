from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import os
from src.services.service_excel_handler import ExcelHandler
from src.services.service_processor import DataProcessor
import decimal
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  
)


processed_file_path = None

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    global processed_file_path  # Usar la variable global

    try:
        os.makedirs("temp", exist_ok=True)

        file_location = f"temp/{file.filename.rsplit('.', 1)[0]}_RESULT.xlsx"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        excel_handler = ExcelHandler(filename=file_location)
        excel_handler.read_excel()

        processor = DataProcessor(excel_handler)
        processor.process_data()

        df_results = processor.get_results_dataframe()

        processed_file_path = file_location
        excel_handler.write_excel(df_results, processed_file_path)

        return JSONResponse(content={"message": "Archivo enviado correctamente"})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download-template")
async def download_template():
    template_path = "src/plantilla/plantilla.xlsx"
    if os.path.exists(template_path):
        return FileResponse(template_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="template.xlsx")
    else:
        raise HTTPException(status_code=404, detail="Template not found")


@app.get("/download-processed-file")
async def download_processed_file():
    global processed_file_path  # Usar la variable global
    if processed_file_path and os.path.exists(processed_file_path):
        return FileResponse(processed_file_path, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename="ARCHIVE_RESULT.xlsx")
    else:
        raise HTTPException(status_code=404, detail="Processed file not found")

