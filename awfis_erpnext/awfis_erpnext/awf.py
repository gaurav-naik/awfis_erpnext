import frappe
from frappe import async
from frappe import _

import re #regular expressions


@frappe.whitelist()
def check_duplicate_centres(docname):
	d = frappe.get_doc("Lead", docname)
	c = (d.lead_awfis_centres[0])
	
	return c
	#return True #Returns {"message":true}

	#return (len(d.lead_awfis_centres) != len(set(d.lead_awfis_centres))) #returns {}

	#if (len(d.lead_awfis_centres) != len(set(d.lead_awfis_centres))):
		#return True ## Returns {}
	#	return '1'
	#else:
#		return '0'
	#return  "{0} <<=====>> {1}".format(c, set(c))\

# @frappe.whitelist(allow_guest=True)
# def popuptrial(mobileno):
# 	for u in frappe.utils.user.get_users():
# 		roles = frappe.utils.user.get_roles(u)
# 		if roles['Sales User']:
# 			uname = u['name']
# 			frappe.async.publish_realtime(event="msgprint", message=mobileno, user=uname)


# from frappe.desk.notifications import clear_notifications
# @frappe.whitelist(allow_guest=True)
# def popmsgtrial(mobileno):
# 	# clear_notifications
# 	#frappe.async.publish_realtime('abc', message=mobileno)
# 	frappe.async.publish_realtime('msgprint')



	# for u in frappe.utils.user.get_users():
	# 	roles = frappe.utils.user.get_roles(u)
	# 	if roles['Sales User']:
	# 		uname = u['name']
	# 		frappe.async.publish_realtime(event="msgprint", message=mobileno, user=uname)



	#frappe.msgprint(frappe.session.user)

	# sales_users = frappe.db.sql("select distinct A.name from tabUser A INNER JOIN tabUserRole B ON A.name = B.parent  where B.role like 'Sales User';")

	# for u in sales_users:
	# 	#frappe.msgprint(u[0])
	# 	frappe.async.publish_realtime(event="msgprint", message=txt, user=u[0])


# @frappe.whitelist(allow_guest=True)
# def erpnext_notify_incoming_call(mobileno):

# 	#http://0.0.0.0:8000/api/method/awfis_erpnext.awfis_erpnext.awf.lead_info_popup/?mobileno=9833222251

# 	mobno = validate_mobile_no(mobileno)

# 	ld = frappe.get_all("Lead", fields=["*"], filters={"mobile_no": mobno})	

# 	if not ld:
# 		#Create stub lead.
# 		ld = frappe.new_doc("Lead")

# 		ld.mobile_no = mobno
# 		ld.lead_name = "New Lead {m}".format(m=mobno) 
		
# 		#Mandatory custom fields.
# 		ld.first_name = "New Lead {m}".format(m=mobno)
# 		ld.awfis_mobile_no = mobno
# 		ld.source = "Other"
# 		ld.awfis_lead_territory = "Mumbai"

# 		#frappe.msgprint("Lead created. {lead}".format(lead=ld))
# 		ld.insert(ignore_permissions=True)
# 		frappe.db.commit()

# 		erpnext_notify_incoming_call(mobno) #Recursive call. This branch wont be hit again for the same mobile no.

# 	# elif len(ld) > 1:
# 	# 	pass
# 	# 	#Add error message to Lead: Duplicate Mobile No.
# 	# 	#Loop through ld and display both leads.

# 	else:
# 		# Display the popup.
# 		prms = {"mobile_no": ld[0].mobile_no, 
# 				"lead_name": ld[0].lead_name, 
# 				"company_name": ld[0].company_name,
# 				"name": ld[0].name}

# 		popup_content = frappe.render_template("awfis_erpnext/templates/lead_info.html", prms)


# 	 	#Add to notifications.
# 		notif = frappe.new_doc("Communication")
# 		notif.subject = "Incoming Call {m}".format(m=mobno)
# 		notif.communication_type = "Communication"
# 		notif.content = popup_content #, {"communication_type": "Notification", "content": popup_content})
# 		notif.status = "Linked"
# 		notif.sent_or_received = "Sent"
# 		notif.reference_doctype = "Lead"
# 		notif.reference_name = ld[0].name

# 		notif.insert(ignore_permissions=True)
# 		frappe.db.commit()

# 		#frappe.async.emit_via_redis(
# 		#sales_users_logged_in = frappe.get_all("User", fields=['*'], filters={""})

# 		#sales_users = frappe.db.sql("SELECT DISTINCT A.name FROM tabUser A INNER JOIN tabUserRole B ON A.name = B.parent WHERE A.enabled = 1 AND B.role LIKE 'Sales User';")

