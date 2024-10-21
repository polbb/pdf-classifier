import joblib
import os
import logging
from typing import Optional
from pdf_classifier.feature_extraction import extract_pdf_features

# Define the path to the model
MODEL_PATH: str = os.path.join(
    os.path.dirname(__file__), "models", "logistic_regression_model.pkl"
)

# Load the trained model
try:
    model = joblib.load(MODEL_PATH)
    logging.info(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    logging.error(f"Failed to load model from {MODEL_PATH}: {str(e)}")
    raise


def classify_pdf(file_path: str) -> str:
    """Classify the PDF based on its extracted features."""
    try:
        # Extract features from the PDF
        features_df = extract_pdf_features(file_path)

        # Check if features extraction was successful
        if features_df is None:
            raise ValueError(f"Failed to extract features from {file_path}")
        
        # Make a prediction using the loaded model
        prediction = model.predict(features_df)[0]
        logging.info(f"Prediction for file '{file_path}': {prediction}")

        return "document" if prediction == "documents" else "powerpoint"
    except Exception as e:
        logging.error(
            f"Error during classification of file '{file_path}': {
                str(e)}")
        raise
