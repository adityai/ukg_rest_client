import requests
from ukg_api_client import UKGAPIClient

def get_accrual_balances(employee_id, start_date, end_date):
    api_client = UKGAPIClient()
    return api_client.get_accrual_balances(employee_id, start_date, end_date)

def get_union_entitlements(employee_id):
    api_client = UKGAPIClient()
    return api_client.get_union_entitlements(employee_id)

def get_compliance_violations(employee_id, start_date, end_date):
    api_client = UKGAPIClient()
    return api_client.get_compliance_violations(employee_id, start_date, end_date)

def get_compliance_parameters(union_id):
    api_client = UKGAPIClient()
    return api_client.get_compliance_parameters(union_id)
