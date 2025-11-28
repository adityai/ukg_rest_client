#!/usr/bin/env python3
"""
Test script for UKG API Client against mock server
Demonstrates how to test the client with the mock service
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ukg_api_client import UKGAPIClient
import json

def test_ukg_client():
    """Test UKG API Client against mock server"""
    
    # Initialize client pointing to mock server
    client = UKGAPIClient(
        application_id='test_app',
        application_secret='test_secret',
        client_id='test_client',
        base_url='http://localhost:8080'
    )
    
    print("🧪 Testing UKG API Client against Mock Server")
    print("=" * 50)
    
    try:
        # Test health check
        print("\n1. Testing Health Check...")
        health = client.health_check()
        print(f"✓ Health check: {health['status']}")
        
        # Test listing companies
        print("\n2. Testing List Companies...")
        companies = client.list_companies()
        print(f"✓ Found {len(companies.get('data', []))} companies")
        
        # Test creating a company
        print("\n3. Testing Create Company...")
        new_company = client.create_company({
            'name': 'Test Company',
            'industry': 'Technology',
            'size': 'Small'
        })
        print(f"✓ Created company: {new_company['name']} (ID: {new_company['id']})")
        company_id = new_company['id']
        
        # Test getting company details
        print("\n4. Testing Get Company...")
        company_details = client.get_company(company_id)
        print(f"✓ Retrieved company: {company_details['name']}")
        
        # Test creating an employee
        print("\n5. Testing Create Employee...")
        new_employee = client.create_employee({
            'first_name': 'Test',
            'last_name': 'Employee',
            'email': 'test.employee@testcompany.com',
            'company_id': company_id,
            'employee_id': 'TEST001'
        })
        print(f"✓ Created employee: {new_employee['first_name']} {new_employee['last_name']} (ID: {new_employee['id']})")
        employee_id = new_employee['id']
        
        # Test listing employees
        print("\n6. Testing List Employees...")
        employees = client.list_employees()
        print(f"✓ Found {len(employees.get('data', []))} employees")
        
        # Test creating time-off request
        print("\n7. Testing Create Time-off Request...")
        time_off = client.create_time_off_request({
            'employee_id': employee_id,
            'type': 'vacation',
            'start_date': '2024-03-01',
            'end_date': '2024-03-05',
            'days_requested': 5,
            'reason': 'Spring break'
        })
        print(f"✓ Created time-off request (ID: {time_off['id']}, Status: {time_off['status']})")
        request_id = time_off['id']
        
        # Test approving time-off request
        print("\n8. Testing Approve Time-off Request...")
        approved = client.approve_time_off_request(request_id, {
            'approved_by': 'manager@testcompany.com',
            'notes': 'Approved for spring break'
        })
        print(f"✓ Approved time-off request (Status: {approved['status']})")
        
        # Test creating timesheet
        print("\n9. Testing Create Timesheet...")
        timesheet = client.create_timesheet({
            'employee_id': employee_id,
            'week_ending': '2024-02-02',
            'total_hours': 40.0,
            'regular_hours': 40.0,
            'overtime_hours': 0.0
        })
        print(f"✓ Created timesheet (ID: {timesheet['id']})")
        
        # Test creating document type
        print("\n10. Testing Create Document Type...")
        doc_type = client.create_document_type({
            'name': 'Test Document Type',
            'description': 'Test document for validation',
            'company_id': company_id,
            'required': False
        })
        print(f"✓ Created document type: {doc_type['name']} (ID: {doc_type['id']})")
        
        # Test creating webhook
        print("\n11. Testing Create Webhook...")
        webhook = client.create_webhook({
            'url': 'https://test.example.com/webhook',
            'events': ['employee.created', 'employee.updated'],
            'active': True,
            'description': 'Test webhook'
        })
        print(f"✓ Created webhook: {webhook['description']} (ID: {webhook['id']})")
        
        # Test webhook functionality
        print("\n12. Testing Webhook Test...")
        webhook_test = client.test_webhook(webhook['id'])
        print(f"✓ Webhook test: {webhook_test['status']}")
        
        # Test creating signature request
        print("\n13. Testing Create Signature Request...")
        sig_request = client.create_signature_request({
            'document_name': 'Test Contract',
            'signers': [{'email': 'test@example.com', 'name': 'Test Signer'}],
            'message': 'Please sign this test document'
        })
        print(f"✓ Created signature request (ID: {sig_request['id']}, Status: {sig_request['status']})")
        
        # Test creating report
        print("\n14. Testing Create Report...")
        report = client.create_report({
            'name': 'Employee Report',
            'type': 'employee_summary',
            'company_id': company_id,
            'parameters': {'include_inactive': False}
        })
        print(f"✓ Created report: {report['name']} (ID: {report['id']})")
        
        # Test bulk import
        print("\n15. Testing Bulk Employee Import...")
        bulk_job = client.create_bulk_employee_import({
            'file_url': 'https://example.com/employees.csv',
            'company_id': company_id,
            'options': {'update_existing': True}
        })
        print(f"✓ Created bulk import job (ID: {bulk_job['id']}, Status: {bulk_job['status']})")
        
        print("\n" + "=" * 50)
        print("🎉 All tests passed successfully!")
        print("✅ Mock UKG REST API is working correctly")
        print("✅ UKG API Client is compatible with the mock server")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = test_ukg_client()
    sys.exit(0 if success else 1)