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
        return self.make_request("POST", "time-off/requests", data=data)
    
    def get_vacation_request_by_id(self, request_id):
        response = requests.get(f"{self.BASE_URL}/api/v2/client/time-off/requests/{request_id}", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def approve_vacation_request(self, request_id, approver_id):
        data = {
            "approver_id": approver_id,
            "status": "approved"
        }
        return self.make_request("PUT", f"time-off/requests/{request_id}", data=data)
    
    def get_vacation_requests(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "time-off/requests", params=params)
    
    def get_payroll_runs(self):
        return self.make_request("GET", "payroll/runs")
    
    def create_payroll_runs(self, payroll_run_data):
        return self.make_request("POST", "payroll/runs", data=payroll_run_data)
    
    def create_pay_stubs(self, pay_stub_data):
        return self.make_request("POST", "payroll/pay-stubs", data=pay_stub_data)
    
    def get_pay_stubs(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "payroll/pay-stubs", params=params)
    
    def create_deduction(self, deduction_data):
        return self.make_request("POST", "payroll/deductions", data=deduction_data)

    def get_deductions(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "payroll/deductions", params=params)
    
    def create_tax(self, tax_data):
        return self.make_request("POST", "payroll/taxes", data=tax_data)

    def get_taxes(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "payroll/taxes", params=params)

    # EMPLOYEE & ORGANIZATION
    def list_employees(self, params = None):
        return self.make_request("GET", "employees", params=params)
    
    def create_employee(self, data):
        return self.make_request("POST", "employees", data=data)
    
    def get_employee_by_uuid(self, employee_uuid):
        return self.make_request("GET", f"employees/{employee_uuid}")
    
    def get_departments(self):
        return self.make_request("GET", "configuration/departments")
    
    def get_locations(self):
        return self.make_request("GET", "configuration/locations")
    
    def get_organization_hierarchy(self, company_id=None):
        params = {}
        if company_id:
            params['company_id'] = company_id
        return self.make_request("GET", "organization/hierarchy", params=params)
    
    def get_accrual_balances(self, employee_id, start_date, end_date):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        return self.make_request("GET", "time-off/accrual-balances", params=params)
    
    def get_pto_plans(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "time-off/pto-plans", params=params)
    
    def get_accrual_balances(self, employee_id, start_date, end_date):
        params = {
            'employee_id': employee_id,
            'start_date': start_date,
            'end_date': end_date
        }
        return self.make_request("GET", "time-off/accrual-balances", params=params)
    
    def get_pto_plans(self, employee_id):
        params = {}
        if employee_id:
            params['employee_id'] = employee_id
        return self.make_request("GET", "time-off/pto-plans", params=params)

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

    # Create deduction
    deduction_data = {
        "employee_id": "123",
        "name": "Health Insurance",
        "amount": 100
    }
    deduction = client.create_deduction(deduction_data=deduction_data)
    print("Created Deduction:", deduction)

    # Get deductions
    deductions = client.get_deductions(employee_id="123")
    print("Deductions:", deductions)
    
    # Create tax
    tax_data = {
        "employee_id": "123",
        "tax_type": "Federal Income Tax",
        "amount": 500.00,
        "taxable_amount": 40000.00
    }
    tax = client.create_tax(tax_data=tax_data)
    print("Created Tax:", tax)

    # Get taxes
    taxes = client.get_taxes(employee_id="123")
    print("Taxes:", taxes)

    # List employees
    employees = client.list_employees()
    print("Employees:", employees)

    # Get employee by ID (use the UUID id from the employee list)
    employee_uuid = employees['data'][0]['id']  # Get the first employee's UUID
    employee = client.get_employee_by_uuid(employee_uuid=employee_uuid)
    print("Employee:", employee)

    # Create employee
    new_employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "Y8TtQ@example.com",
        "phone": "123-456-7890",
        "address": "123 Main St, Anytown, USA",
        "city": "Anytown",
        "state": "CA",
        "zip_code": "12345",
        "country": "USA",
        "date_of_birth": "1990-01-01",
        "hire_date": "2022-01-01",
        "job_title": "Software Engineer",
        "department": "IT",
        "salary": 50000
    }
    new_employee = client.create_employee(data=new_employee_data)
    print("New Employee:", new_employee)
    
    # Get departments
    departments = client.get_departments()
    print("Departments:", departments)
    
    # Get locations
    locations = client.get_locations()
    print("Locations:", locations)
    
    # Get organization hierarchy
    org_hierarchy = client.get_organization_hierarchy()
    print("Organization Hierarchy:", org_hierarchy)
    