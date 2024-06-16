
import requests
from bot_token import authenticate_bot
from access_token import authenticate_user
import os

# {subject,body, content, recipient}

def send_emails(message):
    
    headers = {"Authorization": str(authenticate_bot()['access_token'])}
    response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

    if response.status_code == 200:
        print("Authenticated successfully")
    else:
        # Handle error
        print("Error authenticating")

    data = {
        "message": {
            "subject": message['subject'],
            "body": {
                "content": message['content']
            },
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": message['recipient']
                    }
                }
            ]
        }
    }

    response = requests.post("https://graph.microsoft.com/v1.0/me/sendmail", json=data, headers=headers)

    if response.status_code == 202:
        print("Email sent successfully")
    else:
        # Handle error
        print("Error sending email",response.content)
        exit(1)

def read_emails():
    headers = {"Authorization": str(authenticate_bot()['access_token'])}
 
    # Retrieve a list of emails in the Inbox folder
    response = requests.get("https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages", headers=headers)
 
    if response.status_code == 200:
        email = response.json()["value"][0]
        email_id = email["id"]
        response = requests.get(f"https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/{email_id}", headers=headers)
        if response.status_code == 200:
            email_details = response.json()
            attachment_response = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/attachments", headers=headers)
            attachments = []
            attachment_contents = {}
            if attachment_response.status_code == 200:
                attachments = attachment_response.json().get('value', [])
                for attachment in attachments:
                    attachment_id = attachment['id']
                    attachment_detail_response = requests.get(f"https://graph.microsoft.com/v1.0/me/messages/{email_id}/attachments/{attachment_id}/$value", headers=headers)
                    if attachment_detail_response.status_code == 200:
                        attachment_contents[attachment['name']] = attachment_detail_response.content
                    else:
                        print(f"Error retrieving attachment content for {attachment['name']}")
 
            # Extract only the name without the extension
            attachment_names = [os.path.splitext(attachment['name'])[0] for attachment in attachments]
            # print(email_details)
            return {
                'from': email_details['from'],
                'subject': email_details['subject'],
                'body': email_details['bodyPreview'],
                'received': email_details['receivedDateTime'],
                'attachments': attachment_names,
                # 'attachment_contents': attachment_contents
            }
        else:
            print("Error retrieving email details")
    else:
        print("Error retrieving emails")


# message= {'subject' : "1234",'content': " Hello test email", "address": "yash@easeworkai.com"} 
# send_emails('yash@easeworkai.com',message)


# print(read_emails('yash@easeworkai.com'))



