import frappe
from frappe import async
from frappe import _

import re #regular expressions

from frappe.async import emit_via_redis, get_site_room


@frappe.whitelist()
def check_duplicate_centres(docname):
	d = frappe.get_doc("Lead", docname)
	c = (d.lead_awfis_centres[0])
	
	return c
	

@frappe.whitelist(allow_guest=True)
def notify_incoming_call(caller_number, agent_number, call_id):

	if validate_request_header() == 1:
		agent_id = validate_agent(agent_number)

		if agent_id:
			create_popup(caller_number, agent_id, call_id)
		else:
			return "Invalid agent number"
	else:
		return "You are not authorized to make this request."


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

def validate_request_header():
	key_header = frappe.get_request_header("awf_erpnext_api_key")
	key_local = frappe.get_single("Awfis Settings").api_key_knowlarity

	if key_header == "":
		return 0 #"Key header is blank"
	elif key_header != key_local:
		return 0 #"{0} != {1} : Key header does not match local key".format(key_header, key_local)
	else:
		return 1 #""

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

@frappe.whitelist()
def generate_key_knowlarity():
	apikey = frappe.generate_hash()
	return apikey #{ "key" : apikey }

@frappe.whitelist(allow_guest=True)
def popuptest():

	#frappe.msgprint(validate_request_header())

	for u in frappe.get_all("User", fields=['name'], filters={"role": "Sales User"}):
		#emit_via_redis(event="msgprint", message="Howdy!", room=get_site_room())
		frappe.async.publish_realtime(event="msgprint", message="Howdy!", user=u.name)
		#frappe.publish_realtime('msgprint', 'Howdy!', user='Administrator')
		#frappe.msgprint(frappe.session.user)
