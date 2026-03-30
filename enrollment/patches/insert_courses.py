import frappe

def execute():
    courses = [
        {"course_name": "Python Basics", "description": "Intro to Python", "course_duration": "3 Months"},
        {"course_name": "Java Fundamentals", "description": "Core Java", "course_duration": "4 Months"},
        {"course_name": "Web Dev", "description": "HTML CSS JS", "course_duration": "2 Months"},
        {"course_name": "Data Science", "description": "ML Basics", "course_duration": "6 Months"},
        {"course_name": "DBMS", "description": "Database Concepts", "course_duration": "3 Months"}
    ]

    for c in courses:
        if not frappe.db.exists("Courses", {"course_name": c["course_name"]}):
            doc = frappe.get_doc({
                "doctype": "Courses",
                **c
            })
            doc.insert(ignore_permissions=True)