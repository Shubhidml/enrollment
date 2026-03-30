import frappe
from frappe.model.utils.rename_field import rename_field

def execute():
    rename_field("Students", "student", "student_name")