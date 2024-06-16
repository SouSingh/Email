import requests
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bot_token import authenticate_bot

logger = logging.getLogger(__name__)

def send_BotEmail(sender, subject, message, contentType):
    try:
        access_token = authenticate_bot()['access_token']
    except Exception as e:
        logger.error(f"Error authenticating: {e}")
        return

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    if response.status_code == 200:
        logger.info("Authenticated successfully")
    else:
        logger.error(f"Error authenticating: {response.content}")
        return

    data = {
        "message": {
            "subject": subject,
            "body": {
                "content": message,
                "contentType": contentType
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": sender
                    }
                }
            ]
        }
    }

    try:
        response = requests.post("https://graph.microsoft.com/v1.0/me/sendMail", json=data, headers=headers)
        response.raise_for_status()
        logger.info("Email sent successfully")
    except requests.exceptions.RequestException as e:
        logger.error(f"Error sending email: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

def send_approval_email(to_email, supplier_mail):
    body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        
        body {{
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            box-sizing: border-box;
        }}
        .content {{
            background-color: #fff;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            width: 100%;
            box-sizing: border-box;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{
            color: #5e0dac;
            font-size: 36px;
            margin: 0;
            font-family: 'Roboto', sans-serif;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        .message {{
            margin-bottom: 40px;
            font-size: 16px;
            line-height: 1.8;
        }}
        .message h3 {{
            margin: 0;
            font-size: 22px;
            color: #5e0dac;
            margin-bottom: 20px;
        }}
        .message p {{
            margin: 0 0 15px;
        }}
        .btn {{
            background-color: #5e0dac;
            color: white;
            padding: 14px 28px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            border-radius: 5px;
            margin: 0 10px 0 0;
            cursor: pointer;
            transition: background-color 0.3s;
            font-size: 16px;
        }}
        .btn.reject {{
            background-color: #a62926;
        }}
        .btn:hover {{
            background-color: #3e0b8f;
        }}
        .btn.reject:hover {{
            background-color: #871d1b;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="content">
            <div class="header">
                <h1>Easework AI</h1>
            </div>
            <div class="message">
                <h3>Document Approval Request</h3>
                <p><strong>Mail and Document from Supplier:</strong></p>
                <p>{supplier_mail}</p>
                <p><strong>Please approve or reject the document.</strong></p>
            </div>
            <a class="btn" href="http://54.164.36.151:8000/approve?response=yes&ip_address=54.164.36.151" style="background-color: #5e0dac; color: white; padding: 14px 28px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin: 0 10px 0 0; cursor: pointer; font-size: 16px;">Approve</a>
            <a class="btn reject" href="http://54.164.36.151:8000/approve?response=no&ip_address=54.164.36.151" style="background-color: #a62926; color: white; padding: 14px 28px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; margin: 0 10px 0 0; cursor: pointer; font-size: 16px;">Reject</a>
        </div>
    </div>
</body>
</html>
"""

    send_BotEmail(to_email, "Approval Email", body, "html")

