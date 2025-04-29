import frappe
from frappe.utils import now_datetime

def get_context(context):
    # สร้าง context สำหรับ web page
    context.channels = frappe.get_all("LINE Channel", fields=["name", "channel_name"])
    context.messages = frappe.get_all(
        "Omnichat Message",
        fields=["sender_id", "channel", "message_type", "message_content", "file_url", "timestamp", "is_incoming"],
        order_by="timestamp asc"
    )
    return context