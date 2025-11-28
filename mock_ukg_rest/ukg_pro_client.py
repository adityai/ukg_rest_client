#!/usr/bin/env python3
"""
UKG Pro API Client - Sample implementation for UKG Pro endpoints
"""

import requests
import base64
from typing import Dict, List, Optional

class UKGProClient:
    def __init__(self, base_url='http://localhost:8080', username='test', password='test'):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.token = self._authenticate()
    
    def _authenticate(self):
        """Authenticate and get token"""
        auth_url = f"{self.base_url}/api/v2/client/tokens"
        credentials = base64.b64encode(f'{self.username}:{self.password}'.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'client_credentials',
            'scope': 'client',
            'client_id': 'test_client'
        }
        
        response = requests.post(auth_url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()['access_token']
    
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
    
    # Personnel Information
    def get_employees(self):
        """Get all employees"""
        response = requests.get(f"{self.base_url}/personnel/v1/employees", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def get_employee(self, employee_id: str):
        """Get specific employee"""
        response = requests.get(f"{self.base_url}/personnel/v1/employees/{employee_id}", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Time Management
    def get_timecards(self):
        """Get timecards"""
        response = requests.get(f"{self.base_url}/timemanagement/v1/timecards", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    def create_timecard(self, data: Dict):
        """Create timecard"""
        response = requests.post(f"{self.base_url}/timemanagement/v1/timecards", 
                               json=data, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Payroll
    def get_paychecks(self):
        """Get paychecks"""
        response = requests.get(f"{self.base_url}/payroll/v1/paychecks", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Benefits
    def get_enrollments(self):
        """Get benefit enrollments"""
        response = requests.get(f"{self.base_url}/benefits/v1/enrollments", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Recruiting
    def get_jobs(self):
        """Get job postings"""
        response = requests.get(f"{self.base_url}/recruiting/v1/jobs", headers=self._get_headers())
        response.raise_for_status()
        return response.json()
    
    # Performance Management
    def get_reviews(self):
        """Get performance reviews"""
        response = requests.get(f"{self.base_url}/performance/v1/reviews", headers=self._get_headers())
        response.raise_for_status()
        return response.json()

if __name__ == '__main__':
    client = UKGProClient()
    
    print("Testing UKG Pro API endpoints:")
    print("Employees:", client.get_employees())
    print("Timecards:", client.get_timecards())
    print("Paychecks:", client.get_paychecks())
    print("Enrollments:", client.get_enrollments())
    print("Jobs:", client.get_jobs())
    print("Reviews:", client.get_reviews())