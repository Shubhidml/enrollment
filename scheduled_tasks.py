import frappe
from frappe.utils import today

def update_attendance_count():
    """
    Scheduled daily job: increments attendance_count for all students
    marked present in today's Student Attendance records.
    """
    today_date = today()

    # Fetch all Student Attendance records for today
    attendance_records = frappe.get_all(
        "Student Attendance",
        filters={"date": today_date},
        fields=["name"]
    )

    if not attendance_records:
        frappe.logger().info(f"No attendance records found for {today_date}")
        return

    # Collect all student names marked present today
    present_students = set()

    for record in attendance_records:
        doc = frappe.get_doc("Student Attendance", record["name"])
        for row in doc.attendance_details:
            if row.is_present and row.student:
                present_students.add(row.student)

    # Increment attendance count for each present student
    for student_id in present_students:
        frappe.db.sql("""
            UPDATE `tabStudents`
            SET attendance_count = COALESCE(attendance_count, 0) + 1
            WHERE name = %s
        """, student_id)

    frappe.db.commit()
    frappe.logger().info(
        f"Attendance updated for {len(present_students)} students on {today_date}"
    )