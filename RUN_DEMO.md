# UKG Rest Client Demo Setup

## Prerequisites
- Python 3.11+
- pip package manager

## Step 1: Install Dependencies

```bash
# Install main dependencies
pip install -r requirements.txt

# Install mock server dependencies
cd mock_ukg_rest
pip install -r requirements.txt
cd ..
```

## Step 2: Start Services

### Terminal 1 - Mock UKG Server
```bash
cd mock_ukg_rest
python3 mock_server.py
```
Server runs on http://localhost:8080

### Terminal 2 - Union Entitlements Service
```bash
python3 union_entitlements_service.py
```
Service runs on http://localhost:8081

### Terminal 3 - Load Sample Data
```bash
cd mock_ukg_rest
python3 sample_data.py
```

## Step 3: Set Environment Variables

```bash
export UKG_APP_ID="test_app"
export UKG_APP_SECRET="test_secret"
export UKG_CLIENT_ID="test_client"
export UKG_COMPANY_SHORT_NAME="your_company_short_name"
export UKG_BASE_URL="http://localhost:8080"
```

## Step 4: Run Demos

### Basic UKG API Client Demo
```bash
python3 ukg_api_client.py
```

### Union Leave Workflow Demo
```bash
python3 union_leave_workflow.py
```

## Expected Output

The union leave workflow demonstrates:
- Time off request creation
- PTO plan retrieval
- Accrual balance verification
- Union entitlements checking
- Compliance violation monitoring

## Services Overview

- **Mock UKG Server** (port 8080): Simulates UKG Pro API endpoints
- **Union Entitlements Service** (port 8081): Provides union-specific data from SQLite database
- **UKG API Client**: Python client for consuming UKG services
- **Union Leave Workflow**: End-to-end workflow demonstrating union leave processing