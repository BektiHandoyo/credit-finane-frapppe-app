import frappe
from frappe import _
from frappe.utils import escape_html

@frappe.whitelist(allow_guest=True)
def create_user(email: str, first_name: str, last_name: str, password:str, redirect_to: str="/login") -> tuple[int, str]:
	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": first_name,
				"last_name" : last_name,
				"enabled": 1,
				"new_password": password,
				"send_welcome_email": 0,
				"user_type": "Website User",
			}
		)
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()
  
		user.add_roles("Customer")

		# set default signup role as per Portal Settings
		frappe.set_user(user.name)
		return {
			"status" : 200,
			"message": "create user successfully",
		}
		# frappe.local.response["type"] = "redirect"
		# frappe.local.response["location"] = redirect_to


@frappe.whitelist(allow_guest=True)
def login(email, password):
	try : 
		loginManager = frappe.auth.LoginManager()
		loginManager.authenticate(user=email, pwd=password)
		loginManager.post_login()
		return {
			"status": 200,
			"message" : "login success"
		}
		# frappe.local.response["type"] = "redirect"
		# frappe.local.response["location"] = frappe.response["home_page"]
	except frappe.exceptions.AuthenticationError:
		# frappe.clear_messages()
		# frappe.local.response["message"] = {
        #     "success_key": 0,
        #     "message": "Authentication error"
        # }
		return {
			"status": 500,
			"message" : "Authentication error"
		}
