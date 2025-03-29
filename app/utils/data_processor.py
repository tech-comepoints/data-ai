import pandas as pd
from typing import Dict
import requests
from .config_loader import ConfigLoader, CategoryFilter

class DataProcessor:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader
        self.api_config = config_loader.get_api_config()
        self.categories_config = config_loader.get_categories_config()

    def fetch_data(self) -> pd.DataFrame:
        """Fetch data from configured API endpoint"""
        url = self.api_config['base_url'] + self.api_config['endpoints']['data']
        response = requests.get(url, headers=self.api_config['headers'])
        response.raise_for_status()
        return pd.DataFrame(response.json())

    def categorize_data(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Categorize data based on configuration"""
        categorized_data = {}
        for cat_id, cat_config in self.categories_config.items():
            category_filter = CategoryFilter(cat_config)
            categorized_data[cat_id] = category_filter.apply_filter(df)
        return categorized_data

    def process_for_chart(self, df: pd.DataFrame, x_column: str, y_column: str) -> Dict:
        """Process data for chart visualization"""
        return {
            'x': df[x_column].tolist(),
            'y': df[y_column].tolist(),
            'name': y_column
        }