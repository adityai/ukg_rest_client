import requests
from ukg_api_client import UKGAPIClient

UNION_ENTITLEMENT_SERVICE_BASE_URL="http://localhost:8081"

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

def verify_accrual_balances(accruals, required_days):
    total_balance = sum([accrual['current_balance'] for accrual in accruals['data']])
    return total_balance >= required_days

def evaluate_union_entitlements(entitlements, time_off_request):
    # Placeholder for actual evaluation logic
    return True

def check_compliance_violations(violations, time_off_request):
    # Placeholder for actual evaluation logic
    return True

def evaluate_compliance_parameters(compliance_parameters, time_off_request):
    # Placeholder for actual evaluation logic
    return True

if __name__ == "__main__":
    employee_id = "EMP001"
    start_date = "2025-12-05"
    end_date = "2026-02-05"
    
    # Create a time off request for 2 months of medical leave
    time_off_request_data = {
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "reason": "Medical Leave",
        "type": "Medical Leave"
    }
    api_client = UKGAPIClient()
    time_off_request = api_client.create_vacation_request(time_off_request_data)
    print("Time Off Request:", time_off_request)

    # Get PTO plans 
    pto_plans = api_client.get_pto_plans(employee_id)
    print("PTO Plans:", pto_plans)

    # Get accrual balances
    accruals = api_client.get_accrual_balances(employee_id, start_date, end_date)
    print("Accrual Balances:", accruals)

    # Verify that the employee has accrued at least 30 hours of PTO
    required_hours = 30
    has_accrued_pto = verify_accrual_balances(accruals, required_hours)
    if not has_accrued_pto:
        print(f"Employee {employee_id} does not have enough PTO accrued for the requested time period.")
    else:
        print(f"Employee {employee_id} has sufficient PTO accrued.")

    # Get union entitlements
    entitlements = get_union_entitlements(employee_id)
    print("Union Entitlements:", entitlements)

    # Evaluate union entitlements
    is_union_entitled = evaluate_union_entitlements(entitlements, time_off_request)
    if not is_union_entitled:
        print("Union entitlements do not allow for the requested time off.")
    else:
        print("Union entitlements allow for the requested time off.")
    
    # Get compliance violations
    violations = get_compliance_violations(employee_id, start_date, end_date)
    print("Compliance Violations:", violations)

    # Evaluate compliance violations
    is_compliant = check_compliance_violations(violations, time_off_request)
    if not is_compliant:
        print("Compliance violations prevent the requested time off.")
    else:
        print("No compliance violations prevent the requested time off.")

    # Get union_id from entitlements for compliance parameters
    union_id = entitlements[0].get("union_id", "XXXXXXXX")

    # Get compliance parameters for the union
    compliance_parameters = get_compliance_parameters(union_id)
    print("Compliance Parameters:", compliance_parameters)

    # Evaluate compliance parameters
    is_compliant = evaluate_compliance_parameters(compliance_parameters, time_off_request)
    if not is_compliant:
        print("Compliance parameters do not allow for the requested time off.")
    else:
        print("Compliance parameters allow for the requested time off.")
    
    # Approve the time off request if all checks pass
    if is_union_entitled and is_compliant and has_accrued_pto:
        print(api_client.approve_vacation_request(time_off_request['id'], "APPROVER_ID"))
        print("Time Off Request Approved")
    else:
        print("Time Off Request Rejected")
        