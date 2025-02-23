from fastapi import FastAPI, Response, File, UploadFile, Request, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse, FileResponse
from fastapi.encoders import jsonable_encoder
from db.supabase import create_supabase_client
from db.models import Complaints
from routes.models import ImageComplaint
from utils.tools import generateTextDesc, generatePriority, generateDepartment, generateVidDesc, translateComplaint, extractPNR
from io import BytesIO
from PIL import Image
import os 
import base64
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import uuid
import datetime


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# supabase = create_supabase_client()
supabase = MongoClient("mongodb+srv://root:root123@railmadad.zw0i3.mongodb.net/?retryWrites=true&w=majority&appName=RailMadad", server_api=ServerApi('1'))
print(supabase.list_database_names())
db = supabase['rail-madad']
print(db.list_collection_names())

sample = {
        'complaint_id': 3,
        'complaint': "The sanitation and hygiene in the medical cabin are very poor.",
        'department': 'medical',
        'sub_department': 'hygiene',
        'number_of_similar_complaints': 1,
        'assigned': False,
        'assigned_official': 0,
        'age': 0,
        'timestamp': datetime.datetime.now(datetime.timezone.utc),
        'priority': 88
    }

pnr_data = {
    "2921001863": {
        "pnrNumber": "2921001863",
        "dateOfJourney": "Nov 2, 2024 3:20:53 PM",
        "trainNumber": "22425",
        "trainName": "VANDE BHARAT EXP",
        "sourceStation": "AYC",
        "destinationStation": "ANVT",
        "reservationUpto": "ANVT",
        "boardingPoint": "AYC",
        "journeyClass": "CC",
        "numberOfpassenger": 1,
        "chartStatus": "Chart Prepared",
        "timeStamp": "Nov 7, 2024 1:05:53 AM",
        "trainCancelStatus": "Train has Departed, Booking not allowed",
        "bookingFare": 1280,
        "ticketFare": 1280,
        "quota": "GN",
        "reasonType": "C",
        "ticketTypeInPrs": "E",
        "waitListType": 0,
        "bookingDate": "Sep 15, 2024 12:00:00 AM",
        "arrivalDate": "Nov 7, 2024 11:40:53 PM",
        "mobileNumber": "",
        "distance": 629,
        "isWL": "N",
        "phoneNumber": "919910593396"
    }
}

@app.get("/")
def read_root():
    return {"message": "Rail Madad Backend"}


class RoutedComplaints(BaseModel):
    complaint_id : int
    complaint: str
    department: str
    sub_department: str
    number_of_similar_complaints: int
    assigned: bool
    assigned_official: int
    age: int
    timestamp: datetime.datetime
    priority: float
    phone_number: str
    pnr: str


class Official(BaseModel):
    official_id : int
    assigned_complaints: list
    in_progress: int
    phone_number: int
    department: str
    number_of_assigned_complaints: int
    name: str


class Feedback(BaseModel):
    sentiment: str
    user_phone_number: str
    feedback: str



@app.get("/get-all-complaints")
def get_all_complaints():
    cursor = db['complaints'].find({})
    complaints = cursor.to_list(length=None)

    data = [RoutedComplaints(**complaint).model_dump(mode='json') for complaint in complaints]

    print(data)

    return data


@app.get("/get-all-officials")
def get_all_complaints():
    cursor = db['officials'].find({})
    complaints = cursor.to_list(length=None)

    data = [Official(**complaint).model_dump(mode='json') for complaint in complaints]

    print(data)

    return data


@app.get("/get-all-feedbacks")
def get_all_complaints():
    cursor = db['feedbacks'].find({})
    complaints = cursor.to_list(length=None)

    data = [Feedback(**complaint).model_dump(mode='json') for complaint in complaints]

    print(data)

    return data


@app.get("/get-complaints/{department}")
def get_complaints(department):
    complaints = supabase.table("Complaints").select("*").eq("department", department).execute()
    print(complaints)
    return complaints

@app.get("/get-complaint/{id}")
def get_complaint(id):
    print(id)
    print(type(id))
    cursor = db['complaints'].find_one({'complaint_id' : int(id)})

    print(cursor)

    res = RoutedComplaints(**cursor).model_dump(mode='json')
    print(res)
    return res
    
    # complaint = supabase.table("Complaints").select("*").eq("id", id).execute()
    # print(complaint)
    # return complaint


@app.get("/get-image/{id}")
def get_image(id):
    return FileResponse(f"./uploaded_images/{id}")


