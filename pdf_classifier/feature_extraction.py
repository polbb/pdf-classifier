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


def read_pdf_metadata(file_path: str, num_pages_to_check: int) -> Dict[str, int]:
    """
    Read metadata from a PDF file for the first few pages.

    Parameters:
    - file_path (str): Path to the PDF file.
    - num_pages_to_check (int): Number of pages to consider for metadata extraction.

    Returns:
    - Dict[str, int]: A dictionary containing extracted metadata features.
    """
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            logging.info(f"Total pages: {total_pages}")

            # Extract metadata from the first 'num_pages_to_check' pages or fewer if total pages are less
            pages_to_check = min(num_pages_to_check, total_pages)
            logging.info(f"Checking {pages_to_check} pages")
            pages_info = [_extract_page_info(reader.pages[i]) for i in range(pages_to_check)]

            # Extract rotation information for all pages
            all_pages_rotated = all((page.get('/Rotate') or 0) != 0 for page in reader.pages)
            logging.info(f"All pages rotated: {all_pages_rotated}")

            # Calculate features from pages info
            widths = [info['width'] for info in pages_info]
            heights = [info['height'] for info in pages_info]

            # Construct metadata features
            metadata = {
                'num_pages': total_pages,
                'average_width': int(sum(widths) / len(widths)) if widths else 0,
                'average_height': int(sum(heights) / len(heights)) if heights else 0,
                'all_pages_rotated': int(all_pages_rotated),
            }
            logging.info(f"Metadata extracted successfully for file '{file_path}'")
            return metadata
    except Exception as e:
        logging.error(f"Error reading PDF metadata from file '{file_path}': {str(e)}")
        raise


def _extract_page_info(page) -> Dict[str, int]:
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


def extract_text_features(file_path: str, num_pages_to_check: int) -> Dict[str, int]:
    """
    Extract text features from the first few pages of the PDF using OCR.

    Parameters:
    - file_path (str): Path to the PDF file.
    - num_pages_to_check (int): Number of pages in the PDF to consider for OCR.

    Returns:
    - Dict[str, int]: A dictionary containing text-related features.
    """
    try:
        images = convert_from_path(
            file_path,
            first_page=1,
            last_page=min(num_pages_to_check, num_pages_to_check)
        )

        total_words = sum(len(pytesseract.image_to_string(image).split()) for image in images)
        average_word_count = int(total_words / len(images)) if images else 0

        text_features = {
            'average_word_count': average_word_count
        }
        logging.info(f"Text features extracted successfully for file '{file_path}'")
        return text_features
    except Exception as e:
        logging.error(f"Error extracting text features from file '{file_path}': {str(e)}")
        raise


def extract_pdf_features(file_path: str, num_pages_to_check: int = 10) -> Optional[pd.DataFrame]:
    """
    Extract features from a PDF file for classification.

    Parameters:
    - file_path (str): Path to the PDF file.
    - num_pages_to_check (int, optional): Number of pages to consider for feature extraction (default: 10).

    Returns:
    - pd.DataFrame or None: A DataFrame containing extracted features,
    or None if an error occurs.
    """
    try:
        # Extract metadata features for the specified number of pages or fewer
        metadata_features = read_pdf_metadata(file_path, num_pages_to_check)

        # Extract text features for the specified number of pages or fewer
        text_features = extract_text_features(file_path, min(num_pages_to_check, metadata_features['num_pages']))

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

        logging.info(f"Features extracted successfully for file '{file_path}':\n{features_df.to_string(index=False)}")

        return features_df

    except Exception as e:
        logging.error(f"Error processing file '{file_path}': {str(e)}")
        return None
