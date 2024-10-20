import logging
from typing import Dict, List
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from api.utils import validate_pdf, save_temp_file, clean_up_temp_file, classify_and_log

# Create the FastAPI instance
app = FastAPI()

# In-memory storage for classification results (for simplicity)
classification_results: List[Dict[str, str]] = []

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


class ClassificationResult(BaseModel):
    filename: str
    classification: str
    timestamp: str


@app.post("/classify/", response_model=ClassificationResult, summary="Upload and classify a PDF",
          description="Endpoint to upload and classify a PDF file. The file must be in PDF format.")
async def upload_pdf(file: UploadFile = File(...)) -> Dict[str, str]:
    """Endpoint to upload and classify a PDF."""
    validate_pdf(file)
    temp_file_path = save_temp_file(file)
    try:
        result = classify_and_log(
            temp_file_path,
            file.filename,
            classification_results)
    except Exception as e:
        logging.error(
            f"Error occurred while processing file '{
                file.filename}': {
                str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the file.",
        )
    finally:
        clean_up_temp_file(temp_file_path)
    return result


@app.get("/results/",
         response_model=List[ClassificationResult],
         summary="Retrieve classification results",
         description="Endpoint to retrieve the classification results of previously uploaded PDFs.")
async def retrieve_results() -> List[Dict[str, str]]:
    """Endpoint to retrieve classification results."""
    logging.info(
        f"Retrieving classification results, total: {
            len(classification_results)}")
    return classification_results

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
