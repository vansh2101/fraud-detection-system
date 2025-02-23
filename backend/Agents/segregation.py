from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
import os 
from dotenv import load_dotenv
import asyncio
load_dotenv()

# API keys
os.environ['groq_key'] = os.getenv('groq_key')


# models
model = ChatGroq(model='llama-3.1-8b-instant', api_key=os.environ['groq_key'])

# Output Parser for the segregation chain
class SegregrationOutput(BaseModel):
    dept : str = Field(description='The department in which the complaint belongs to.')
    sub_dept : str = Field(description='Sub-category of the complaint for more detail')

# Segregation Chain
output_parser = JsonOutputParser(pydantic_object=SegregrationOutput)
prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You will be given a complaint with its textual description along with media description (audio/video/image attached with the complaint). 
            You have to categorize the complaint into 5 major categories and also give their sub category after analysing the complaint in detail. 
            Below is the details about each category and a list of sub-categories for each.
            Categories/Departments : 
            1. medical
            2. security - 
                Eve-Teasing/Misbehaviour with Lady Passenger/Rape
                Theft of Passenger Belonging/Snatching
                Unauthorized person in Ladies/Disabled Coach/SLR/Reserve Coach
                Harrasment/Extortion by Security Personnel/Railway Personnel
                Nuisance by Hawkers/Beggar/Eunuch
                Luggage Left Behind/Unclaimed/Suspected Article
                Passenger Missing /Not Resoponding Call
                Smoking/Drinking Alcohol/ Narcotics 
                Dacoity/Robbery/ Murder/Riots 
                Passenger Fallen Down 
                Nuisance by passenger
                Misbehave
            3. sanitation - 
                Window/Seat Broken
                Window/Door locking problem
                Tap Leaking/Tap not working
                Broken/Missing Toilet Fiitings
                Jerks/Abnormal Sound
                Toilet 
                Washbasin
                Coach Interior
                Coach Exterior
                Food
            4. electrical - 
                Air Conditioner
                Fans
                Lights
                Charging Point 
            5. ticketing-booking - 

            Example complaints for better understanding --\n
            Medical Complaints
            Subcategory: Medical Emergency
            Complaint: "My father is experiencing severe chest pain in Coach B2. He seems to be in severe condition. Please send medical assistance immediately! my pnr number is 0123456789"
            Subcategory: Medicine/First Aid
            Complaint: "PNR: 9876543210 - I am experiencing a headache and weakness. Can someone provide me with a basic painkiller in Coach S3, berth 46?"
            \n\n
            Security and Safety Complaints
            Subcategory: Theft
            Complaint: "PNR: 1122334455 - Someone stole my bag while I was asleep in Coach S1. I contains all my important documentd and money. Please take immediate action!"
            Subcategory: Harassment
            Complaint: "PNR: 2233445566 - A group of people is behaving inappropriately and making female passengers uncomfortable in Coach S5. When I tried to intervene they misbehaved and even were ready for a fight. Please intervene."
            Subcategory: Suspicious Activity
            Complaint: "PNR: 3344556677 - I noticed an unattended bag near the door of Coach C3. Its a brown bag. It looks suspicious, please check."
            \n\n
            Sanitation Complaints
            Subcategory: Unclean Toilets
            Complaint: "The toilet in Coach A1 is filthy, and very dirty and the water supply isn't working. there is not even soap in soap dispenser. Kindly clean it. pnr num: 0123456789"
            Subcategory: Trash Disposal
            Complaint: "There is a lot of garbage on the platform of station Old Delhi Junction. The garbage is creating a lot of unpleasant smell. Please clean it as soon as possible."
            \n\n
            Ticketing Complaints
            Subcategory: Wrong Ticket Details
            Complaint: "PNR: 7788990011 - My ticket shows Coach S5, berth 32, but someone else is already sitting there. He is insisting that it is his seat, when i asked to show the ticket but he is denying. Please help resolve this."
            Subcategory: Refund Issues
            Complaint: "PNR: 8899001122 - I canceled my ticket a week ago, but I haven’t received the refund yet. when i asked on the ticket counter, they were not able to give eme a satisfactory answer. Please look into this matter."
            Subcategory: Tatkal Booking Issues
            Complaint: "PNR: 9900112233 - I booked a Tatkal ticket, but the transaction failed, and the amount was deducted. Please help me get my booking or a refund."
            \n\n
            Electrical Complaints
            Subcategory: Lights Not Working
            Complaint: "PNR: 1233214567 - The lights in Coach S6 are not working, and it’s very dark. Please fix it as soon as possible."
            Subcategory: Charging Point Issues
            Complaint: "PNR: 2344325678 - None of the charging points in Coach B3 are functional. Please fix them. My phone is about to die."
            
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Classify the following complaint into appropriate deparment and output in the format specified. \n\n
            Complaint Description - {complaint_description} \n
            Media Description - {media_description} \n
            Output Instructions - {output_instructions}
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """, 
    input_variables= ['complaint_description', 'media_description'], 
    partial_variables= {'output_instructions' : output_parser.get_format_instructions()}
)

segregationAgent = prompt | model | output_parser


async def classify(complaint_description, media_description):
    '''
    complaint_description : text input from the user 
    media_descriptionn : descritions of the media files attached with the compalaint
    '''
    
    print('Segregating the complaint....')
    response = segregationAgent.invoke({'complaint_description' : complaint_description, 'media_description' : media_description})
    return response

if __name__ == '__main__':
    res = asyncio.run(classify('There is a bug in my rice which I was served at lunch in coach C4. Please look into this and give me another meal.', ""))
    print(res)