from db import get_delivery_date, get_missing_docs, get_incharge, get_requestor, get_supplier
import datetime
from send_approval_email import send_BotEmail
import json
import time
import os

def doc_request():
    today = datetime.date.today()
    dd = get_delivery_date()
    for PO,DD in dd:
        daysRemaining = DD - today
        missing = get_missing_docs(PO)
        supplier_docNames = ["Bill Of Ladding", "Pro Forma Invoice", "Drawings", "Material Quality Inspection Certificate"]
        buyer_docNames = ["Letter of Credit"]

        supplier = get_supplier(PO)
        requestor = get_requestor(PO)
        requestTo = {supplier : "", requestor: ""}
        
        # if daysRemaining.days < 0 :
        #     continue
        for i,j in missing["s_missing"]:
            requestTo[supplier] += "- " + supplier_docNames[i] + "\n"
        for i,j in missing["b_missing"]:
            requestTo[requestor] += "- " + buyer_docNames[i] + "\n"
        

        # print(requestTo)
        for to,missing_docs in requestTo.items():
            subject = "Submit the missing document"
            msg = f"""Dear User,
Submit your missing documents for PO order #{PO}, {daysRemaining.days} days are left.
Your missing Documents: \n
{missing_docs}
Submit before the deadline.

Best Regards,
EaseAgent

        """
            # print(to, msg, "\n\n-----")
            if missing_docs == "":
                continue
            else:
                send_BotEmail(to, subject, msg,"text")
        

def check_docs():
    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if os.path.exists('times.json'):
            with open('times.json', 'r') as file:
                data = json.load(file)
            received_time = data[0]["received_time"]
        else:
            received_time = "00:00:00"

        if current_time == received_time:
            print('Processing document request...')
            doc_request()  # Assuming this function is defined elsewhere
            time.sleep(1)  # Delay to prevent rapid processing
        time.sleep(1)

check_docs()

# doc_request()

# import asyncio
# asyncio.run(check_docs())

# print(datetime.time.now())