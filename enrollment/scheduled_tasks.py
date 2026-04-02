import frappe
from frappe.utils import today

def update_attendance_count():
    today_date = today()

    attendance_records = frappe.get_all(
        "Student Attendance",
        filters={"date": today_date},
        fields=["name"]
    )

    if not attendance_records:
        frappe.logger().info(f"No attendance records found for {today_date}")
        return

    present_students = set()

    for record in attendance_records:
        doc = frappe.get_doc("Student Attendance", record["name"])
        for row in doc.attendance_details:
            if row.is_present and row.student:
                present_students.add(row.student)

    for student_id in present_students:
        frappe.db.sql("""
            UPDATE `tabStudents`
            SET attendance_count = COALESCE(attendance_count, 0) + 1
            WHERE name = %s
        """, student_id)

    frappe.db.commit()
    print(f"Attendance updated for {len(present_students)} students on {today_date}")


def process_assignment_grading():
    """
    Background job to process completed assignments and assign grades to students.
    This function runs periodically to check for assignments marked as 'Completed'
    and assigns random grades based on assignment completion.
    """
    # Get all assignments that are completed but not yet graded
    completed_assignments = frappe.get_all(
        "Assignment",
        filters={
            "status": "Completed"
        },
        fields=["name", "student", "course", "semester"]
    )

    if not completed_assignments:
        frappe.logger().info("No completed assignments found for grading")
        return

    grades_processed = 0

    for assignment in completed_assignments:
        try:
            # Assign a random grade (weighted towards better grades)
            grade = assign_random_grade()

            # Update the student record with the grade
            student_doc = frappe.get_doc("Students", assignment.student)
            student_doc.grade = grade
            student_doc.save(ignore_permissions=True)

            # Update assignment status to 'Graded'
            assignment_doc = frappe.get_doc("Assignment", assignment.name)
            assignment_doc.status = "Graded"
            assignment_doc.save(ignore_permissions=True)

            grades_processed += 1

            frappe.logger().info(f"Assigned grade '{grade}' to student '{assignment.student}' for assignment '{assignment.name}'")

        except Exception as e:
            frappe.logger().error(f"Error processing assignment {assignment.name}: {str(e)}")
            continue

    frappe.db.commit()
    frappe.logger().info(f"Processed {grades_processed} assignment grades")


def assign_random_grade():
    """
    Assign a random grade with weighted probabilities.
    A: 30%, B: 35%, C: 20%, D: 10%, F: 5%
    """
    import random

    grades = ['A', 'B', 'C', 'D', 'F']
    weights = [0.3, 0.35, 0.2, 0.1, 0.05]

    return random.choices(grades, weights=weights, k=1)[0]
