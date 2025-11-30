import requests
from ukg_api_client import UKGAPIClient

UNION_ENTITLEMENT_SERVICE_BASE_URL="http://localhost:8081"

def get_accrual_balances(employee_id, start_date, end_date):
    api_client = UKGAPIClient()
    return api_client.get_accrual_balances(employee_id, start_date, end_date)

def get_union_entitlements(employee_id):
    response = requests.get(
        f"{UNION_ENTITLEMENT_SERVICE_BASE_URL}/employees/{employee_id}/entitlements"
    )
    return response.json()

def get_compliance_violations(employee_id, start_date, end_date):
    response = requests.get(
        f"{UNION_ENTITLEMENT_SERVICE_BASE_URL}/employees/{employee_id}/violations"
    )
    return response.json()

def get_compliance_parameters(union_id):
    response = requests.get(
        f"{UNION_ENTITLEMENT_SERVICE_BASE_URL}/unions/{union_id}/compliance"
    )
    return response.json()

if __name__ == "__main__":
    # Example usage
    employee_id = "EMP001"
    start_date = "2023-01-01"
    end_date = "2023-12-31"
    
    entitlements = get_union_entitlements(employee_id)
    print("Union Entitlements:", entitlements)
    
    violations = get_compliance_violations(employee_id, start_date, end_date)
    print("Compliance Violations:", violations)
