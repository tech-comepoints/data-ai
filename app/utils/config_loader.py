import yaml
import operator
from typing import Dict, Any
import pandas as pd

class ConfigLoader:
    def __init__(self, config_path: str = "app/config/config.yaml"):
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
        self.filter_config = category_config['filter']

    def apply_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        column = self.filter_config['column']
        op = self.filter_config['operator']

        if op == '>':
            return df[df[column] > self.filter_config['threshold']]
        elif op == '<':
            return df[df[column] < self.filter_config['threshold']]
        elif op == 'between':
            range_min, range_max = self.filter_config['range']
            return df[(df[column] >= range_min) & (df[column] <= range_max)]
        else:
            raise ValueError(f"Unsupported operator: {op}")