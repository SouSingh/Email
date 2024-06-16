


"""

Respond to a suppliers email:
    1. Get the email
    2. Categorize email into "Accepting the PO Order", "PO order        changes", "Rejecting the PO order"
    3. If changes then categorize those into change in "Delivery Date", "Quantity"
    4. If changes send a request mail to the Buyer and after changes make changes into the mail and write a mail back to supplier for accepting the changes.
    5. If no changes then write a accept or rejection mail back to the supplier


Agents:
    - Email Categorizer
    - Researcher
    - Email Writer

Tasks:
    -  Categorize email
    - Research the answer
    - Write the email

"""



from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
import os
from llama_index.llms.openai import OpenAI
from llama_index.core import ChatPromptTemplate
from llama_index.core.llms import ChatMessage
from crewai import Agent, Task, Crew, Process
from langchain_community.tools import DuckDuckGoSearchRun
import json
from crewai import Crew, Process

GROQ_LLM = ChatGroq(
    api_key = os.environ["GROQ_API_KEY"],
    model="llama3-70b-8192"
)


class EmailAgents():
    def make_validator_agent(self):
        return Agent(
            role = "Email Validator Agent",
            goal = """ Our company has sent a purchase order to suppliers and the suppliers reply in emails. You will be given an email and you need to validate that email whether it is from supplier or not. \
            If the email is from supplier then filter the email into plain text (if it is already in the text format then no need to filter), since it can be in the Html format as well. So return the email in normal plain text format such that no content of the email is misplaced or meaining is changed. If PO or Purchase Order is not mentioned then the email is not a supplier \
            Make sure to return the output strictly in json format no extra explanation
""",
            backstory = """ You are master at understanding who is writing the letter and if the body of the letter is in the HTML format then you can understand it too and return the main content in plain text format from that email""",
            llm = GROQ_LLM,
            verbose = True,
            allow_delegation = False,
            memory = True
        )
    def make_categorizer_agent(self):
        return Agent(
            role = "Email Categorizer Agent",
            goal = """Our company has sent a purchase order to suppliers and the suppliers reply in emails and take these emails and categorize it into one of the following categories into strict json format: \ 
            acceptance - used when the supplier is ready or accepts the supply of the Purchase Order \
            rejection - used when the supplier is not ready or rejects the supply of the Purchase Order \
            change - used when the supplier requests change in the Purhcase Order and further categorizes it into: \
            quantity: used when supplier requests to change the quantity \
            delivery_date: used when supplier requests a change in the delivery date \
""",
            backstory = """ You are a master at understanding what a supplier wants when they write an email and are able to categorize it in a useful way
""",
            llm = GROQ_LLM,
            verbose = True,
            allow_delegation = False,
            # max_iter = 10,
            memory = True
        )
    
    def make_email_writer_agent(self):
        return Agent(
            role = "",
            goal = """ Our company has sent a purchase order to suppliers and the suppliers reply in emails and take these emails, the category that the categorizer agent has provided and the research provided by the researcher agent and write a helpful email in thoughful and proffessional way. \
            If the supplier email is 'acceptance' then reply them with the good note and thank for the confirmation. \
            If the supplier email is 'rejection' then reply them with the good note asking the reason if mentioned in the email then do not ask and thank for the confirmation. \
            If the supplier email is 'change' then reply them with the good note and thank for the confirmation. \
""",
            backstory = """You are a master at synthesizing a variety of information and writing a helpful email that will address the suppliers and provide them with helpful confirmation.
""",
            llm=GROQ_LLM,
            verbose = True,
            allow_delegation = False,
            # max_iter = 10,
            memory = True,
        )
    


