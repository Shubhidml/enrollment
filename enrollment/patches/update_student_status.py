import frappe
from datetime import datetime, timedelta

def execute():
    one_year_ago = datetime.now() - timedelta(days=365)

    frappe.db.sql("""
        UPDATE `tabEnrollments`
        SET status = 'Active'
        WHERE enrollment_date >= %s
    """, (one_year_ago,))