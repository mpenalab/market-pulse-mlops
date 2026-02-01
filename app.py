from fastapi import FastAPI
import joblib
import pandas as pd
from pydantic import BaseModel

# Definir la estructura de la entrada
class MarketData(BaseModel):
    MA7: float
    MA21: float
    Daily_Return: float

# Inicializar la app
app = FastAPI(title="Market Pulse Predictor API")

# Cargar el modelo al iniciar
MODEL_PATH = "models/model.joblib"
model = joblib.load(MODEL_PATH)

@app.get("/")
def home():
    return {"message": "API de Predicción Market Pulse Activa"}

@app.post("/predict")
def predict(data: MarketData):
    # Convertir entrada a DataFrame (como espera scikit-learn)
    input_df = pd.DataFrame([data.model_dump()])
    
    # Realizar predicción
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df).max()
    
    return {
        "prediction": int(prediction),
        "label": "SUBE" if prediction == 1 else "BAJA",
        "confidence": round(float(probability), 2)
    }