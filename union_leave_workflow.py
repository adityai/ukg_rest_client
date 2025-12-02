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
    print("\n" + "="*60)
    print("🏥 UNION LEAVE WORKFLOW DEMO")
    print("="*60)
    
    employee_id = "EMP001"
    start_date = "2025-12-05"
    end_date = "2026-02-05"
    
    print(f"\n📋 Processing leave request for Employee: {employee_id}")
    print(f"📅 Leave Period: {start_date} to {end_date}")
    
    # Create a time off request for 2 months of medical leave
    time_off_request_data = {
        "employee_id": employee_id,
        "start_date": start_date,
        "end_date": end_date,
        "reason": "Medical Leave",
        "type": "Medical Leave"
    }
    
    print("\n🔄 Step 1: Creating Time Off Request...")
    api_client = UKGAPIClient()
    time_off_request = api_client.create_vacation_request(time_off_request_data)
    print(f"✅ Request ID: {time_off_request['id']}")
    print(f"📝 Status: {time_off_request['status'].upper()}")

    print("\n🔄 Step 2: Checking PTO Plans...")
    pto_plans = api_client.get_pto_plans(employee_id)
    for plan in pto_plans['data']:
        print(f"📊 {plan['name']}: {plan['accrual_rate']} hrs/month, Max: {plan['max_balance']} hrs")

    print("\n🔄 Step 3: Verifying Accrual Balances...")
    accruals = api_client.get_accrual_balances(employee_id, start_date, end_date)
    for accrual in accruals['data']:
        print(f"💰 {accrual['accrual_type'].title()}: {accrual['current_balance']} hrs available")

    required_hours = 30
    has_accrued_pto = verify_accrual_balances(accruals, required_hours)
    if has_accrued_pto:
        print(f"✅ Sufficient PTO balance (≥{required_hours} hrs required)")
    else:
        print(f"❌ Insufficient PTO balance (≥{required_hours} hrs required)")

    print("\n🔄 Step 4: Checking Union Entitlements...")
    entitlements = get_union_entitlements(employee_id)
    for ent in entitlements:
        print(f"🏛️ {ent['description']}: {ent['current_balance']} {ent['unit']} available")

    is_union_entitled = evaluate_union_entitlements(entitlements, time_off_request)
    print(f"{'✅' if is_union_entitled else '❌'} Union entitlements {'approved' if is_union_entitled else 'denied'}")
    
    print("\n🔄 Step 5: Reviewing Compliance Violations...")
    violations = get_compliance_violations(employee_id, start_date, end_date)
    if violations:
        for violation in violations:
            status = "✅ Resolved" if violation['resolved'] else "⚠️ Active"
            print(f"📋 {violation['violation_type']}: {status}")
    else:
        print("✅ No compliance violations found")

    is_compliant_violations = check_compliance_violations(violations, time_off_request)
    print(f"{'✅' if is_compliant_violations else '❌'} Compliance violations check {'passed' if is_compliant_violations else 'failed'}")

    print("\n🔄 Step 6: Evaluating Compliance Parameters...")
    union_id = entitlements[0].get("union_id", "UNION001")
    compliance_parameters = get_compliance_parameters(union_id)
    for param in compliance_parameters:
        print(f"📏 {param['parameter_name']}: {param['parameter_value']} ({param['description']})")

    is_compliant_params = evaluate_compliance_parameters(compliance_parameters, time_off_request)
    print(f"{'✅' if is_compliant_params else '❌'} Compliance parameters {'satisfied' if is_compliant_params else 'violated'}")
    
    print("\n" + "="*60)
    print("🎯 FINAL DECISION")
    print("="*60)
    
    all_checks_passed = is_union_entitled and is_compliant_violations and is_compliant_params and has_accrued_pto
    
    if all_checks_passed:
        print("\n🔄 Approving time off request...")
        approval = api_client.approve_vacation_request(time_off_request['id'], "MANAGER_001")
        print(f"🎉 TIME OFF REQUEST APPROVED!")
        print(f"✅ Approved by: MANAGER_001")
        print(f"📅 Effective: {start_date} to {end_date}")
    else:
        print(f"\n❌ TIME OFF REQUEST REJECTED")
        print("📋 Failed checks:")
        if not has_accrued_pto: print("   • Insufficient PTO balance")
        if not is_union_entitled: print("   • Union entitlements not met")
        if not is_compliant_violations: print("   • Active compliance violations")
        if not is_compliant_params: print("   • Compliance parameters violated")
    
    print("\n" + "="*60)
    print("✨ WORKFLOW COMPLETE")
    print("="*60 + "\n")
        