import pandas as pd
import numpy as np
import json
import json2table
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index_one(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/output")
def upload_data(request: Request, File: UploadFile = File(...)):
    try:
        df = pd.read_csv(File.file, encoding='latin1')

        df["Daily Returns"] = df["Close"].pct_change()
        daily_volatility = df["Daily Returns"].std()

        length_data = len(df)
        annual_volatility = daily_volatility * np.sqrt(length_data)

        calculated_data = {
            "DataFrame": df.to_json(orient="records"),
            "Daily Volatility": daily_volatility,
            "Annual Volatility": annual_volatility
        }

        calculated_data['DataFrame'] = json.loads(calculated_data['DataFrame'])

        # print(calculated_data)
        return templates.TemplateResponse("output.html", {"request": request, "dataframe": calculated_data})
    
    except pd.errors.ParserError as e:
        error_message = f"Error parsing CSV file: {str(e)}"
        return templates.TemplateResponse("output.html", {"request": request, "json_data": error_message})
