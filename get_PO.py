
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


# Initialize the OpenAI API (ensure you have set up your OpenAI API key)
openai_api = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
 
prompt_template = PromptTemplate.from_template(
    template="Extract the PO number from the following email content:\n\n{email_content} \n\n\n The PO number format is 'POxxx'. Donot consider any extra spaces."
)
chain = prompt_template | openai_api
 
def extract_po_number(email_content):
    response = chain.invoke({"email_content": email_content})
    return response
 
# Integrate with email reading function
def get_po(mail):
    email_details = mail
    email_content = email_details['subject'] + email_details['body']  # Assuming the email body contains the PO number
    po_number = extract_po_number(email_content)
    return po_number.strip()
 