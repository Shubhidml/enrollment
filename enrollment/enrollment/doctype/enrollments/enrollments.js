// Copyright (c) 2026, shubh and contributors
// For license information, please see license.txt

frappe.ui.form.on("Enrollments", {
    refresh(frm) {
        let course = frappe.get_doc("Courses", frm.doc.course);

        if (course.available_seats <= 0) {
            frappe.throw(
                "Not enough seats available in " + course.course_name + ". Available seats: " + course.available_seats
            );
        }

        course.available_seats = course.available_seats - 1;

        course.save();
    },
});
