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

    def __init__(self):
        token = self.get_access_token()
        
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }


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
        response = requests.get(f"{self.BASE_URL}/api/v2/client/companies", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_timesheet(self, data):
        
        response = requests.post(f"{self.BASE_URL}/api/v2/client/time-attendance/timesheets", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_timesheets(self, employee_id: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        response = requests.get(f"{self.BASE_URL}/api/v2/client/time-attendance/timesheets", headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    client = UKGAPIClient()
    companies = client.list_companies()
    print(companies)

    # Create a timesheet for today
    timesheet_data = {
        "employee_id": "123",
        "date": "2025-11-28",
        "start_time": "09:00",
        "end_time": "17:00",
        "notes": "Test today's timesheet"
    }
    timesheet = client.create_timesheet(data=timesheet_data)

    print("Get Timesheet:", timesheet)
    # Fetch timesheet for today
    timesheets = client.get_timesheets(employee_id="123", start_date="2025-11-28", end_date="2025-11-28")
    print("Timesheet for 2025-11-28:", timesheets)
    