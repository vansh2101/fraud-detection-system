import os 
from dotenv import load_dotenv
import google.generativeai as genai


os.environ['google_key'] = os.getenv('google_key')
genai.configure(api_key=os.environ['google_key'])

gemini = genai.GenerativeModel(model_name='gemini-1.5-flash-8b')
def extract_image_description(file_path : str, complaint_description : str):
    media_description = gemini.generate_content([f'Generate description of the provided image, explaining the issue visually described in the given complaint : {complaint_description}', file_path])
    return media_description