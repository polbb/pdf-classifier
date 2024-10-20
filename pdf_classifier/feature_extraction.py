import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import logging
from pypdf import PdfReader
from typing import Optional

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def extract_pdf_features(file_path: str) -> Optional[pd.DataFrame]:
    """
    Extract features from a PDF file for classification.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns: - pd.DataFrame or None: A DataFrame containing extracted features,
    or None if an error occurs.
    """
    try:
        # Initialize the features dictionary
        features = {}

        # Read the PDF to extract metadata
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)
            features['num_pages'] = num_pages

            # Extract page dimensions and rotations
            widths = []
            heights = []
            all_pages_rotated = True

            # Iterate over each page to extract dimensions and rotation
            for page in reader.pages:
                mediabox = page.mediabox
                widths.append(int(mediabox.width))
                heights.append(int(mediabox.height))

                rotation = page.get('/Rotate') or 0
                if rotation == 0:
                    all_pages_rotated = False

            # Calculate average width and height
            features['average_width'] = int(sum(widths) / len(widths))
            features['average_height'] = int(sum(heights) / len(heights))
            features['all_pages_rotated'] = int(all_pages_rotated)

        # Extract text from the first 10 pages using OCR
        images = convert_from_path(
            file_path, first_page=1, last_page=min(
                10, num_pages))
        total_words = sum(len(pytesseract.image_to_string(image).split())
                          for image in images)

        # Calculate average word count
        average_word_count = int(total_words / len(images)) if images else 0
        features['average_word_count'] = average_word_count

        # Create a DataFrame with the extracted features
        feature_names = [
            'average_width',
            'average_height',
            'all_pages_rotated',
            'average_word_count']
        features_df = pd.DataFrame([features], columns=feature_names)
        logging.info(f"Features extracted successfully for file '{file_path}'")

        return features_df

    except Exception as e:
        logging.error(f"Error processing file '{file_path}': {str(e)}")
        return None
