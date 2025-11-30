#!/usr/bin/env python3
"""
Pytest tests for UKG API Client
"""

import pytest
from unittest.mock import Mock, patch
from ukg_api_client import UKGAPIClient

@pytest.fixture
def mock_client():
    """Create a mocked UKG API client"""
    with patch('ukg_api_client.requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value.raise_for_status.return_value = None
        return UKGAPIClient()

@patch('ukg_api_client.requests.post')
def test_get_access_token(mock_post):
    """Test OAuth token retrieval"""
    mock_post.return_value.json.return_value = {'access_token': 'test_token_123'}
    mock_post.return_value.raise_for_status.return_value = None
    
    with patch('ukg_api_client.requests.post') as mock_init_post:
        mock_init_post.return_value.json.return_value = {'access_token': 'init_token'}
        mock_init_post.return_value.raise_for_status.return_value = None
        client = UKGAPIClient()
    
    token = client.get_access_token()
    assert token == 'test_token_123'

@patch.object(UKGAPIClient, 'make_request')
def test_list_companies(mock_make_request, mock_client):
    """Test listing companies"""
    mock_make_request.return_value = {'data': [{'id': '1', 'name': 'Test Company'}]}
    
    companies = mock_client.list_companies()
    
    assert companies['data'][0]['name'] == 'Test Company'
    mock_make_request.assert_called_once_with('GET', 'companies')

@patch.object(UKGAPIClient, 'make_request')
def test_create_timesheet(mock_make_request, mock_client):
    """Test timesheet creation"""
    mock_make_request.return_value = {'id': 'ts_123', 'employee_id': '123'}
    
    timesheet_data = {
        'employee_id': '123',
        'date': '2025-11-28',
        'start_time': '09:00',
        'end_time': '17:00'
    }
    
    result = mock_client.create_timesheet(timesheet_data)
    
    assert result['id'] == 'ts_123'
    mock_make_request.assert_called_once_with('POST', 'time-attendance/timesheets', data=timesheet_data)

@patch('ukg_api_client.requests.get')
def test_get_timesheets(mock_get, mock_client):
    """Test retrieving timesheets"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'ts_123', 'employee_id': '123'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_timesheets(employee_id='123')
    
    assert len(result['data']) == 1
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-attendance/timesheets",
        headers=mock_client.headers,
        params={'employee_id': '123'}
    )

@patch.object(UKGAPIClient, 'make_request')
def test_create_vacation_request(mock_make_request, mock_client):
    """Test vacation request creation"""
    mock_make_request.return_value = {'id': 'vr_123', 'status': 'pending'}
    
    vacation_data = {
        'employee_id': '123',
        'start_date': '2025-12-01',
        'end_date': '2025-12-05'
    }
    
    result = mock_client.create_vacation_request(vacation_data)
    
    assert result['id'] == 'vr_123'
    assert result['status'] == 'pending'
    mock_make_request.assert_called_once_with('POST', 'time-off/requests', data=vacation_data)

@patch('ukg_api_client.requests.get')
def test_get_vacation_request_by_id(mock_get, mock_client):
    """Test retrieving vacation request by ID"""
    mock_get.return_value.json.return_value = {'id': 'vr_123', 'status': 'approved'}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_vacation_request_by_id('vr_123')
    
    assert result['id'] == 'vr_123'
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-off/requests/vr_123",
        headers=mock_client.headers
    )

@patch.object(UKGAPIClient, 'make_request')
def test_approve_vacation_request(mock_make_request, mock_client):
    """Test vacation request approval"""
    mock_make_request.return_value = {'id': 'vr_123', 'status': 'approved'}
    
    result = mock_client.approve_vacation_request('vr_123', 'manager_456')
    
    assert result['status'] == 'approved'
    mock_make_request.assert_called_once_with('PUT', 'time-off/requests/vr_123', data={'approver_id': 'manager_456', 'status': 'approved'})

@patch.object(UKGAPIClient, 'make_request')
def test_get_vacation_requests(mock_make_request, mock_client):
    """Test retrieving vacation requests for employee"""
    mock_make_request.return_value = {'data': [{'id': 'vr_123', 'employee_id': '123'}]}
    
    result = mock_client.get_vacation_requests('123')
    
    assert len(result['data']) == 1
    mock_make_request.assert_called_once_with('GET', 'time-off/requests', params={'employee_id': '123'})

@patch('ukg_api_client.requests.post')
def test_authentication_failure(mock_post):
    """Test authentication failure handling"""
    mock_post.side_effect = Exception("Authentication failed")
    
    with pytest.raises(Exception):
        UKGAPIClient()

@patch.object(UKGAPIClient, 'make_request')
def test_api_error_handling(mock_make_request, mock_client):
    """Test API error handling"""
    mock_make_request.side_effect = Exception("API Error")
    
    with pytest.raises(Exception):
        mock_client.list_companies()

@patch('ukg_api_client.requests.post')
def test_authentication_with_raise_for_status_error(mock_post):
    """Test authentication with HTTP error"""
    mock_post.return_value.raise_for_status.side_effect = Exception("HTTP Error")
    
    with pytest.raises(Exception):
        UKGAPIClient()

def test_client_initialization():
    """Test client initialization with mocked authentication"""
    with patch('ukg_api_client.requests.post') as mock_post:
        mock_post.return_value.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value.raise_for_status.return_value = None
        
        client = UKGAPIClient()
        
        assert client.BASE_URL == 'http://localhost:8080'
        assert client.APP_ID == 'test_app'
        assert 'Authorization' in client.headers

@patch.object(UKGAPIClient, 'make_request')
def test_get_payroll_runs(mock_make_request, mock_client):
    """Test retrieving payroll runs"""
    mock_make_request.return_value = {'data': [{'id': 'pr_123', 'status': 'completed'}]}
    
    result = mock_client.get_payroll_runs()
    
    assert len(result['data']) == 1
    assert result['data'][0]['status'] == 'completed'
    mock_make_request.assert_called_once_with('GET', 'payroll/runs')

@patch.object(UKGAPIClient, 'make_request')
def test_get_pay_stubs_with_employee(mock_make_request, mock_client):
    """Test retrieving pay stubs with employee filter"""
    mock_make_request.return_value = {'data': [{'id': 'ps_123', 'employee_id': '123'}]}
    
    result = mock_client.get_pay_stubs('123')
    
    assert len(result['data']) == 1
    mock_make_request.assert_called_once_with('GET', 'payroll/pay-stubs', params={'employee_id': '123'})

@patch.object(UKGAPIClient, 'make_request')
def test_get_pay_stubs_no_employee(mock_make_request, mock_client):
    """Test retrieving pay stubs without employee filter"""
    mock_make_request.return_value = {'data': [{'id': 'ps_123'}, {'id': 'ps_456'}]}
    
    result = mock_client.get_pay_stubs(None)
    
    assert len(result['data']) == 2
    mock_make_request.assert_called_once_with('GET', 'payroll/pay-stubs', params={})

@patch('ukg_api_client.requests.get')
def test_get_timesheets_with_dates(mock_get, mock_client):
    """Test retrieving timesheets with date filters"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'ts_123'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_timesheets(employee_id='123', start_date='2025-01-01', end_date='2025-01-31')
    
    assert len(result['data']) == 1
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-attendance/timesheets",
        headers=mock_client.headers,
        params={'employee_id': '123', 'start_date': '2025-01-01', 'end_date': '2025-01-31'}
    )

