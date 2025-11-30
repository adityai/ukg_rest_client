#!/usr/bin/env python3
"""
Simple web service to read union entitlements data from SQLite database
"""

from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), 'external_data', 'union_entitlements.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/unions', methods=['GET'])
def get_unions():
    conn = get_db_connection()
    unions = conn.execute('SELECT * FROM unions').fetchall()
    conn.close()
    return jsonify([dict(row) for row in unions])

@app.route('/unions/<union_id>/members', methods=['GET'])
def get_union_members(union_id):
    conn = get_db_connection()
    members = conn.execute('SELECT * FROM union_members WHERE union_id = ?', (union_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in members])

@app.route('/employees/<employee_id>/entitlements', methods=['GET'])
def get_employee_entitlements(employee_id):
    conn = get_db_connection()
    query = '''
        SELECT e.*, me.current_balance, me.accrued_ytd, me.used_ytd, me.last_updated
        FROM entitlements e
        JOIN member_entitlements me ON e.entitlement_id = me.entitlement_id
        JOIN union_members um ON me.member_id = um.member_id
        WHERE um.employee_id = ?
    '''
    entitlements = conn.execute(query, (employee_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in entitlements])

@app.route('/members/<member_id>/entitlements', methods=['GET'])
def get_member_entitlements(member_id):
    conn = get_db_connection()
    query = '''
        SELECT e.*, me.current_balance, me.accrued_ytd, me.used_ytd, me.last_updated
        FROM entitlements e
        JOIN member_entitlements me ON e.entitlement_id = me.entitlement_id
        WHERE me.member_id = ?
    '''
    entitlements = conn.execute(query, (member_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in entitlements])

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'database': os.path.exists(DB_PATH)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)