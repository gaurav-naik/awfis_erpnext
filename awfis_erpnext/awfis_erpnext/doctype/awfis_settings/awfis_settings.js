// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Awfis Settings', {
	refresh: function(frm) {

	},

	btn_generate_key_knowlarity: function(frm) {
		frappe.call({
			method: "awfis_erpnext.awfis_erpnext.awf.generate_key_knowlarity",
			freeze: true,
			freeze_message: __("Generating API key for Knowlarity"),
			callback: function(r){
				if(!r.exc) {
					frm.set_value("api_key_knowlarity", r.message);
				} else {
					frappe.msgprint(__("Key was not generated. <br /> " + r.exc));
				}
			}
		});
	}


});
