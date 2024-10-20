import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from pdf_classifier.classifier import classify_pdf


@patch('pdf_classifier.classifier.extract_pdf_features')
@patch('joblib.load')
def test_classify_pdf_document(mock_load_model, mock_extract_features):
    """
    Test classify_pdf when the model predicts 'document'.
    Mocks the feature extraction and model prediction.
    """
    # Mock the model's prediction to return 'document'
    mock_model = MagicMock()
    # Simulate the prediction of "documents"
    mock_model.predict.return_value = ['documents']
    mock_load_model.return_value = mock_model  # Mock loading of the model

    # Mock feature extraction to return a valid pandas DataFrame
    mock_extract_features.return_value = pd.DataFrame([{
        'average_width': 600,
        'average_height': 800,
        'all_pages_rotated': 0,
        'average_word_count': 100
    }])

    # Test classification result
    result = classify_pdf('sample.pdf')
    assert result == 'document'  # Expected classification based on the mocked prediction


@patch('pdf_classifier.classifier.extract_pdf_features')
@patch('joblib.load')
def test_classify_pdf_powerpoint(mock_load_model, mock_extract_features):
    """
    Test classify_pdf when the model predicts 'powerpoint'.
    Mocks the feature extraction and model prediction.
    """
    # Mock the model's prediction to return 'powerpoint'
    mock_model = MagicMock()
    # Simulate the prediction of "powerpoint"
    mock_model.predict.return_value = ['powerpoint']
    mock_load_model.return_value = mock_model  # Mock loading of the model

    # Mock feature extraction to return a valid pandas DataFrame with correct
    # feature names
    mock_extract_features.return_value = pd.DataFrame([{
        'average_width': 1024,
        'average_height': 768,
        'all_pages_rotated': 1,
        'average_word_count': 50
    }])

    # Test classification result
    result = classify_pdf('sample.pdf')
    # Expected classification based on the mocked prediction
    assert result == 'powerpoint'


@patch('pdf_classifier.classifier.extract_pdf_features', return_value=None)
def test_classify_pdf_feature_extraction_failure(mock_extract_features):
    """
    Test classify_pdf when feature extraction fails.
    Mocks feature extraction to return None, simulating a failure.
    """
    # Test if ValueError is raised when feature extraction fails
    with pytest.raises(ValueError):
        classify_pdf('tests/test_pdfs/corrupted.pdf')
