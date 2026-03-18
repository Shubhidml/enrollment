# Copyright (c) 2026, shubh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Enrollments(Document):
	def validate(self):
		# Server-side validation
		if self.course_credit < 5 and self.semester > 4:
			frappe.throw("You cannot enroll because course credit is less than 5 and semester is greater than 4")
		
		# Calculate total fee
		self.calculate_total()

	def calculate_total(self):
		# Calculate total fee from course_fee and registration_fee
		self.total_fee = (self.course_fee or 0) + (self.registration_fee or 0)
