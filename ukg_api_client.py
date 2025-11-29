import requests
import base64
import json
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from urllib.parse import urlencode
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UKGAPIClient:
    BASE_URL = os.getenv('UKG_BASE_URL', 'https://api.ultipro.com')  # Base URL for UKG API
    APP_ID = os.getenv('UKG_APP_ID')  # Your actual application ID
    APP_SECRET = os.getenv('UKG_APP_SECRET')  # Your actual application secret
    CLIENT_ID = os.getenv('UKG_CLIENT_ID')  # Your actual client ID
    COMPANY_SHORT_NAME = os.getenv('UKG_COMPANY_SHORT_NAME')  # Your company identifier

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
    
    def make_request(self, method, endpoint, params = None, data = None):
        url = f"{self.BASE_URL}/api/v2/client/{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=data)
        response.raise_for_status()
        return response.json()

    def list_companies(self):        
        return self.make_request("GET", "companies")
    
    def create_timesheet(self, data):
        return self.make_request("POST", "time-attendance/timesheets", data=data)
    
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
    
    def create_vacation_request(self, data):
        response = requests.post(f"{self.BASE_URL}/api/v2/client/time-off/requests", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_vacation_request_by_id(self, request_id):
        response = requests.get(f"{self.BASE_URL}/api/v2/client/time-off/requests/{request_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def approve_vacation_request(self, request_id, approver_id):
        data = {
            "approver_id": approver_id,
            "status": "approved"
        }
        response = requests.put(f"{self.BASE_URL}/api/v2/client/time-off/requests/{request_id}", headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_vacation_requests(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        response = requests.get(f"{self.BASE_URL}/api/v2/client/time-off/requests", headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_payroll_runs(self):
        response = requests.get(f"{self.BASE_URL}/api/v2/client/payroll/runs", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def create_payroll_runs(self, payroll_run_data):
        response = requests.post(f"{self.BASE_URL}/api/v2/client/payroll/runs", headers=self.headers, json=payroll_run_data)
        response.raise_for_status()
        return response.json()
    
    def create_pay_stubs(self, pay_stub_data):
        response = requests.post(f"{self.BASE_URL}/api/v2/client/payroll/pay-stubs", headers=self.headers, json=pay_stub_data)
        response.raise_for_status()
        return response.json()
    
    def get_pay_stubs(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        response = requests.get(f"{self.BASE_URL}/api/v2/client/payroll/pay-stubs", headers=self.headers, params=params)
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

    # Create a vacation request
    vacation_request_data = {
        "employee_id": "123",
        "start_date": "2025-12-01",
        "end_date": "2025-12-05",
        "reason": "Vacation",
        "notes": "Going on vacation"
    }
    vacation_request = client.create_vacation_request(data=vacation_request_data)
    print("Vacation Request:", vacation_request)

    # Get vacation request by ID
    vacation_request_by_id = client.get_vacation_request_by_id(request_id=vacation_request['id'])
    print("Vacation Request by ID:", vacation_request_by_id)

    # Get all vacation requests
    all_vacation_requests = client.get_vacation_requests(employee_id="123")
    print("All Vacation Requests:", all_vacation_requests)

    # Approve vacation request
    approved_vacation_request = client.approve_vacation_request(request_id=vacation_request['id'], approver_id="manager_4567")
    print("Approved Vacation Request:", approved_vacation_request)

    # Create payroll run
    payroll_run_data = {
        "payroll_period_start": "2025-11-01",
        "payroll_period_end": "2025-11-15",
        "employees": ["123", "456"]
    }
    payroll_run = client.create_payroll_runs(payroll_run_data=payroll_run_data)
    print("Created Payroll Run:", payroll_run)

    # Get payroll runs
    payroll_runs = client.get_payroll_runs()
    print("Payroll Runs:", payroll_runs)

    # Create pay stubs
    pay_stub_data = {
        "employee_id": "123",
        "pay_period_start": "2025-11-01",
        "pay_period_end": "2025-11-15",
        "gross_pay": 2000,
        "net_pay": 1500,
        "deductions": 500
    }
    pay_stub = client.create_pay_stubs(pay_stub_data=pay_stub_data)
    print("Created Pay Stub:", pay_stub)

    # Get pay stubs
    pay_stubs = client.get_pay_stubs(employee_id="123")
    print("Pay Stubs:", pay_stubs)