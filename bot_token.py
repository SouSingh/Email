import os
import msal
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import json

load_dotenv()
def send_authentication_email( subject, body):
    print("[+] Please do your Authentication [+]")
    from_address = "radhasupplychain2020@gmail.com"
    password = "entg sjdm haco pvjv"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    to_address = input("Enter Your Email: ")

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print("[+] Check your Email for Verification URI and Code!!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def authenticate_bot():
    app_id = os.getenv('MS_CLIENT_ID')
    scopes = ['User.Read', 'Mail.Read', 'Mail.Send']
    access_token_cache = msal.SerializableTokenCache()

    if os.path.exists('Bot_token.json') and os.path.getsize('Bot_token.json') > 0:
        access_token_cache.deserialize(open('Bot_token.json', 'r').read())

    client = msal.PublicClientApplication(client_id=app_id, token_cache=access_token_cache)

    accounts = client.get_accounts()
    if accounts:
        token_response = client.acquire_token_silent(scopes, accounts[0])
    else:
        flow = client.initiate_device_flow(scopes=scopes)
        user_code = flow['user_code']
        verification_uri = flow['verification_uri']

        email_body = f'Welcome To Easeworkai\n\nUser code: {user_code}\nVerification URI: {verification_uri}'
        send_authentication_email("Verification Required", email_body)

        print("Please complete the verification process.")
        token_response = client.acquire_token_by_device_flow(flow)
        # print(token_response)

    with open('Bot_token.json', 'w') as _f:
        _f.write(access_token_cache.serialize())
    
    return token_response

def get_username_from_token_cache():
    if os.path.exists('api_token_access.json') and os.path.getsize('api_token_access.json') > 0:
        with open('api_token_access.json') as f:
            token_cache = json.load(f)
        accounts = token_cache.get("Account", {})
        for key, value in accounts.items():
            if 'username' in value:
                return value['username']
    return None

def get_or_authenticate_bot():
    username = get_username_from_token_cache()
    if username:
        return username
    else:
        print("No registered user found, starting authentication process...")
        token_response = authenticate_bot()

        if token_response:
            username = get_username_from_token_cache()
            if username:
                return username
            else:
                print("Authentication completed, but could not retrieve username.")
                return None
        else:
            print("Authentication failed.")
            return None



