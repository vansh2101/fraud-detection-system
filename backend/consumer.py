import pika
import json
import base64
import mimetypes
import os
from database import database 
from Services.Priority.Priority import PriorityModel
from Services.Audio.asr import extract_text_from_audio_video
from Services.Video.video_description import VideoCaptioner
from Services.Image.image_description import extract_image_description
from Agents.segregation import classify
from Agents.description_summarizer import summarizer

## Initialize the models
priority_model = PriorityModel()

## Initialize database objects
mongo = database.MongoDB()
milvus = database.MilvusDB()
video_captioner = VideoCaptioner()

def detect_file_type(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type:
        if mime_type.startswith("audio"):
            return "audio"
        elif mime_type.startswith("video"):
            return "video"
        elif mime_type.startswith("image"):
            return "image"

    return None

def complaint_registration():
    HOST = None # the public ip of the server where the RabbitMQ is set up
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='complaints')



    def callback(ch, method, properties, body):
        # PERFORM FUNCTIONS IN HERE WHEN A MESSAGE IS CONSUMED.
        print(f" [x] Received complaint")

        message = json.loads(body.decode('utf-8'))
        filename = message['filename']
        file_data = base64.b64decode(message['file_data'])
        
        # save the media file in a dir for further inference
        dir = os.path.join('files', filename)
        with open(dir, 'wb') as file: 
            file.write(file_data)
        print('File saved')

        # perform further analysis 
        file_type = message['file_type']
        
        audio_transcription = ""
        video_description = ""
        complaint_category = ""
        media_description = ""
        
        if file_type.startswith('audio/'):
            audio_transcription = extract_text_from_audio_video(dir)
            # get audio transcription media_description
            media_description = summarizer(message['text'], audio_transcription, "")
            complaint_category = classify(message['text'], media_description=f"Audio transcription from audio input message : {media_description}")
        
        elif file_type.startswith('video/'):
            audio_transcription = extract_text_from_audio_video(dir)
            video_description = video_captioner.caption_video(video_path=dir)
            media_description = summarizer(text=message['text'], audio_transcription=audio_transcription, video_description=video_description)
            complaint_category = classify(message['text'], media_description=f"Audio Transcription from video and description of the video  : {media_description}")
        
        elif file_type.startswith('image/'):
            media_description = extract_image_description(dir)
            complaint_category = classify(message['text'], media_description=f"Image description of image input : {media_description}")
        
        else: 
            complaint_category = classify(message['text'], media_description="No supporting media given by the user.")
        
        # Checking for similar complaints
        similarity = milvus.findSimilar(message['text'], dept=complaint_category['dept'])

        if similarity == None: 
            complaint_id = milvus.insertData(data=message['text'])
            # calculate priority
            priority = priority_model.calculate_priority(content=message['text'], dept=complaint_category['dept'], age_of_complaint=1, number_of_similar_complaints=1)
            # create a json to insert to mongodb
            log = {
                'user_id' : 7042690376,
                'complaint_id' : complaint_id, 
                'complaint' : message['original_text'], 
                'department' : complaint_category['dept'], 
                'media' : {
                    'path' : dir, 
                    'type' : file_type
                }, 
            }
            complaint = {
                'complaint_id' : complaint_id, 
                'complaint' : message['text'], 
                'department' : complaint_category['dept'], 
                'sub-department' : complaint_category['sub_dept'], 
                'media' : {
                    'path' : dir, 
                    'type' : file_type
                }, 
                'number_of_similar_complaints' : 1, 
                'media_description' : media_description, 
                'assigned' : False, 
                'age' : 1, 
                'priority' :  priority
            }
            mongo.insertData(complaint, complaint_category['dept'])
            mongo.insertData(log, 'complaint-logs')
        else:
            # Similar complaint found, hence increment the number of similar complaints 
            complaint_id = similarity
            log = {
                'user_id' : 7042690376,
                'complaint_id' : complaint_id, 
                'complaint' : message['original_text'], 
                'department' : complaint_category['dept'], 
                'media' : {
                    'path' : dir, 
                    'type' : file_type
                }, 
            }
            filter = {'complaint_id' : complaint_id}
            query = {'$inc' : {'number_of_similar_complaints' : 1}}
            mongo.updateData(complaint_category['dept'], filter, query)
            mongo.insertData(log, 'complaint-logs')
        

            
    channel.basic_consume(queue='complaints', on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

