frappe.provide("frappe");
frappe.provide("frappe.utils.jinja");
frappe.provide("awfis_erpnext.awfis_erpnext");


//Extend to handle incoming call.
// awfis_erpnext.awfis_erpnext.FooBar = frappe.Application.extend({
// 	startup: function() {
// 		this._super();

// 		frappe.realtime.on('global', function() {
// 			frappe.msgprint('Realtime!');
// 			// var dialog = frappe.msgprint({
// 			// 	message: 'Great success!',
// 			// 	indicator: 'green',
// 			// 	title: 'Incoming Call'
// 			// });
// 			// dialog.set_primary_action("Refresh", function() {
// 			// 	location.reload(true);
// 			// });
// 			//dialog.get_close_btn().toggle(false);
// 		});	
// 	},

// 	foobar: function() {
// 		//NOOP;
// 		frappe.msgprint('XTEND!')
// 	}

// });