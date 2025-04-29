import frappe
import requests
import json
from frappe.utils import now_datetime

@frappe.whitelist(allow_guest=True)
def handle_line_webhook(channel_name):
    # รับ webhook จาก LINE สำหรับ channel ที่ระบุ
    data = frappe.request.get_data(as_text=True)
    events = json.loads(data).get('events', [])
    
    channel = frappe.get_doc("LINE Channel", channel_name)
    
    for event in events:
        if event['type'] == 'message':
            sender_id = event['source']['userId']
            message_type = event['message']['type'].capitalize()
            timestamp = now_datetime()
            
            # สร้าง Omnichat Message
            message = frappe.get_doc({
                "doctype": "Omnichat Message",
                "sender_id": sender_id,
                "channel": channel_name,
                "message_type": message_type,
                "message_content": event['message'].get('text') if message_type == 'Text' else '',
                "file_url": event['message'].get('contentProvider', {}).get('originalContentUrl') if message_type != 'Text' else '',
                "timestamp": timestamp,
                "is_incoming": 1,
                "status": "Received"
            })
            message.insert(ignore_permissions=True)
            
    return {"status": "success"}