# 		# for u in sales_users:
# 		# 	uname = u[0]
# 		# 	frappe.async.publish_realtime(event="msgprint", message=popup_content, user=uname)

# 		#frappe.get_all("Users", fields)

# 		# for u in frappe.utils.user.get_users():
# 		# 	roles = get_roles(u)
# 		# 	if 'Sales User' in roles:
# 		# 		uname = u['email']
# 		# 		frappe.async.publish_realtime(event="msgprint", message=popup_content, user=uname)

# 		for u in frappe.get_all("User", fields=['name'], filters={"role": "Sales User"}):
# 			frappe.async.publish_realtime(event="msgprint", message=popup_content, user=u.name)

@frappe.whitelist(allow_guest=True)
def notify_incoming_call(caller_number, agent_number, call_id):

	agent_id = validate_agent(agent_number)

	if agent_id:
		create_popup(caller_number, agent_id, call_id)
	else:
		pass #Handle this?


def validate_agent(agent_number):
	agent_number_processed = process_mobile_no(agent_number)

	#agent_id = frappe.db.get_value("User", {"phone": agent_number_processed, "role": "Sales User"}, "name")

	agents = frappe.get_all("User", fields=['name'], filters={"role": "Sales User", "phone": agent_number_processed})

	if len(agents) > 1:
		frappe.throw(__("Multiple agents have the same mobile no."))

	agent_id = agents[0]["name"] #Return the name of the first agent.

	if agent_id:
		return agent_id
	else:
		return None


def create_popup(caller_number, agent_id, call_id):
	#http://0.0.0.0:8000/api/method/awfis_erpnext.awfis_erpnext.awf.lead_info_popup/?mobileno=9833222251

	caller_number_processed = process_mobile_no(caller_number)

	ld = None

	ld_name = frappe.db.get_value("Lead", {"mobile_no": caller_number_processed}, "name") # frappe.get_all("Lead", fields=["*"], filters={"mobile_no": caller_number_processed})	

	if not ld_name:
		#Create stub lead if lead is not found.
		ld = frappe.new_doc("Lead")
		ld.mobile_no = caller_number_processed
		ld.lead_name = "New Lead ({m})".format(m=caller_number) 
		
		#Set mandatory custom fields.
		ld.first_name = "New Lead ({m})".format(m=caller_number)
		ld.awfis_mobile_no = caller_number_processed
		ld.source = "Other"
		ld.awfis_lead_territory = "Mumbai"

		ld.insert(ignore_permissions=True)
		frappe.db.commit()
	else:
		ld = frappe.get_doc("Lead", ld_name)
	
	#Make popup content.
	lead_fields = {"mobile_no": caller_number,  
			"lead_name": ld.lead_name, 
			"company_name": ld.company_name,
			"name": ld.name, 
			"call_timestamp": frappe.utils.datetime.datetime.strftime(frappe.utils.datetime.datetime.today(), '%d/%m/%Y %H:%M:%S'), 
			"call_id": call_id}

	popup_content = frappe.render_template("awfis_erpnext/templates/lead_info.html", lead_fields)

	#Create a notification.
	notif = frappe.new_doc("Communication")
	notif.subject = "Incoming Call {m}".format(m=caller_number)
	notif.communication_type = "Communication"
	notif.content = popup_content #, {"communication_type": "Notification", "content": popup_content})
	notif.status = "Linked"
	notif.sent_or_received = "Sent"
	notif.reference_doctype = "Lead"
	notif.reference_name = ld.name

	notif.insert(ignore_permissions=True)
	frappe.db.commit()

	#Display the actual popup to all sales users.
	for u in frappe.get_all("User", fields=['name'], filters={"role": "Sales User"}):
		frappe.async.publish_realtime(event="msgprint", message=popup_content, user=u.name)

def process_mobile_no(caller_number):
	#Strip the +91
	#"^\+(91|0)\d{9,13}$" : Regex for number.

	#Ensure that the raw number is in a specific format 
	# rule = re.compile(r"^\+(91|0)\d{9,13}$")

	# if not rule.search(caller_number):
	# 	frappe.throw(_("Mobile No. format is invalid."))

	#Process the number. Subtract left ten digits.
	final_caller_number = caller_number[-10:]


	return final_caller_number


#from frappe.core.notifications import get_notification_config

def awfis_notification_filter():
	return {
		"for_doctype": {
			"Communication": {"status": ["in", ('Linked', 'Open')], "communication_type": "Communication"}
		}
	}	
