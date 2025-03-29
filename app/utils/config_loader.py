import os
import yaml
import operator
from typing import Dict, Any, List
import pandas as pd
from pathlib import Path

class ConfigLoader:
    def __init__(self):
        # Get the project root directory (data-ai)
        root_dir = Path(__file__).parent.parent.parent
        config_path = root_dir / 'config' / 'config.yaml'
        
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_api_config(self) -> Dict:
        return self.config['api']

    def get_dashboard_config(self) -> Dict:
        return self.config['dashboard']

    def get_categories_config(self) -> Dict:
        return self.config['categories']

class CategoryFilter:
    def __init__(self, category_config: Dict):
        self.name = category_config['name']
        self.filters = category_config['filters']

    def get_query_params(self) -> Dict[str, str]:
        """Convert filters list to a dictionary of query parameters"""
        params = {}
        for filter_dict in self.filters:
            params.update(filter_dict)
        return params

    def apply_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply filters to the DataFrame based on the query parameters"""
        # This method can be implemented if we need to filter the DataFrame
        # after fetching the data. Currently, filtering is done via API query params.
        return df