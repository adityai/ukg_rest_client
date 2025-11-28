#!/usr/bin/env python3
"""
Mock UKG REST API Server
Implements all endpoints from ukg_api_client.py for testing purposes
"""

from flask import Flask, request, jsonify, make_response
from datetime import datetime, timedelta
import uuid
import base64
import json
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Mock data storage
mock_data = {
    'tokens': {},
    'companies': {},
    'employees': {},
    'document_types': {},
    'company_documents': {},
    'company_folders': {},
    'time_off_requests': {},
    'timesheets': {},
    'attendance_records': {},
    'payroll_runs': {},
    'pay_stubs': {},
    'earnings': {},
    'deductions': {},
    'taxes': {},
    'departments': {},
    'job_titles': {},
    'locations': {},
    'benefits': {},
    'employee_benefits': {},
    'reports': {},
    'signature_requests': {},
    'signature_tasks': {},
    'webhooks': {},
    'bulk_jobs': {},
    'audit_logs': {},
    'org_units': {}
}

def generate_id():
    return str(uuid.uuid4())

def create_paginated_response(data, cursor=None):
    return {
        'data': data,
        'pagination': {
            'cursor': cursor,
            'has_more': False
        }
    }

# Authentication endpoint
@app.route('/api/v2/client/tokens', methods=['POST'])
def authenticate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Basic '):
        return jsonify({'error': 'Invalid authentication'}), 401
    
    token = generate_id()
    mock_data['tokens'][token] = {
        'expires_at': datetime.now() + timedelta(hours=1)
    }
    
    return jsonify({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': 3600
    })

def require_auth():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split(' ')[1]
    return token in mock_data['tokens']

# Health check
@app.route('/api/v2/client/health', methods=['GET'])
def health_check():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# Document Management Endpoints
@app.route('/api/v2/client/documents/company-document-types', methods=['GET', 'POST'])
def company_document_types():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        company_id = request.args.get('company_id')
        data = list(mock_data['document_types'].values())
        if company_id:
            data = [d for d in data if d.get('company_id') == company_id]
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        doc_type = request.json
        doc_type['id'] = generate_id()
        doc_type['created_at'] = datetime.now().isoformat()
        mock_data['document_types'][doc_type['id']] = doc_type
        return jsonify(doc_type), 201

