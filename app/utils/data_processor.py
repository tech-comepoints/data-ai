import pandas as pd
import requests
from datetime import datetime
from typing import Dict, List
from app.utils.config_loader import ConfigLoader, CategoryFilter

class DataProcessor:
    def __init__(self, config_loader: ConfigLoader):
        self.config = config_loader
        self.api_config = config_loader.get_api_config()
        self.categories_config = config_loader.get_categories_config()

    def fetch_data(self) -> pd.DataFrame:
        """Fetch data from configured API endpoint"""
        try:
            url = self.api_config['base_url'] + self.api_config['endpoints']['data']
            
            # Set up the parameters
            params = {
                'language': self.api_config['params']['language'],
                'pageSize': self.api_config['params']['pageSize'],
                'apiKey': self.api_config['api_key']
            }

            # Make the request
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            # Convert to DataFrame
            if data['status'] == 'ok' and data['articles']:
                df = pd.DataFrame(data['articles'])
                
                # Process dates
                df['publishedAt'] = pd.to_datetime(df['publishedAt'])
                df['date'] = df['publishedAt'].dt.date
                
                # Extract source name
                df['source'] = df['source'].apply(lambda x: x['name'])
                
                return df
            else:
                print(f"API Error: {data.get('message', 'Unknown error')}")
                return pd.DataFrame()

        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()

    def fetch_news_data(self) -> Dict[str, pd.DataFrame]:
        """Fetch news data from NewsAPI for each category"""
        categorized_data = {}
        
        try:
            base_url = self.api_config['base_url']
            endpoint = self.api_config['endpoints']['news']
            url = base_url + endpoint

            # Fetch data for each category
            for cat_id, cat_config in self.categories_config.items():
                category_filter = CategoryFilter(cat_config)
                
                # Set up the parameters
                params = {
                    'language': self.api_config['params']['language'],
                    'pageSize': self.api_config['params']['pageSize'],
                    'apiKey': self.api_config['api_key']
                }
                # Add category-specific parameters
                params.update(category_filter.get_query_params())

                # Make the request
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data['status'] == 'ok' and data['articles']:
                    df = pd.DataFrame(data['articles'])
                    
                    # Process dates
                    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
                    df['date'] = df['publishedAt'].dt.date
                    
                    # Extract source name
                    df['source'] = df['source'].apply(lambda x: x['name'])
                    
                    # Add category
                    df['category'] = cat_id
                    
                    categorized_data[cat_id] = df
                else:
                    print(f"API Error for category {cat_id}: {data.get('message', 'Unknown error')}")
                    categorized_data[cat_id] = pd.DataFrame()

        except Exception as e:
            print(f"Error fetching news data: {e}")
            return {cat: pd.DataFrame() for cat in self.categories_config.keys()}

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