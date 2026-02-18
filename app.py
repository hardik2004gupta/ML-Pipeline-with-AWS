import os
import sys
import logging
from urllib.parse import urlparse

import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet

import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature


# ---------------------------
# Configuration
# ---------------------------

MLFLOW_TRACKING_URI = "http://ec2-16-16-211-129.eu-north-1.compute.amazonaws.com:5000/"
DATA_URL = "https://raw.githubusercontent.com/mlflow/mlflow/master/tests/datasets/winequality-red.csv"
RANDOM_STATE = 42


# ---------------------------
# Logging Setup
# ---------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------
# Evaluation Function
# ---------------------------

def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


# ---------------------------
# Main Execution
# ---------------------------

if __name__ == "__main__":

    # Set MLflow Tracking URI (set BEFORE start_run)
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    logger.info(f"MLflow Tracking URI: {mlflow.get_tracking_uri()}")

    # Read Dataset
    try:
        data = pd.read_csv(DATA_URL, sep=";")
        logger.info("Dataset loaded successfully.")
    except Exception as e:
        logger.exception("Failed to load dataset.")
        sys.exit(1)

    # Train-Test Split (Reproducible)
    train, test = train_test_split(data, test_size=0.25, random_state=RANDOM_STATE)

    train_x = train.drop("quality", axis=1)
    test_x = test.drop("quality", axis=1)
    train_y = train["quality"]
    test_y = test["quality"]

    # Hyperparameters from CLI
    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    # MLflow Experiment
    with mlflow.start_run():

        # Model
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=RANDOM_STATE)
        model.fit(train_x, train_y)

        # Predictions
        predictions = model.predict(test_x)

        # Metrics
        rmse, mae, r2 = eval_metrics(test_y, predictions)

        print(f"ElasticNet Model (alpha={alpha}, l1_ratio={l1_ratio})")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE: {mae:.4f}")
        print(f"R2: {r2:.4f}")

        # Log Params
        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)

        # Log Metrics
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)

        # Infer & Log Signature
        signature = infer_signature(train_x, predictions)

        tracking_scheme = urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_scheme != "file":
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                registered_model_name="ElasticnetWineModel",
                signature=signature
            )
        else:
            mlflow.sklearn.log_model(
                model,
                artifact_path="model",
                signature=signature
            )

        logger.info("Model logged successfully to MLflow.")