@app.route('/api/v2/client/documents/company-document-types/<doc_type_id>', methods=['GET', 'PUT', 'DELETE'])
def company_document_type(doc_type_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if doc_type_id not in mock_data['document_types']:
        return jsonify({'error': 'Document type not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['document_types'][doc_type_id])
    
    elif request.method == 'PUT':
        doc_type = mock_data['document_types'][doc_type_id]
        doc_type.update(request.json)
        doc_type['updated_at'] = datetime.now().isoformat()
        return jsonify(doc_type)
    
    elif request.method == 'DELETE':
        del mock_data['document_types'][doc_type_id]
        return '', 204

@app.route('/api/v2/client/documents/company-documents', methods=['GET', 'POST'])
def company_documents():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['company_documents'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        doc = request.json
        doc['id'] = generate_id()
        doc['created_at'] = datetime.now().isoformat()
        mock_data['company_documents'][doc['id']] = doc
        return jsonify(doc), 201

@app.route('/api/v2/client/documents/company-documents/<doc_id>', methods=['GET', 'PUT', 'DELETE'])
def company_document(doc_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if doc_id not in mock_data['company_documents']:
        return jsonify({'error': 'Document not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['company_documents'][doc_id])
    
    elif request.method == 'PUT':
        doc = mock_data['company_documents'][doc_id]
        doc.update(request.json)
        doc['updated_at'] = datetime.now().isoformat()
        return jsonify(doc)
    
    elif request.method == 'DELETE':
        del mock_data['company_documents'][doc_id]
        return '', 204

@app.route('/api/v2/client/documents/company-folders', methods=['GET', 'POST'])
def company_folders():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['company_folders'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        folder = request.json
        folder['id'] = generate_id()
        folder['created_at'] = datetime.now().isoformat()
        mock_data['company_folders'][folder['id']] = folder
        return jsonify(folder), 201

@app.route('/api/v2/client/documents/company-folders/<folder_id>', methods=['GET', 'PUT', 'DELETE'])
def company_folder(folder_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if folder_id not in mock_data['company_folders']:
        return jsonify({'error': 'Folder not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['company_folders'][folder_id])
    
    elif request.method == 'PUT':
        folder = mock_data['company_folders'][folder_id]
        folder.update(request.json)
        folder['updated_at'] = datetime.now().isoformat()
        return jsonify(folder)
    
    elif request.method == 'DELETE':
        del mock_data['company_folders'][folder_id]
        return '', 204

# Employee Management Endpoints
@app.route('/api/v2/client/employees', methods=['GET', 'POST'])
def employees():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['employees'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        employee = request.json
        employee['id'] = generate_id()
        employee['created_at'] = datetime.now().isoformat()
        mock_data['employees'][employee['id']] = employee
        return jsonify(employee), 201

@app.route('/api/v2/client/employees/<employee_id>', methods=['GET', 'PUT', 'DELETE'])
def employee(employee_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if employee_id not in mock_data['employees']:
        return jsonify({'error': 'Employee not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['employees'][employee_id])
    
    elif request.method == 'PUT':
        emp = mock_data['employees'][employee_id]
        emp.update(request.json)
        emp['updated_at'] = datetime.now().isoformat()
        return jsonify(emp)
    
    elif request.method == 'DELETE':
        del mock_data['employees'][employee_id]
        return '', 204

# Time & Attendance Endpoints
@app.route('/api/v2/client/time-off/requests', methods=['GET', 'POST'])
def time_off_requests():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['time_off_requests'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        request_obj = request.json
        request_obj['id'] = generate_id()
        request_obj['status'] = 'pending'
        request_obj['created_at'] = datetime.now().isoformat()
        mock_data['time_off_requests'][request_obj['id']] = request_obj
        return jsonify(request_obj), 201

@app.route('/api/v2/client/time-off/requests/<request_id>', methods=['GET', 'PUT'])
def time_off_request(request_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request_id not in mock_data['time_off_requests']:
        return jsonify({'error': 'Request not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['time_off_requests'][request_id])
    
    elif request.method == 'PUT':
        req = mock_data['time_off_requests'][request_id]
        req.update(request.json)
        req['updated_at'] = datetime.now().isoformat()
        return jsonify(req)

@app.route('/api/v2/client/time-off/requests/<request_id>/approve', methods=['POST'])
def approve_time_off_request(request_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request_id not in mock_data['time_off_requests']:
        return jsonify({'error': 'Request not found'}), 404
    
    req = mock_data['time_off_requests'][request_id]
    req['status'] = 'approved'
    req['approved_at'] = datetime.now().isoformat()
    return jsonify(req)

@app.route('/api/v2/client/time-off/requests/<request_id>/reject', methods=['POST'])
def reject_time_off_request(request_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request_id not in mock_data['time_off_requests']:
        return jsonify({'error': 'Request not found'}), 404
    
    req = mock_data['time_off_requests'][request_id]
    req['status'] = 'rejected'
    req['rejected_at'] = datetime.now().isoformat()
    return jsonify(req)

@app.route('/api/v2/client/time-attendance/timesheets', methods=['GET', 'POST'])
def timesheets():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['timesheets'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        timesheet = request.json
        timesheet['id'] = generate_id()
        timesheet['created_at'] = datetime.now().isoformat()
        mock_data['timesheets'][timesheet['id']] = timesheet
        return jsonify(timesheet), 201

@app.route('/api/v2/client/time-attendance/timesheets/<timesheet_id>', methods=['GET', 'PUT'])
def timesheet(timesheet_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if timesheet_id not in mock_data['timesheets']:
        return jsonify({'error': 'Timesheet not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['timesheets'][timesheet_id])
    
    elif request.method == 'PUT':
        ts = mock_data['timesheets'][timesheet_id]
        ts.update(request.json)
        ts['updated_at'] = datetime.now().isoformat()
        return jsonify(ts)

@app.route('/api/v2/client/time-attendance/attendance-records', methods=['GET'])
def attendance_records():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['attendance_records'].values())
    return jsonify(create_paginated_response(data))

# Payroll Endpoints
@app.route('/api/v2/client/payroll/runs', methods=['GET'])
def payroll_runs():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['payroll_runs'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/payroll/runs/<run_id>', methods=['GET'])
def payroll_run(run_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if run_id not in mock_data['payroll_runs']:
        return jsonify({'error': 'Payroll run not found'}), 404
    
    return jsonify(mock_data['payroll_runs'][run_id])

@app.route('/api/v2/client/payroll/pay-stubs', methods=['GET'])
def pay_stubs():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['pay_stubs'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/payroll/pay-stubs/<stub_id>', methods=['GET'])
def pay_stub(stub_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if stub_id not in mock_data['pay_stubs']:
        return jsonify({'error': 'Pay stub not found'}), 404
    
    return jsonify(mock_data['pay_stubs'][stub_id])

@app.route('/api/v2/client/payroll/earnings', methods=['GET'])
def earnings():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['earnings'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/payroll/deductions', methods=['GET'])
def deductions():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['deductions'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/payroll/taxes', methods=['GET'])
def taxes():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['taxes'].values())
    return jsonify(create_paginated_response(data))

# Company/Configuration Endpoints
@app.route('/api/v2/client/companies', methods=['GET', 'POST'])
def companies():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['companies'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        company = request.json
        company['id'] = generate_id()
        company['created_at'] = datetime.now().isoformat()
        mock_data['companies'][company['id']] = company
        return jsonify(company), 201

@app.route('/api/v2/client/companies/<company_id>', methods=['GET', 'PUT'])
def company(company_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if company_id not in mock_data['companies']:
        return jsonify({'error': 'Company not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['companies'][company_id])
    
    elif request.method == 'PUT':
        comp = mock_data['companies'][company_id]
        comp.update(request.json)
        comp['updated_at'] = datetime.now().isoformat()
        return jsonify(comp)

@app.route('/api/v2/client/configuration/departments', methods=['GET'])
def departments():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['departments'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/configuration/departments/<dept_id>', methods=['GET'])
def department(dept_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if dept_id not in mock_data['departments']:
        return jsonify({'error': 'Department not found'}), 404
    
    return jsonify(mock_data['departments'][dept_id])

@app.route('/api/v2/client/configuration/job-titles', methods=['GET'])
def job_titles():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['job_titles'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/configuration/locations', methods=['GET'])
def locations():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['locations'].values())
    return jsonify(create_paginated_response(data))

# Benefits Endpoints
@app.route('/api/v2/client/benefits/plans', methods=['GET'])
def benefits():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['benefits'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/benefits/plans/<benefit_id>', methods=['GET'])
def benefit(benefit_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if benefit_id not in mock_data['benefits']:
        return jsonify({'error': 'Benefit not found'}), 404
    
    return jsonify(mock_data['benefits'][benefit_id])

@app.route('/api/v2/client/employees/<employee_id>/benefits', methods=['GET'])
def employee_benefits(employee_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = [b for b in mock_data['employee_benefits'].values() if b.get('employee_id') == employee_id]
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/employees/<employee_id>/benefits/<benefit_id>', methods=['GET'])
def employee_benefit(employee_id, benefit_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    key = f"{employee_id}_{benefit_id}"
    if key not in mock_data['employee_benefits']:
        return jsonify({'error': 'Employee benefit not found'}), 404
    
    return jsonify(mock_data['employee_benefits'][key])

# Reports Endpoints
@app.route('/api/v2/client/reports', methods=['GET', 'POST'])
def reports():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['reports'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        report = request.json
        report['id'] = generate_id()
        report['status'] = 'processing'
        report['created_at'] = datetime.now().isoformat()
        mock_data['reports'][report['id']] = report
        return jsonify(report), 201

@app.route('/api/v2/client/reports/<report_id>', methods=['GET'])
def report(report_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if report_id not in mock_data['reports']:
        return jsonify({'error': 'Report not found'}), 404
    
    return jsonify(mock_data['reports'][report_id])

# eSignature Endpoints
@app.route('/api/v2/client/esignature/requests', methods=['GET', 'POST'])
def signature_requests():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['signature_requests'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        sig_req = request.json
        sig_req['id'] = generate_id()
        sig_req['status'] = 'pending'
        sig_req['created_at'] = datetime.now().isoformat()
        mock_data['signature_requests'][sig_req['id']] = sig_req
        return jsonify(sig_req), 201

@app.route('/api/v2/client/esignature/requests/<request_id>', methods=['GET'])
def signature_request(request_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request_id not in mock_data['signature_requests']:
        return jsonify({'error': 'Signature request not found'}), 404
    
    return jsonify(mock_data['signature_requests'][request_id])

@app.route('/api/v2/client/esignature/tasks', methods=['GET'])
def signature_tasks():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['signature_tasks'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/esignature/tasks/<task_id>', methods=['GET'])
def signature_task(task_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if task_id not in mock_data['signature_tasks']:
        return jsonify({'error': 'Signature task not found'}), 404
    
    return jsonify(mock_data['signature_tasks'][task_id])

# Webhooks Endpoints
@app.route('/api/v2/client/webhooks', methods=['GET', 'POST'])
def webhooks():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if request.method == 'GET':
        data = list(mock_data['webhooks'].values())
        return jsonify(create_paginated_response(data))
    
    elif request.method == 'POST':
        webhook = request.json
        webhook['id'] = generate_id()
        webhook['created_at'] = datetime.now().isoformat()
        mock_data['webhooks'][webhook['id']] = webhook
        return jsonify(webhook), 201

@app.route('/api/v2/client/webhooks/<webhook_id>', methods=['GET', 'PUT', 'DELETE'])
def webhook(webhook_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if webhook_id not in mock_data['webhooks']:
        return jsonify({'error': 'Webhook not found'}), 404
    
    if request.method == 'GET':
        return jsonify(mock_data['webhooks'][webhook_id])
    
    elif request.method == 'PUT':
        wh = mock_data['webhooks'][webhook_id]
        wh.update(request.json)
        wh['updated_at'] = datetime.now().isoformat()
        return jsonify(wh)
    
    elif request.method == 'DELETE':
        del mock_data['webhooks'][webhook_id]
        return '', 204

@app.route('/api/v2/client/webhooks/<webhook_id>/test', methods=['POST'])
def test_webhook(webhook_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if webhook_id not in mock_data['webhooks']:
        return jsonify({'error': 'Webhook not found'}), 404
    
    return jsonify({'status': 'test_sent', 'timestamp': datetime.now().isoformat()})

# Bulk Operations Endpoints
@app.route('/api/v2/client/bulk/employees/import', methods=['POST'])
def bulk_employee_import():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    job = request.json
    job['id'] = generate_id()
    job['status'] = 'processing'
    job['created_at'] = datetime.now().isoformat()
    mock_data['bulk_jobs'][job['id']] = job
    return jsonify(job), 201

@app.route('/api/v2/client/bulk/import-jobs', methods=['GET'])
def bulk_import_jobs():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['bulk_jobs'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/bulk/import-jobs/<job_id>', methods=['GET'])
def bulk_import_job(job_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if job_id not in mock_data['bulk_jobs']:
        return jsonify({'error': 'Import job not found'}), 404
    
    return jsonify(mock_data['bulk_jobs'][job_id])

# Audit/Logging Endpoints
@app.route('/api/v2/client/audit/logs', methods=['GET'])
def audit_logs():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['audit_logs'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/audit/logs/<log_id>', methods=['GET'])
def audit_log(log_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if log_id not in mock_data['audit_logs']:
        return jsonify({'error': 'Audit log not found'}), 404
    
    return jsonify(mock_data['audit_logs'][log_id])

# Organization Management Endpoints
@app.route('/api/v2/client/organization/units', methods=['GET'])
def org_units():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = list(mock_data['org_units'].values())
    return jsonify(create_paginated_response(data))

@app.route('/api/v2/client/organization/units/<unit_id>', methods=['GET'])
def org_unit(unit_id):
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if unit_id not in mock_data['org_units']:
        return jsonify({'error': 'Organization unit not found'}), 404
    
    return jsonify(mock_data['org_units'][unit_id])

@app.route('/api/v2/client/organization/hierarchy', methods=['GET'])
def org_hierarchy():
    if not require_auth():
        return jsonify({'error': 'Unauthorized'}), 401
    
    hierarchy = {
        'company_id': request.args.get('company_id', 'default'),
        'structure': [
            {'id': '1', 'name': 'CEO', 'level': 0, 'parent_id': None},
            {'id': '2', 'name': 'VP Engineering', 'level': 1, 'parent_id': '1'},
            {'id': '3', 'name': 'VP Sales', 'level': 1, 'parent_id': '1'}
        ]
    }
    return jsonify(hierarchy)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)