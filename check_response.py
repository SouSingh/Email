import json
import time
import requests
import os
 
def fetch_and_save_json():
    if os.path.exists('approval_response.json'):
        os.remove('approval_response.json')
 
    response = requests.get('http://54.164.36.151:8000/get_responses')
    response.raise_for_status()
    json_data = response.json()
    with open('approval_response.json', "w") as file:
        file.write(response.text)
 
def check_approval_responses(check_interval=3):
    file_path = 'approval_response.json'
    open(file_path,"w")  
    while True:
        fetch_and_save_json()
        try:
            # Load the JSON data from the file
            with open(file_path, 'r') as file:
                file_content = file.read()
                response = json.loads(file_content)
                
                if response == []:
                    # If the file is empty
                    print("No responses yet. Waiting...")
                    time.sleep(check_interval)
                    continue
                else:
                    if response[0]['response'].lower() == 'yes':
                        return True
                    else:
                        return False
        except Exception as e:
            # If the file content is not valid JSON
            print("Error reading JSON file. Retrying...",e)
            time.sleep(check_interval)
            continue
 
        # # Check if there are any responses
        # if not approval_responses:
        #     print("No responses yet. Waiting...")
        #     time.sleep(check_interval)
        #     continue
 
        # # Check if responses are "yes"
        # yes = True
        # for response in approval_responses:
        #     if response['response'].lower() != 'yes':
        #         all_yes = False
        #         break
 
        
 
