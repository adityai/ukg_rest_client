import requests
import base64
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from urllib.parse import urlencode
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UKGAPIClient:
    BASE_URL = 'http://localhost:8080'  # Mock server URL
    APP_ID = 'test_app'
    APP_SECRET = 'test_secret'
    CLIENT_ID = 'test_client'

    def get_access_token(self):
        auth_url = f"{self.BASE_URL}/api/v2/client/tokens"
        credentials = base64.b64encode(f'{self.APP_ID}:{self.APP_SECRET}'.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'client',
            'client_id': self.CLIENT_ID
        }
        
        response = requests.post(auth_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()['access_token']

    def list_companies(self):
        token = self.get_access_token()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{self.BASE_URL}/api/v2/client/companies", headers=headers)
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    client = UKGAPIClient()
    companies = client.list_companies()
    print(companies)