class EmailTasks():
    # Define your tasks with descriptions and expected outputs

    def validating_email(self,email_content,validator_agent):
        return Task(
            description = f"""Conduct the comprehensive analysis on the email provided and validate whether the reply is from supplier or not \
            if it is from supplier then return True else False. Make sure the email has PO or Purchase Order number if not then the email is not from supplier and return False \
            Also the email provided can be in the HTML format so extract the relevant content of the email and give it in the proper email format.
            Email Content: \n\n {email_content} \n\n \
Ouput the is supplier in true and false and text format email
""",
            expected_output = """ Give the validation of the supplier and the text format email(if already in text format then return same) strictly in JSON format and no other explaination.\
            \
            Make sure to return the output strictly in json format no extra explanation
            Example:
            { Is_Supplier_Email : "True/False" ,
            email : {
                (text formatted email)
                from:
                to:
                subject:
                body:
                }
            }
""",
            output_file="validator_email.txt",
            agent=validator_agent
        )

    def categorize_email(self, email_content,validate_email,categorizer_agent):
        return Task(
            description=f"""Conduct a comprehensive analysis of the email provided and categorize into \
            one of the following categories:
            acceptance - used when the supplier is ready or accepts the supply of the Purchase Order \
            rejection - used when the supplier is not ready or rejects the supply of the Purchase Order \
            change - used when the supplier requests change in the Purhcase Order and further categorizes into sub-category that is: \
            quantity: used when supplier requests to change the quantity \
            delivery_date: used when supplier requests a change in the delivery date \
            No need to categorize email if the email is not from the supplier as confirmed by the validator agent

            EMAIL CONTENT:\n\n {email_content} \n\n
            Output a single category only, if it is change then also mention multiple the sub categories """,
            expected_output="""A single categtory for the type of email from the types ('acceptance', 'rejection', 'change : quantity, delivery_date') \
            
            if Not a supplier than no need to categorize if not a supplier as suggested by validator agent \
            No need of extra explaination, give strictly in JSON \
            Strictly Follow the same format of keys as shown in example \
            example
                {
                category: "acceptance/rejection/change"
                change: {
                change_type : "quantity/delivery_date",
                changed_qty : "changed quantity in numbers/ non",
                changed_date: "changed date in date format only(YYYY-MM-DD)} / non"
                } / "non",
                PO: "PO(Purchase Order) Number/non"
                }
            """,
            context = [validate_email],
            output_file=f"email_category.txt",
            agent=categorizer_agent
            )

   

    def draft_email(self, email_content,email_writer_agent,validate_email,categorize_email):
        return Task(
            description=f"""Conduct a comprehensive analysis of the email provided, the category provided\
            and the info provided from the research specialist to write an email. \
            Use only required information.
            Write a simple, polite and to the point email which will respond to the suppliers email. \
            If useful use the info provided from the research specialist in the email. \
            Always reply to the email positively.
            If no useful info was provided from the research specialist the answer politely but don't make up info. \
            If there is no PO or Purchase order number mentioned in the output of the email categorizer agent then write email requesting to mention the PO or Purchase Order number in the letter and resend the letter again.


            EMAIL CONTENT:\n\n {email_content} \n\n \
            \
""",
            expected_output="""A well crafted email for the customer that addresses their issues and concerns with Purchase Order number
                
                Give drafted email strictly in JSON format only and no need of extra explaination : 
                Strict Draft Letter Format example in json
                {
                    email: {
                    subject:
                    body:
                    }
                }
            """,
            context = [categorize_email,validate_email],
            agent=email_writer_agent,
            output_file=f"draft_email.txt",
            )
    
def extract_information_from_agents(file_name):
    file_path = file_name
    file_name, _ = os.path.splitext(file_path)  # Split file path to get the file name without extension

    with open(file_path, 'r') as file:
        file_content = file.read()

    llm = OpenAI(model="gpt-3.5-turbo", api_key=os.getenv('OPEN_API_KEY'))

    # Define the prompt and JSON example
    prompt = ChatPromptTemplate(
        message_templates=[
            ChatMessage(
                role="system",
                content=(
                    "You are an expert assistant for converting content into correct JSON format.\n"
                    "Generate a valid JSON in the correct format:\n"
                ),
            ),
            ChatMessage(
                role="user",
                content=(
                    "Here is the content: \n"
                    "------\n"
                    "{file_content}\n"
                    "------"
                ),
            ),
        ])

    # Format messages using the prompt and provided content
    messages = prompt.format_messages(file_content=file_content)

    # Use OpenAI's LLM to process the messages and extract response
    output = llm.chat(messages, response_format={"type": "json_object"}).message.content

    # Write the output to a JSON file
    with open(file_name + "_output.json", "w") as json_file:
        json.dump(output, json_file, indent=4)

    return output

def model(mail):
    # from agents import EmailAgents
    # from agents import EmailTasks

    agents = EmailAgents()
    tasks = EmailTasks()
    ## Agents
    validator_agent = agents.make_validator_agent()
    categorizer_agent = agents.make_categorizer_agent()
    # researcher_agent = agents.make_researcher_agent()
    email_writer_agent = agents.make_email_writer_agent()

    ## Tasks
    validate_email = tasks.validating_email(mail,validator_agent)
    categorize_email = tasks.categorize_email(mail,validate_email,categorizer_agent)
    # research_info_for_email = tasks.research_info_for_email(mail,categorize_email)
    draft_email = tasks.draft_email(mail,email_writer_agent,validate_email,categorize_email)


    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[validator_agent,categorizer_agent, email_writer_agent],
        tasks=[validate_email,categorize_email, draft_email],
        verbose=2,
        process=Process.sequential,
        full_output=True,
        share_crew=False
    )

    # Kick off the crew's work
    results = crew.kickoff()
    file1 = 'validator_email.txt'
    file2 = 'email_category.txt'
    file3 = 'draft_email.txt'

    json1 = extract_information_from_agents(file1)
    json2 = extract_information_from_agents(file2)
    json3 = extract_information_from_agents(file3)
    
    return {"json1":json1,"json2":json2,"json3":json3}
    # return results
    # Print the results
    # print("Crew Work Results:")
    # print(results)

    # # print(f"Categorize Email: {categorize_email.output}")
    # print(crew.usage_metrics)


# Example usage
# po_number = process_emails_for_po()
# print(f'Extracted PO Number: {po_number}')