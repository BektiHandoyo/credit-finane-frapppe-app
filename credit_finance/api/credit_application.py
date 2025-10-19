import frappe
from frappe import _

@frappe.whitelist()
def create(amount_requested: float, loan_purpose: str, loan_term: int, remarks: str = "", additional_documents: str = None):
    """
    Create a new Credit Application document if user is logged in and has allowed role
    """

    # --- 1️⃣ Cek apakah user sudah login ---
    if frappe.session.user == "Guest":
        frappe.throw(_("You must be logged in to create a Credit Application."), frappe.PermissionError)

    # --- 2️⃣ Cek role user ---
    allowed_roles = ["Customer", "Front Officer"]
    user_roles = frappe.get_roles(frappe.session.user)
    if not any(role in allowed_roles for role in user_roles):
        frappe.throw(_("You do not have permission to create a Credit Application."), frappe.PermissionError)

    # --- 3️⃣ Buat dokumen Credit Application ---
    try:
        doc = frappe.get_doc({
            "doctype": "Credit Application",
            "customer": frappe.session.user,
            "amount_requested": amount_requested,
            "loan_purpose": loan_purpose,
            "loan_term": loan_term,
            "remarks": remarks,
            "additional_documents": additional_documents
        })

        # Optional: abaikan permission kalau kamu mau biar bisa dibuat dari portal
        doc.flags.ignore_permissions = True
        doc.insert(ignore_permissions=True)

        frappe.db.commit()

        return {
            "status": 200,
            "message": _("Credit Application created successfully"),
            "name": doc.name
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Credit Application Creation Failed")
        frappe.throw(_("Failed to create Credit Application: {0}").format(str(e)))
