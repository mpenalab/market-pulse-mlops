import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os

def train():
    # 1. Configurar MLflow para que se conecte al servidor de Docker
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment("Market_Pulse_Model_Training")

    # 2. Cargar datos
    df = pd.read_csv("data/processed/cleaned_data.csv", index_col=0)
    
    # Crear variable objetivo: 1 si el precio sube mañana, 0 si baja
    df['Target'] = (df['Daily_Return'].shift(-1) > 0).astype(int)
    df.dropna(inplace=True)

    X = df[['MA7', 'MA21', 'Daily_Return']]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Iniciar experimento en MLflow
    with mlflow.start_run():
        n_estimators = 100
        model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
        model.fit(X_train, y_train)

        # Predicciones y métricas
        predictions = model.predict(X_test)
        acc = accuracy_score(y_test, predictions)

        # 4. Registrar parámetros, métricas y el modelo en MLflow
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_metric("accuracy", acc)

        # Opción B: Guardar manualmente como artefacto si la anterior falla
        import joblib
        model_path = "models/model.joblib"
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, model_path)
        
        # Subir el archivo directamente al servidor de MLflow
        mlflow.log_artifact(model_path, artifact_path="model_file")

        print(f"Entrenamiento completado con éxito. Accuracy: {acc:.4f}")
        print("Revisa los resultados en http://localhost:5000")

if __name__ == "__main__":
    train()