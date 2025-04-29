import frappe
import requests
from frappe.utils import get_url

@frappe.whitelist()
def send_message(sender_id, channel_name, message_type, content=None, file_url=None):
    # ส่งข้อความผ่าน LINE API สำหรับ channel ที่ระบุ
    channel = frappe.get_doc("LINE Channel", channel_name)
    access_token = channel.channel_access_token
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "to": sender_id,
        "messages": []
    }
    
    if message_type == "Text":
        payload["messages"].append({
            "type": "text",
            "text": content
        })
    elif message_type in ["Image", "Video", "File"]:
        payload["messages"].append({
            "type": message_type.lower(),
            "originalContentUrl": file_url,
            "previewImageUrl": file_url if message_type == "Image" else None
        })
    
    response = requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        # บันทึกข้อความที่ส่ง
        message = frappe.get_doc({
            "doctype": "Omnichat Message",
            "sender_id": sender_id,
            "channel": channel_name,
            "message_type": message_type,
            "message_content": content if message_type == "Text" else '',
            "file_url": file_url if message_type != "Text" else '',
            "timestamp": now_datetime(),
            "is_incoming": 0,
            "status": "Sent"
        })
        message.insert(ignore_permissions=True)
        return {"status": "success"}
    else:
        frappe.throw(f"Failed to send message: {response.text}")

@frappe.whitelist()
def setup_webhook(channel_name):
    # ตั้งค่า webhook URL สำหรับ channel ที่ระบุ
    channel = frappe.get_doc("LINE Channel", channel_name)
    webhook_url = get_url(f"/api/method/omnichat.omnichat.webhook.handle_line_webhook?channel_name={channel_name}")
    channel.webhook_url = webhook_url
    channel.save()
    return {"webhook_url": webhook_url}