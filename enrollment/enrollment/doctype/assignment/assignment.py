import frappe
from frappe.model.document import Document


class Assignment(Document):

    def validate(self):
        if not frappe.db.exists("Enrollments", {
            "student": self.student,
            "course": self.course,
            "semester": self.semester
        }):
            frappe.throw("Student not enrolled")


@frappe.whitelist()
def get_students(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
        SELECT student FROM `tabEnrollments`
        WHERE course=%s AND semester=%s
    """, (filters.get("course"), filters.get("semester")))


@frappe.whitelist()
def get_assignment_details(student):

    assignment = frappe.get_all(
        "Assignment",
        filters={"student": student},
        fields=["assignment_details", "course", "semester"],
        order_by="creation desc",
        limit=1
    )

    if assignment:
        return assignment[0]   
    else:
        return {}