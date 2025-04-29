
app_name = "omnichat"
app_title = "OmniChat"
app_description = "OmniChat integration with multiple LINE Messaging API accounts for ERPNext"
app_publisher = "Vuttinun"
app_email = "vuttinunboontang@gmail.com"
app_license = "MIT"

# เพิ่ม route สำหรับ webhook และ web page
website_route_rules = [
    {
        "from_route": "/omnichat/webhook/<channel_name>",
        "to_route": "omnichat.omnichat.webhook.handle_line_webhook"
    },
    {
        "from_route": "/omnichat",
        "to_route": "omnichat.omnichat.web_page.chat"
    }
]