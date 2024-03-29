'''
Project: Market Analysis App
Author: Sushil Waghmare
Date started: 22-01-2024
Last updated: 22-01-2024
Organization: Finzome Technologies
Github Link: https://github.com/sushil1024/Market-Analysis-App
App Home Page Endpoint: https://market-analysis-app.onrender.com
Request Endpoint Link: https://market-analysis-app.onrender.com/output
Method: POST
Request Body (form-data):
    Key: File
    Value: ---Upload CSV File---
'''

import pandas as pd
import numpy as np
import json
import json2table
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index_one(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

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