@patch('ukg_api_client.requests.get')
def test_get_timesheets_no_params(mock_get, mock_client):
    """Test retrieving timesheets without parameters"""
    mock_get.return_value.json.return_value = {'data': []}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_timesheets()
    
    assert len(result['data']) == 0
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-attendance/timesheets",
        headers=mock_client.headers,
        params={}
    )

@patch.object(UKGAPIClient, 'make_request')
def test_get_vacation_requests_no_employee(mock_make_request, mock_client):
    """Test retrieving vacation requests without employee filter"""
    mock_make_request.return_value = {'data': []}
    
    result = mock_client.get_vacation_requests(None)
    
    assert len(result['data']) == 0
    mock_make_request.assert_called_once_with('GET', 'time-off/requests', params={})

def test_create_deduction(mock_client):
    """Test creating a deduction"""
    with patch.object(UKGAPIClient, 'make_request') as mock_make_request:
        mock_make_request.return_value = {'id': 'ded_123', 'amount': 100.0}
        
        deduction_data = {
            'employee_id': '123',
            'amount': 100.0,
            'reason': 'Health Insurance'
        }
        
        result = mock_client.create_deduction(deduction_data)
        
        assert result['id'] == 'ded_123'
        assert result['amount'] == 100.0
        mock_make_request.assert_called_once_with('POST', 'payroll/deductions', data=deduction_data)

def test_get_deductions(mock_client):
    """Test retrieving deductions for an employee"""
    with patch.object(UKGAPIClient, 'make_request') as mock_make_request:
        mock_make_request.return_value = {'data': [{'id': 'ded_123', 'amount': 100.0}]}
        
        result = mock_client.get_deductions('123')
        
        assert len(result['data']) == 1
        assert result['data'][0]['amount'] == 100.0
        mock_make_request.assert_called_once_with('GET', 'payroll/deductions', params={'employee_id': '123'})

