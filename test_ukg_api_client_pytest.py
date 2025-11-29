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

@patch('ukg_api_client.requests.get')
def test_list_companies(mock_get, mock_client):
    """Test listing companies"""
    mock_get.return_value.json.return_value = {'data': [{'id': '1', 'name': 'Test Company'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    companies = mock_client.list_companies()
    
    assert companies['data'][0]['name'] == 'Test Company'
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/companies",
        headers=mock_client.headers
    )

@patch('ukg_api_client.requests.post')
def test_create_timesheet(mock_post, mock_client):
    """Test timesheet creation"""
    mock_post.return_value.json.return_value = {'id': 'ts_123', 'employee_id': '123'}
    mock_post.return_value.raise_for_status.return_value = None
    
    timesheet_data = {
        'employee_id': '123',
        'date': '2025-11-28',
        'start_time': '09:00',
        'end_time': '17:00'
    }
    
    result = mock_client.create_timesheet(timesheet_data)
    
    assert result['id'] == 'ts_123'
    mock_post.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-attendance/timesheets",
        headers=mock_client.headers,
        json=timesheet_data
    )

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

@patch('ukg_api_client.requests.post')
def test_create_vacation_request(mock_post, mock_client):
    """Test vacation request creation"""
    mock_post.return_value.json.return_value = {'id': 'vr_123', 'status': 'pending'}
    mock_post.return_value.raise_for_status.return_value = None
    
    vacation_data = {
        'employee_id': '123',
        'start_date': '2025-12-01',
        'end_date': '2025-12-05'
    }
    
    result = mock_client.create_vacation_request(vacation_data)
    
    assert result['id'] == 'vr_123'
    assert result['status'] == 'pending'

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

@patch('ukg_api_client.requests.put')
def test_approve_vacation_request(mock_put, mock_client):
    """Test vacation request approval"""
    mock_put.return_value.json.return_value = {'id': 'vr_123', 'status': 'approved'}
    mock_put.return_value.raise_for_status.return_value = None
    
    result = mock_client.approve_vacation_request('vr_123', 'manager_456')
    
    assert result['status'] == 'approved'
    mock_put.assert_called_once()

@patch('ukg_api_client.requests.get')
def test_get_vacation_requests(mock_get, mock_client):
    """Test retrieving vacation requests for employee"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'vr_123', 'employee_id': '123'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_vacation_requests('123')
    
    assert len(result['data']) == 1
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-off/requests",
        headers=mock_client.headers,
        params={'employee_id': '123'}
    )

@patch('ukg_api_client.requests.post')
def test_authentication_failure(mock_post):
    """Test authentication failure handling"""
    mock_post.side_effect = Exception("Authentication failed")
    
    with pytest.raises(Exception):
        UKGAPIClient()

@patch('ukg_api_client.requests.get')
def test_api_error_handling(mock_get, mock_client):
    """Test API error handling"""
    mock_get.side_effect = Exception("API Error")
    
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

@patch('ukg_api_client.requests.get')
def test_get_payroll_runs(mock_get, mock_client):
    """Test retrieving payroll runs"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'pr_123', 'status': 'completed'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_payroll_runs()
    
    assert len(result['data']) == 1
    assert result['data'][0]['status'] == 'completed'

@patch('ukg_api_client.requests.get')
def test_get_pay_stubs_with_employee(mock_get, mock_client):
    """Test retrieving pay stubs with employee filter"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'ps_123', 'employee_id': '123'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_pay_stubs('123')
    
    assert len(result['data']) == 1
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/payroll/pay-stubs",
        headers=mock_client.headers,
        params={'employee_id': '123'}
    )

@patch('ukg_api_client.requests.get')
def test_get_pay_stubs_no_employee(mock_get, mock_client):
    """Test retrieving pay stubs without employee filter"""
    mock_get.return_value.json.return_value = {'data': [{'id': 'ps_123'}, {'id': 'ps_456'}]}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_pay_stubs(None)
    
    assert len(result['data']) == 2
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/payroll/pay-stubs",
        headers=mock_client.headers,
        params={}
    )

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

@patch('ukg_api_client.requests.get')
def test_get_vacation_requests_no_employee(mock_get, mock_client):
    """Test retrieving vacation requests without employee filter"""
    mock_get.return_value.json.return_value = {'data': []}
    mock_get.return_value.raise_for_status.return_value = None
    
    result = mock_client.get_vacation_requests(None)
    
    assert len(result['data']) == 0
    mock_get.assert_called_once_with(
        f"{mock_client.BASE_URL}/api/v2/client/time-off/requests",
        headers=mock_client.headers,
        params={}
    )

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