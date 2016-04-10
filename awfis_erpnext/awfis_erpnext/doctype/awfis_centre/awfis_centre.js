// Copyright (c) 2016, MN Technique and contributors
// For license information, please see license.txt

frappe.ui.form.on('Awfis Centre', {
	refresh: function(frm) {
	    cur_frm.set_query("city", function() {
	        return {
	            "filters": {
	                "parent_territory": "India"
	            }
	        };
	    });
	}
});
