from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from utils import test_model



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_data = await file.read()
    accuracy = test_model(file_data=file_data, filename=file.filename)
    return accuracy


@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})