#!/usr/bin/env python3
"""
Sample data loader for mock UKG REST API
Populates the mock server with realistic test data
"""

import requests
import json
from datetime import datetime, timedelta

class MockDataLoader:
    def __init__(self, base_url='http://localhost:8080'):
        self.base_url = base_url
        self.token = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with mock server"""
        import base64
        credentials = base64.b64encode(b'test_app:test_secret').decode('utf-8')
        
        response = requests.post(
            f'{self.base_url}/api/v2/client/tokens',
            headers={'Authorization': f'Basic {credentials}'},
            data={'grant_type': 'client_credentials', 'scope': 'client', 'client_id': 'test_client'}
        )
        
        if response.status_code == 200:
            self.token = response.json()['access_token']
            print("✓ Authenticated with mock server")
        else:
            raise Exception(f"Authentication failed: {response.text}")
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    def load_sample_data(self):
        """Load comprehensive sample data into mock server"""
        
        # Create sample companies
        companies = [
            {
                'name': 'Acme Corporation',
                'industry': 'Technology',
                'size': 'Large',
                'location': 'San Francisco, CA'
            },
            {
                'name': 'Global Industries',
                'industry': 'Manufacturing',
                'size': 'Medium',
                'location': 'Detroit, MI'
            }
        ]
        
        company_ids = []
        for company in companies:
            response = requests.post(
                f'{self.base_url}/api/v2/client/companies',
                headers=self.get_headers(),
                json=company
            )
            if response.status_code == 201:
                company_ids.append(response.json()['id'])
                print(f"✓ Created company: {company['name']}")
        
        # Create sample employees
        employees = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@acme.com',
                'employee_id': 'EMP001',
                'company_id': company_ids[0] if company_ids else 'default',
                'department': 'Engineering',
                'job_title': 'Software Engineer',
                'hire_date': '2023-01-15',
                'status': 'active'
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@acme.com',
                'employee_id': 'EMP002',
                'company_id': company_ids[0] if company_ids else 'default',
                'department': 'HR',
                'job_title': 'HR Manager',
                'hire_date': '2022-06-01',
                'status': 'active'
            },
            {
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'email': 'bob.johnson@global.com',
                'employee_id': 'EMP003',
                'company_id': company_ids[1] if len(company_ids) > 1 else 'default',
                'department': 'Operations',
                'job_title': 'Operations Manager',
                'hire_date': '2021-03-10',
                'status': 'active'
            }
        ]
        
        employee_ids = []
        for employee in employees:
            response = requests.post(
                f'{self.base_url}/api/v2/client/employees',
                headers=self.get_headers(),
                json=employee
            )
            if response.status_code == 201:
                employee_ids.append(response.json()['id'])
                print(f"✓ Created employee: {employee['first_name']} {employee['last_name']}")
        
        # Create sample document types
        doc_types = [
            {
                'name': 'Employee Handbook',
                'description': 'Company employee handbook',
                'company_id': company_ids[0] if company_ids else 'default',
                'required': True
            },
            {
                'name': 'Tax Forms',
                'description': 'Employee tax documentation',
                'company_id': company_ids[0] if company_ids else 'default',
                'required': True
            }
        ]
        
        for doc_type in doc_types:
            response = requests.post(
                f'{self.base_url}/api/v2/client/documents/company-document-types',
                headers=self.get_headers(),
                json=doc_type
            )
            if response.status_code == 201:
                print(f"✓ Created document type: {doc_type['name']}")
        
        # Create sample time-off requests
        time_off_requests = [
            {
                'employee_id': employee_ids[0] if employee_ids else 'default',
                'type': 'vacation',
                'start_date': '2024-02-15',
                'end_date': '2024-02-19',
                'days_requested': 5,
                'reason': 'Family vacation',
                'status': 'pending'
            },
            {
                'employee_id': employee_ids[1] if len(employee_ids) > 1 else 'default',
                'type': 'sick',
                'start_date': '2024-01-20',
                'end_date': '2024-01-20',
                'days_requested': 1,
                'reason': 'Medical appointment',
                'status': 'approved'
            }
        ]
        
        for request in time_off_requests:
            response = requests.post(
                f'{self.base_url}/api/v2/client/time-off/requests',
                headers=self.get_headers(),
                json=request
            )
            if response.status_code == 201:
                print(f"✓ Created time-off request for employee: {request['employee_id']}")
        
        # Create sample timesheets
        timesheets = [
            {
                'employee_id': employee_ids[0] if employee_ids else 'default',
                'week_ending': '2024-01-26',
                'total_hours': 40.0,
                'regular_hours': 40.0,
                'overtime_hours': 0.0,
                'status': 'submitted'
            },
            {
                'employee_id': employee_ids[1] if len(employee_ids) > 1 else 'default',
                'week_ending': '2024-01-26',
                'total_hours': 38.5,
                'regular_hours': 38.5,
                'overtime_hours': 0.0,
                'status': 'approved'
            }
        ]
        
        for timesheet in timesheets:
            response = requests.post(
                f'{self.base_url}/api/v2/client/time-attendance/timesheets',
                headers=self.get_headers(),
                json=timesheet
            )
            if response.status_code == 201:
                print(f"✓ Created timesheet for employee: {timesheet['employee_id']}")
        
        # Create sample webhooks
        webhooks = [
            {
                'url': 'https://example.com/webhook/employee-created',
                'events': ['employee.created', 'employee.updated'],
                'active': True,
                'description': 'Employee change notifications'
            },
            {
                'url': 'https://example.com/webhook/timeoff',
                'events': ['timeoff.requested', 'timeoff.approved'],
                'active': True,
                'description': 'Time-off notifications'
            }
        ]
        
        for webhook in webhooks:
            response = requests.post(
                f'{self.base_url}/api/v2/client/webhooks',
                headers=self.get_headers(),
                json=webhook
            )
            if response.status_code == 201:
                print(f"✓ Created webhook: {webhook['description']}")
        
        print("\n✅ Sample data loading completed successfully!")
        print(f"Mock server is running at: {self.base_url}")
        print("You can now test your UKG API client against this mock server.")

if __name__ == '__main__':
    loader = MockDataLoader()
    loader.load_sample_data()