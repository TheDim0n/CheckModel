import os

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .utils import test_model
from .config import settings


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():
    if not os.path.exists(settings.tmp_dir):
        os.mkdir(settings.tmp_dir)


@app.on_event("shutdown")
async def shutdown_event():
    if os.path.exists(settings.tmp_dir):
        os.rmdir(settings.tmp_dir)


@app.post("/results/", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    file_data = await file.read()
    accuracy = test_model(file_data=file_data, filename=file.filename)
    return templates.TemplateResponse(
        "results.html", 
        {
            "request": request, 
            "accuracy": accuracy,
            "model_name": file.filename,
        }
    )


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})