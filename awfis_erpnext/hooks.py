# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "awfis_erpnext"
app_title = "Awfis Erpnext"
app_publisher = "MN Technique"
app_description = "ERPNext extensions for Awfis"
app_icon = "octicon octicon-file-directory"
app_color = "#DA251D"
app_email = "support@castlecraft.in"
app_license = "GPL v3"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/awfis_erpnext/css/awfis_erpnext.css"
# app_include_js = "/assets/awfis_erpnext/js/awfis_erpnext.js"

# include js, css files in header of web template
# web_include_css = "/assets/awfis_erpnext/css/awfis_erpnext.css"
# web_include_js = "/assets/awfis_erpnext/js/awfis_erpnext.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "awfis_erpnext.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "awfis_erpnext.install.before_install"
# after_install = "awfis_erpnext.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "awfis_erpnext.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"awfis_erpnext.tasks.all"
# 	],
# 	"daily": [
# 		"awfis_erpnext.tasks.daily"
# 	],
# 	"hourly": [
# 		"awfis_erpnext.tasks.hourly"
# 	],
# 	"weekly": [
# 		"awfis_erpnext.tasks.weekly"
# 	]
# 	"monthly": [
# 		"awfis_erpnext.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "awfis_erpnext.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "awfis_erpnext.event.get_events"
# }
fixtures = ["Custom Script", "Custom Field", "Property Setter"]