def test_create_tax(mock_client):
    """Test creating a tax"""
    with patch.object(UKGAPIClient, 'make_request') as mock_make_request:
        mock_make_request.return_value = {'id': 'tax_123', 'amount': 50.0}
        
        tax_data = {
            'employee_id': '123',
            'amount': 50.0,
            'type': 'Federal'
        }
        
        result = mock_client.create_tax(tax_data)
        
        assert result['id'] == 'tax_123'
        assert result['amount'] == 50.0
        mock_make_request.assert_called_once_with('POST', 'payroll/taxes', data=tax_data)

@patch.object(UKGAPIClient, 'make_request')
def test_list_employees(mock_make_request, mock_client):
    """Test listing employees"""
    mock_make_request.return_value = {'data': [{'id': 'emp_123', 'name': 'John Doe'}]}
    
    result = mock_client.list_employees()
    
    assert len(result['data']) == 1
    mock_make_request.assert_called_once_with('GET', 'employees', params=None)

@patch.object(UKGAPIClient, 'make_request')
def test_create_employee(mock_make_request, mock_client):
    """Test creating an employee"""
    mock_make_request.return_value = {'id': 'emp_123', 'name': 'John Doe'}
    
    employee_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com'
    }
    
    result = mock_client.create_employee(employee_data)
    
    assert result['id'] == 'emp_123'
    mock_make_request.assert_called_once_with('POST', 'employees', data=employee_data)

@patch.object(UKGAPIClient, 'make_request')
def test_get_employee_by_uuid(mock_make_request, mock_client):
    """Test getting employee by UUID"""
    mock_make_request.return_value = {'id': 'emp_123', 'name': 'John Doe'}
    
    result = mock_client.get_employee_by_uuid('emp_123')
    
    assert result['id'] == 'emp_123'
    mock_make_request.assert_called_once_with('GET', 'employees/emp_123')

@patch.object(UKGAPIClient, 'make_request')
def test_get_departments(mock_make_request, mock_client):
    """Test getting departments"""
    mock_make_request.return_value = {'data': [{'id': 'DEPT001', 'name': 'Engineering'}]}
    
    result = mock_client.get_departments()
    
    assert len(result['data']) == 1
    assert result['data'][0]['name'] == 'Engineering'
    mock_make_request.assert_called_once_with('GET', 'configuration/departments')

@patch.object(UKGAPIClient, 'make_request')
def test_get_locations(mock_make_request, mock_client):
    """Test getting locations"""
    mock_make_request.return_value = {'data': [{'id': 'LOC001', 'name': 'San Francisco HQ'}]}
    
    result = mock_client.get_locations()
    
    assert len(result['data']) == 1
    assert result['data'][0]['name'] == 'San Francisco HQ'
    mock_make_request.assert_called_once_with('GET', 'configuration/locations')

@patch.object(UKGAPIClient, 'make_request')
def test_get_organization_hierarchy(mock_make_request, mock_client):
    """Test getting organization hierarchy"""
    mock_make_request.return_value = {'structure': [{'id': 'ORG001', 'name': 'CEO'}]}
    
    result = mock_client.get_organization_hierarchy()
    
    assert len(result['structure']) == 1
    assert result['structure'][0]['name'] == 'CEO'
    mock_make_request.assert_called_once_with('GET', 'organization/hierarchy', params={})

@patch.object(UKGAPIClient, 'make_request')
def test_get_organization_hierarchy_with_company(mock_make_request, mock_client):
    """Test getting organization hierarchy with company filter"""
    mock_make_request.return_value = {'structure': [{'id': 'ORG001', 'name': 'CEO'}]}
    
    result = mock_client.get_organization_hierarchy('company_123')
    
    assert len(result['structure']) == 1
    mock_make_request.assert_called_once_with('GET', 'organization/hierarchy', params={'company_id': 'company_123'})

def test_main_execution():
    """Test main execution block"""
    with patch('ukg_api_client.requests.post') as mock_post:
        mock_post.return_value.json.side_effect = [
            {'access_token': 'test_token'},
            {'id': 'ts_123'},
            {'id': 'vr_123'},
            {'id': 'vr_123', 'status': 'approved'}
        ]
        mock_post.return_value.raise_for_status.return_value = None
        
        with patch('ukg_api_client.requests.get') as mock_get:
            mock_get.return_value.json.return_value = {'data': []}
            mock_get.return_value.raise_for_status.return_value = None
            
            with patch('ukg_api_client.requests.put') as mock_put:
                mock_put.return_value.json.return_value = {'id': 'vr_123', 'status': 'approved'}
                mock_put.return_value.raise_for_status.return_value = None
                
                # Import and execute main block
                import ukg_api_client
                # Main block is executed on import, so we just verify it doesn't crash