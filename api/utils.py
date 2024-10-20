import os
from fastapi import UploadFile, HTTPException
import logging
from typing import Dict, List
from datetime import datetime, timezone
from pdf_classifier.classifier import classify_pdf


def validate_pdf(file: UploadFile) -> None:
    """Validate that the uploaded file is a PDF."""
    if not file.filename.endswith(".pdf"):
        logging.error(f"Invalid file format attempted: {file.filename}")
        raise HTTPException(
            status_code=422,
            detail="Invalid file format. Only PDF files are allowed.")


def save_temp_file(file: UploadFile) -> str:
    """Save the uploaded file temporarily and return the file path."""
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(file.file.read())
    return temp_file_path


def clean_up_temp_file(file_path: str) -> None:
    """Remove the temporary file."""
    if os.path.exists(file_path):
        os.remove(file_path)
        logging.info(f"Temporary file '{file_path}' deleted.")


def classify_and_log(file_path: str,
                     filename: str,
                     classification_results: List[Dict[str,
                                                       str]]) -> Dict[str,
                                                                      str]:
    """Classify the PDF and log the result."""
    classification = classify_pdf(file_path)
    result = {
        "filename": filename,
        "classification": classification,
        # Use timezone-aware datetime
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    classification_results.append(result)
    logging.info(
        f"File '{filename}' classified successfully as '{classification}'")
    return result
