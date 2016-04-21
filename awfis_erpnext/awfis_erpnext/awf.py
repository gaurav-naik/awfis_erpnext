import frappe

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
	#return  "{0} <<=====>> {1}".format(c, set(c))