@app.post("/create-complaint")
async def create_complaint(complaint: Request):
    print(0)
    complaint = await complaint.json()

    print(complaint)

    try:
        pnr = complaint['pnr']
        if pnr.strip() == '':
            complaint['pnr'] = await extractPNR(complaint['description'])
    except:
        complaint['pnr'] = await extractPNR(complaint['description'])

    print(1)
    async with httpx.AsyncClient() as client:
        # print(11)
        # response = await client.post("http://34.28.79.173:8000/services/categorize", json={
        #     "description": complaint['complaint'] + '\n' + complaint['description']
        # })
        # print(2)
        # complaint['department'] = response.json()
        # print(3)

        # res = await client.post("http://34.28.79.173:8000/services/sub-categorize", json={
        #     "complaint": complaint['description'],
        #     "category": complaint['department']
        # })
        # print(4)
        # print(res)
        # complaint['sub_department'] = res.json()
        # print(res.json())
        # print(5)

        comp = await translateComplaint(complaint['description'])

        score = await client.post("http://34.28.79.173:8000/services/priority", json={
            "complaint": comp,
            "department": complaint['department']
        })
        print(4)
        complaint['priority_score'] = score.json()
        print(score.json())
        print(5)


    # complaint['pnr'] = ''
    complaint['image'] = ''
    print(complaint)
    id = uuid.uuid4().int % (10 ** 6)
    # supabase.table("Complaints").insert(complaint).execute()
    with supabase.start_session() as session:
        print(6)
        with session.start_transaction():
            print(7)
            data = {
                'complaint_id': id,
                'complaint': complaint['description'],
                'department': complaint['department'].lower().strip(),
                'sub_department': complaint['sub_department'],
                'number_of_similar_complaints': 1,
                'assigned': False,
                'assigned_official': 0,
                'age': 0,
                'timestamp': datetime.datetime.now(datetime.timezone.utc),
                'priority': complaint['priority_score'],
                'phone_number': '919910593396',
                'pnr': complaint['pnr']
            }

            db['complaints'].insert_one(data, session=session)

            data2 = {
                'id': id,
                'complaint': complaint['description'],
                'phone_number': '919910593396',
                'resolved': False
            }
            db['complaint_logs'].insert_one(data2, session=session)


    print(7)
    return {"message": "Complaint created successfully"}


@app.post('/send-photo-complaint')
async def photo_complaint(file: UploadFile = File(...)):
    print("Image received")

    file_location = f"./uploaded_images/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    print('Image saved')
    res = await generateTextDesc(file_location)
    res = jsonable_encoder(res)
    return JSONResponse(content=res)


@app.post('/send-vid-complaint')
async def photo_complaint(file: UploadFile = File(...)):
    print("Vid received")

    file_location = f"./uploaded_images/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())

    print('Vid saved')
    res = await generateVidDesc(file_location)
    res = jsonable_encoder(res)
    return JSONResponse(content=res)


@app.post("/get-priority-score")
async def get_priority_score(complaint: str):
    print(complaint)
    score = await generatePriority(complaint)
    # print(score)
    res = jsonable_encoder(score)
    return JSONResponse(content=res)


@app.post('/resolve_complaint')
async def resolve_complaint(req : Request):
    data = await req.json()
    try:
        with supabase.start_session() as session:
            with session.start_transaction():
                # update the officials information
                db['officials'].update_one(
                    {'official_id' : data['official_id']}, 
                    {'$pull' : {'assigned_complaints' : data['complaint_id']}, '$inc' : {'number_of_assigned_complaints' : -1}}, 
                    session=session
                )

                db['complaints'].delete_one({'complaint_id' : data['complaint_id']}, session=session)

                db['complaint_logs'].update_one(
                    {'complaint_id' : data['complaint_id']},
                    {'$set' : {'resolved' : True}},
                    session=session
                )
    except HTTPException as e:
        print(e)
        return JSONResponse('Internal server error', status_code=500)


    data = {
            "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY3NTY1NzlmODA1YWFmMGJlZGJlMTc1NiIsIm5hbWUiOiJKYWluIExpZmUgRm91bmRhdGlvbiIsImFwcE5hbWUiOiJBaVNlbnN5IiwiY2xpZW50SWQiOiI2NzU2NTc5ZjgwNWFhZjBiZWRiZTE3NTEiLCJhY3RpdmVQbGFuIjoiQkFTSUNfTU9OVEhMWSIsImlhdCI6MTczMzcxMTc3NX0.tdjrQyEND_zG_Px0a1QDJMarMLRVnlNhyPNKOxWhoec",
            "campaignName": "feedback",
            "destination": "7042690376",
            "userName": 'test',
            "source": "new-landing-page form",
            "media": {},
            "templateParams": [],
            "tags": [],
            "attributes": {}
        }

    async with httpx.AsyncClient() as client:
        await client.post("https://backend.aisensy.com/campaign/t1/api/v2", json=data)

    return JSONResponse(content="complaint resolved")