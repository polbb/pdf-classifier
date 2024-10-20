import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import logging
from pypdf import PdfReader
from typing import Optional, List, Dict

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)


def read_pdf_metadata(file_path: str) -> Dict[str, int]:
    """
    Read metadata from a PDF file.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns:
    - Dict[str, int]: A dictionary containing extracted metadata features.
    """
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            num_pages = len(reader.pages)

            # Extract page dimensions and rotations
            pages_info = [extract_page_info(page) for page in reader.pages]

            # Calculate features from pages info
            widths = [info['width'] for info in pages_info]
            heights = [info['height'] for info in pages_info]
            all_pages_rotated = all(info['rotated'] for info in pages_info)

            # Construct metadata features
            metadata = {
                'num_pages': num_pages,
                'average_width': int(sum(widths) / len(widths)) if widths else 0,
                'average_height': int(sum(heights) / len(heights)) if heights else 0,
                'all_pages_rotated': int(all_pages_rotated),
            }
            logging.info(
                f"Metadata extracted successfully for file '{file_path}'")
            return metadata
    except Exception as e:
        logging.error(
            f"Error reading PDF metadata from file '{file_path}': {
                str(e)}")
        raise


def extract_page_info(page) -> Dict[str, int]:
    """
    Extract page dimensions and rotation information.

    Parameters:
    - page: A page object from PyPDF.

    Returns:
    - Dict[str, int]: A dictionary containing page width, height, and rotation status.
    """
    try:
        mediabox = page.mediabox
        width = int(mediabox.width)
        height = int(mediabox.height)
        rotation = page.get('/Rotate') or 0

        page_info = {
            'width': width,
            'height': height,
            'rotated': int(rotation != 0)
        }
        logging.info(f"Page info extracted: {page_info}")
        return page_info
    except Exception as e:
        logging.error(f"Error extracting page info: {str(e)}")
        raise


def extract_text_features(file_path: str, num_pages: int) -> Dict[str, int]:
    """
    Extract text features from the first few pages of the PDF using OCR.

    Parameters:
    - file_path (str): Path to the PDF file.
    - num_pages (int): Number of pages in the PDF.

    Returns:
    - Dict[str, int]: A dictionary containing text-related features.
    """
    try:
        images = convert_from_path(
            file_path,
            first_page=1,
            last_page=min(10, num_pages)
        )

        total_words = sum(len(pytesseract.image_to_string(image).split())
                          for image in images)
        average_word_count = int(total_words / len(images)) if images else 0

        text_features = {
            'average_word_count': average_word_count
        }
        logging.info(
            f"Text features extracted successfully for file '{file_path}'")
        return text_features
    except Exception as e:
        logging.error(
            f"Error extracting text features from file '{file_path}': {
                str(e)}")
        raise


def extract_pdf_features(file_path: str) -> Optional[pd.DataFrame]:
    """
    Extract features from a PDF file for classification.

    Parameters:
    - file_path (str): Path to the PDF file.

    Returns:
    - pd.DataFrame or None: A DataFrame containing extracted features,
    or None if an error occurs.
    """
    try:
        # Extract metadata features
        metadata_features = read_pdf_metadata(file_path)

        # Extract text features
        text_features = extract_text_features(
            file_path, metadata_features['num_pages'])

        # Combine all features
        features = {**metadata_features, **text_features}

        # Create a DataFrame with the extracted features
        feature_names = [
            'average_width',
            'average_height',
            'all_pages_rotated',
            'average_word_count'
        ]
        features_df = pd.DataFrame([features], columns=feature_names)

        logging.info(f"Features extracted successfully for file '{file_path}'")

        return features_df

    except Exception as e:
        logging.error(f"Error processing file '{file_path}': {str(e)}")
        return None
