import pytest
from app.utils.config_loader import ConfigLoader

def test_config_loading():
    config_loader = ConfigLoader()
    api_config = config_loader.get_api_config()
    assert 'base_url' in api_config
    assert 'endpoints' in api_config

def test_dashboard_config():
    config_loader = ConfigLoader()
    dashboard_config = config_loader.get_dashboard_config()
    assert 'title' in dashboard_config
    assert 'refresh_interval' in dashboard_config 