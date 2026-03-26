frappe.ui.form.on("Assignment", {

    onload: function(frm) {
        
        frm.set_query("student", function() {
            return {
                query: "enrollment.enrollment.doctype.assignment.assignment.get_students",
                filters: {
                    course: frm.doc.course,
                    semester: frm.doc.semester
                }
            };
        });

    }

});