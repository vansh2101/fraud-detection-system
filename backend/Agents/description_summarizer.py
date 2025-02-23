from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
import os 
from dotenv import load_dotenv

load_dotenv()

# API keys
os.environ['groq_key'] = os.getenv('groq_key')

model = ChatGroq(model='llama-3.1-8b-instant', api_key=os.environ['groq_key'])

prompt = PromptTemplate(
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
            You will be given either audio transcripts or video descriptions extracted frame-wise along with audio transcriptions. 
            Your task is to make sense of the given descriptions of the media taking reference from text and summarize the descriptions. 
            The text is the complaint that the user has registered and they have attached audio/video files for proof, hence you've to analyze the descriptions and generate a meaningful description that describes the situation accurately. 
            Keep in mind that the audio transcriptions may contain errors and wrong words, accomodate for such things yourself. 
            <|eot_id|><|start_header_id|>user<|end_header_id|>
            Text : {text}\n
            Audio Transcription : {audio_transcription}\n
            Video Description : {video_description} \n
            <|eot_id|><|start_header_id|>assistant<|end_header_id|>
            """, 
    input_variables= ['text', 'audio_transcription' , 'video_description'], 
)

summarizer_agent = prompt | model | StrOutputParser()

async def summarizer(text, audio_transcription, video_description):
    summary = summarizer_agent.invoke({'text' : text, 'audio_transcription' : audio_transcription , 'video_description' : video_description})
    return summary