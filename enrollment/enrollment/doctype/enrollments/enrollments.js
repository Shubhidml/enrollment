frappe.ui.form.on("Enrollments", {

    onload(frm) {
        frm.set_query("course", function() {
            return {
                filters: {
                    available_seats: [">", 0]
                }
            };
        });
    },

    refresh(frm) {

        frm.add_custom_button("Create ToDo", function() {

            if (frm.is_new()) {
                frappe.throw("Please save the document first");
            }

            frappe.call({
                method: "enrollment.enrollment.doctype.enrollments.enrollments.make_todo",
                args: {
                    source_name: frm.doc.name
                },
                callback: function(r) {
                    frappe.msgprint("ToDo Created Successfully ✅");

                    if (r.message) {
                        frappe.set_route("Form", "ToDo", r.message.name);
                    }
                }
            });

        });
    }

});