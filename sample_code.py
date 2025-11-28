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
