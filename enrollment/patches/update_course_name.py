import frappe

def execute():
    frappe.db.sql("""
        UPDATE `tabCourses`
        SET name = 'C Foundation'
        WHERE name = 'Let Us C'
    """)