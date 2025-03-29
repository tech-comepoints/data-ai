import pytest
import pandas as pd
from app.utils.data_processor import DataProcessor
from app.utils.config_loader import ConfigLoader

def test_data_categorization():
    config_loader = ConfigLoader()
    processor = DataProcessor(config_loader)
    
    # Create sample data
    test_data = pd.DataFrame({
        'value': [500, 1500, 50, 750],
        'date': pd.date_range(start='2024-01-01', periods=4)
    })
    
    categorized_data = processor.categorize_data(test_data)
    assert len(categorized_data) > 0 