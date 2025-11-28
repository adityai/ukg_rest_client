# Mock UKG REST API Server

This directory contains a complete mock implementation of the UKG HR Service Delivery REST API v2 for testing purposes. The mock server implements all UKG endpoints, based on the documentation available at 'https://doc.people-doc.com/client/api/index-v2.html' without requiring access to the actual UKG developer portal.

## Features

- **Complete API Coverage**: All endpoints from `https://doc.people-doc.com/client/api/index-v2.html` are implemented
- **OAuth 2.0 Authentication**: Mock authentication flow with Bearer tokens
- **Realistic Responses**: Proper HTTP status codes and JSON response formats
- **In-Memory Storage**: Data persists during server runtime for testing
- **Sample Data**: Pre-populated test data for immediate testing
- **Error Handling**: Proper error responses for invalid requests

## Quick Start

### 1. Install Dependencies

```bash
cd mock_ukg_rest
pip install -r requirements.txt
```

### 2. Start the Mock Server

```bash
python mock_server.py
```

The server will start on `http://localhost:8080`

### 3. Load Sample Data (Optional)

In a new terminal:

```bash
python sample_data.py
```

### 4. Test Your Client

```bash
python test_client.py
```

## Create Your UKG API Client

Create your UKG API Client based on the example.

```python
import requests
import base64

BASE_URL = 'http://localhost:8080'  # Mock server URL
APP_ID = 'test_app'
APP_SECRET = 'test_secret'
CLIENT_ID = 'test_client'

# Step 1: Authenticate and get access token
def get_access_token():
    auth_url = f"{BASE_URL}/api/v2/client/tokens"
    credentials = base64.b64encode(f'{APP_ID}:{APP_SECRET}'.encode()).decode()
    
    headers = {
        'Authorization': f'Basic {credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = {
        'grant_type': 'client_credentials',
        'scope': 'client',
        'client_id': CLIENT_ID
    }
    
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()['access_token']

# Step 2: List companies
def list_companies():
    token = get_access_token()
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(f"{BASE_URL}/api/v2/client/companies", headers=headers)
    response.raise_for_status()
    return response.json()

# Usage
companies = list_companies()
print(companies)
```

## Implemented Endpoints

### Authentication
- `POST /api/v2/client/tokens` - OAuth token generation

### Document Management
- `GET/POST /api/v2/client/documents/company-document-types`
- `GET/PUT/DELETE /api/v2/client/documents/company-document-types/{id}`
- `GET/POST /api/v2/client/documents/company-documents`
- `GET/PUT/DELETE /api/v2/client/documents/company-documents/{id}`
- `GET/POST /api/v2/client/documents/company-folders`
- `GET/PUT/DELETE /api/v2/client/documents/company-folders/{id}`

### Employee Management
- `GET/POST /api/v2/client/employees`
- `GET/PUT/DELETE /api/v2/client/employees/{id}`

### Time & Attendance
- `GET/POST /api/v2/client/time-off/requests`
- `GET/PUT /api/v2/client/time-off/requests/{id}`
- `POST /api/v2/client/time-off/requests/{id}/approve`
- `POST /api/v2/client/time-off/requests/{id}/reject`
- `GET/POST /api/v2/client/time-attendance/timesheets`
- `GET/PUT /api/v2/client/time-attendance/timesheets/{id}`
- `GET /api/v2/client/time-attendance/attendance-records`

### Payroll
- `GET /api/v2/client/payroll/runs`
- `GET /api/v2/client/payroll/runs/{id}`
- `GET /api/v2/client/payroll/pay-stubs`
- `GET /api/v2/client/payroll/pay-stubs/{id}`
- `GET /api/v2/client/payroll/earnings`
- `GET /api/v2/client/payroll/deductions`
- `GET /api/v2/client/payroll/taxes`

### Company/Configuration
- `GET/POST /api/v2/client/companies`
- `GET/PUT /api/v2/client/companies/{id}`
- `GET /api/v2/client/configuration/departments`
- `GET /api/v2/client/configuration/departments/{id}`
- `GET /api/v2/client/configuration/job-titles`
- `GET /api/v2/client/configuration/locations`

### Benefits
- `GET /api/v2/client/benefits/plans`
- `GET /api/v2/client/benefits/plans/{id}`
- `GET /api/v2/client/employees/{id}/benefits`
- `GET /api/v2/client/employees/{id}/benefits/{benefit_id}`

### Reports
- `GET/POST /api/v2/client/reports`
- `GET /api/v2/client/reports/{id}`

### eSignature
- `GET/POST /api/v2/client/esignature/requests`
- `GET /api/v2/client/esignature/requests/{id}`
- `GET /api/v2/client/esignature/tasks`
- `GET /api/v2/client/esignature/tasks/{id}`

### Webhooks
- `GET/POST /api/v2/client/webhooks`
- `GET/PUT/DELETE /api/v2/client/webhooks/{id}`
- `POST /api/v2/client/webhooks/{id}/test`

### Bulk Operations
- `POST /api/v2/client/bulk/employees/import`
- `GET /api/v2/client/bulk/import-jobs`
- `GET /api/v2/client/bulk/import-jobs/{id}`

### Audit/Logging
- `GET /api/v2/client/audit/logs`
- `GET /api/v2/client/audit/logs/{id}`

### Organization Management
- `GET /api/v2/client/organization/units`
- `GET /api/v2/client/organization/units/{id}`
- `GET /api/v2/client/organization/hierarchy`

### Health Check
- `GET /api/v2/client/health`

## Authentication

The mock server uses a simplified OAuth 2.0 flow:

1. **Credentials**: Any application ID/secret combination works
2. **Token Request**: POST to `/api/v2/client/tokens` with Basic auth
3. **Access Token**: Use returned token in `Authorization: Bearer {token}` header

## Data Persistence

- Data is stored in memory and persists during server runtime
- Restart the server to reset all data
- Use `sample_data.py` to repopulate with test data

## Customization

### Adding Custom Data

Modify `sample_data.py` to add your specific test scenarios:

```python
# Add custom test data
custom_employee = {
    'first_name': 'Custom',
    'last_name': 'Employee',
    'email': 'custom@company.com',
    # ... other fields
}
```

### Modifying Responses

Edit `mock_server.py` to customize response formats or add validation:

```python
@app.route('/api/v2/client/employees', methods=['POST'])
def employees():
    # Add custom validation
    employee = request.json
    if not employee.get('email'):
        return jsonify({'error': 'Email is required'}), 400
    # ... rest of implementation
```

## Testing Scenarios

The mock server supports testing various scenarios:

1. **Success Cases**: All endpoints return successful responses
2. **Authentication**: Test with invalid tokens (401 responses)
3. **Not Found**: Test with non-existent IDs (404 responses)
4. **Validation**: Some endpoints validate required fields
5. **Pagination**: All list endpoints support cursor-based pagination

## Troubleshooting

### Server Won't Start
- Check if port 8080 is available
- Install required dependencies: `pip install -r requirements.txt`

### Authentication Fails
- Ensure you're using Basic auth for token endpoint
- Use any credentials (mock server accepts all)

### Client Connection Issues
- Verify server is running on `http://localhost:8080`
- Check firewall settings
- Ensure client is pointing to correct base URL

## Production Notes

⚠️ **This is a mock server for testing only**
- Do not use in production environments
- No data encryption or security measures
- No rate limiting or performance optimization
- Data is not persisted between restarts
