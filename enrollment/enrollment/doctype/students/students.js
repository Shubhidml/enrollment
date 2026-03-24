frappe.ui.form.on("Students", {

    refresh(frm) {

        frm.add_custom_button("Get Assignment Details", function() {

            frappe.call({
                method: "enrollment.enrollment.doctype.assignment.assignment.get_assignment_details",
                args: {
                    student: frm.doc.name
                },
                callback: function(r) {

                    if (r.message && r.message.assignment_details) {

                        frappe.msgprint({
                            title: "Assignment Details",
                            message: `
                                <b>Course:</b> ${r.message.course} <br>
                                <b>Semester:</b> ${r.message.semester} <br><br>
                                <b>Details:</b><br>
                                ${r.message.assignment_details}
                            `,
                            indicator: "green"
                        });

                    } else {
                        frappe.msgprint("No Assignment Found ❌");
                    }

                }
            });

        });

    }

});