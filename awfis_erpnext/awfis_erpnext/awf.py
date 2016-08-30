import frappe
from frappe import async
from frappe import _

import re #regular expressions

from frappe.async import get_redis_server, get_user_room

@frappe.whitelist()
def check_duplicate_centres(docname):
	d = frappe.get_doc("Lead", docname)
	c = (d.lead_awfis_centres[0])
	
	return c
	
@frappe.whitelist(allow_guest=True)
def notify_incoming_call(caller_number, agent_number, call_id):
	#url = urllib.unquote(caller_number).decode('utf8')

	is_request_valid = validate_request_header()
	caller_no = process_mobile_no(caller_number)
	agent_no = process_mobile_no(agent_number)
	agent_id = validate_agent(agent_number)

	if is_request_valid != 1:
		return "You are not authorized to make this request."
	elif caller_no == "":
		return "Caller number is invalid."
	elif agent_no == "":
		return "Agent number is invalid."
	elif agent_id == "":
		return "No agent with this number."
	else:
		create_popup(caller_number, agent_id, frappe.db.escape(call_id))


def create_popup(caller_number, agent_id, call_id):
	#return caller_number

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
		ld.awfis_lead_territory = "All Territories"

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
	# for u in frappe.get_all("User", fields=['name'], filters={"role": "Sales User"}):
#		frappe.async.publish_realtime(event="msgprint", message=popup_content, user=u.name)

	#Display popup to agent
	frappe.async.publish_realtime(event="msgprint", message=popup_content, user=agent_id)


#Uses regex to match and extract a 10 digit mobile no from the caller_number parameter. 
#'+' must be encoded if received from URL. 
def process_mobile_no(caller_number):
	# matched_extracted_mobno = re.search(r"^\+?(91|0)\d{10}$", caller_number)
	
	# if matched_extracted_mobno:
	# 	mobno = matched_extracted_mobno.group(0) 
	# 	return mobno[-10:]
	# else:
	# 	return ""
	return caller_number[-10:]


def validate_request_header():
	key_header = frappe.get_request_header("awfis-api-key")
	key_local = frappe.get_single("Awfis Settings").api_key_knowlarity

	if key_header == "":
		return -1 #"Key header is blank"
	elif key_header != key_local:
		return 0 #"{0} != {1} : Key header does not match local key".format(key_header, key_local)
	else:
		return 1 #""


def validate_agent(agent_number):
	agent_number_processed = process_mobile_no(agent_number)

	#If None, all agents are returned. Validation fails.
	if not agent_number_processed:
		return ""

	agents = frappe.get_all("User", fields=['name'], filters={"role": "Sales User", "phone": agent_number_processed})

	if len(agents) > 0:
		return agents[0]["name"] #Return the name of the first agent.
	else:
		return ""

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
def popuptest(caller_number, agent_number, call_id):
	is_request_valid = validate_request_header()
	caller_no = process_mobile_no(caller_number)
	agent_id = validate_agent(agent_number)

	if is_request_valid != 1:
		return "You are not authorized to make this request. [0]"
	elif agent_id == "":
		return "No agent with this number."
	else:
		return "Popup created {c}, {a}, {cl}".format(c=caller_no, a=agent_number, cl=call_id)
		#create_popup(caller_number, agent_id, frappe.db.escape(call_id))


# @frappe.whitelist(allow_guest=True)
# def regextest(caller_number):
# 	cano = process_mobile_no(caller_number)
# 	return "Raw: {r}, Processed: {p}".format(r=caller_number, p=cano)
