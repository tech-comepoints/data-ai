import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List
from app.utils.config_loader import ConfigLoader

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

    def fetch_news_data(self) -> pd.DataFrame:
        """Fetch news data from NewsAPI"""
        try:
            # Construct the API URL
            url = 'https://newsapi.org/v2/top-headlines'
            
            # Set up the parameters
            params = {
                'language': 'en',
                'pageSize': 100,
                'apiKey': self.api_config['api_key']
            }

            # Make the request
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            # Convert to DataFrame
            if data['status'] == 'ok' and data['articles']:
                df = pd.DataFrame(data['articles'])
                
                # Process dates
                df['publishedAt'] = pd.to_datetime(df['publishedAt'])
                df['date'] = df['publishedAt'].dt.date
                
                # Extract source name
                df['source'] = df['source'].apply(lambda x: x['name'])
                
                # Add a default category if not present
                if 'category' not in df.columns:
                    df['category'] = 'general'
                
                return df
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return pd.DataFrame()

        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

    def categorize_data(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """Categorize news data based on configuration"""
        categories_config = self.config.get_categories_config()
        categorized_data = {}

        if df.empty:
            return categorized_data

        for cat_id, cat_config in categories_config.items():
            filter_col = cat_config['filter']['column']
            filter_val = cat_config['filter']['value']
            
            # For empty or missing category, put in 'general'
            if filter_col == 'category' and filter_col not in df.columns:
                categorized_data[cat_id] = df
            else:
                categorized_data[cat_id] = df[df[filter_col] == filter_val]

        return categorized_data

    def process_for_chart(self, df: pd.DataFrame, x_column: str, y_column: str) -> Dict:
        """Process data for visualization"""
        if df.empty:
            return {'x': [], 'y': [], 'type': 'bar'}

        if y_column == 'count':
            # Group by date and count articles
            chart_data = df.groupby(x_column).size().reset_index(name='count')
            return {
                'x': chart_data[x_column].tolist(),
                'y': chart_data['count'].tolist(),
                'type': 'bar'
            }
        else:
            return {
                'x': df[x_column].tolist(),
                'y': df[y_column].tolist(),
                'type': 'scatter'
            }