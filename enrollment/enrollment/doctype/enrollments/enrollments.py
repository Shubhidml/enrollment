import frappe
from frappe.model.document import Document


class Enrollments(Document):

	def validate(self):
		if self.course_credit and self.semester:
			if self.course_credit < 5 and self.semester > 4:
				frappe.throw("You cannot enroll because course credit is less than 5 and semester is greater than 4")

		self.total_fees = (self.course_fee or 0) + (self.registration_fees or 0)


@frappe.whitelist()
def make_todo(source_name):

	doc = frappe.get_doc("Enrollments", source_name)

	todo = frappe.get_doc({
		"doctype": "ToDo",
		"description": f"Student: {doc.student}, Course Fee: {doc.course_fee}",
		"reference_type": "Enrollments",
		"reference_name": doc.name
	})

	todo.insert(ignore_permissions=True)

	return {"name": todo.name}