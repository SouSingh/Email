from transformers import pipeline

# Initialize the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification")

def classify_email(email_body):
    # Define the candidate labels
    candidate_labels = ["purchase order related", "business inquiry", "complaint", "mail with attechment", "other"]
    
    # Classify the email
    result = classifier(email_body, candidate_labels)
    
    # Extract the most likely label
    most_likely_label = result['labels'][0]
    
    return most_likely_label, result

def is_po_date_change(email_body):
    most_likely_label, _ = classify_email(email_body)
    
    # Check if the email is about a PO date change
    if most_likely_label == "purchase order":
        return True
    else:
        return False

# Example email body
email_body ='''
Dear Yash,
I liked the product you are selling and I want to meet you in person to talk more business in future supplies. Our supply chain has been very fast and I am pretty sure that we'll expand your business to greater extent.

Yours Sincerely,
Yash
'''
# print(classify_email(email_body)[0])

# Check if the email is about a PO date change
# po_date_change = is_po_date_change(email_body)
# print(f"Is the email about a PO date change? {po_date_change}")


