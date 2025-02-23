from pymilvus import MilvusClient, DataType
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np 
import os 
from dotenv import load_dotenv
load_dotenv()

os.environ['mongodb'] = os.getenv('mongodb')
os.environ['milvus'] = os.getenv('milvus')


"""
Mongo DB schema - 
schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["_id", "complaint_id", "complaint"],
        "properties": {
            "_id": {
                "bsonType": "objectId",
                "description": "Primary key for the document"
            },
            "complaint_id": {
                "bsonType": "string",
                "description": "Complaint ID generated from Milvus"
            },
            "department" : {
                "bsonType" : "string", 
                "description" : "Dept of the complaint"
            }, 
            "complaint": {
                "bsonType": "object",
                "required": ["registration_timestamp", "priority", "assigned"],
                "properties": {
                    "text": {
                        "bsonType": ["string", "null"],
                        "description": "Text input from the user, nullable"
                    },
                    "video": {
                        "bsonType": "object",
                        "properties": {
                            "filepath": {
                                "bsonType": ["string", "null"],
                                "description": "Path of video file uploaded, nullable"
                            },
                        }
                    },
                    "audio": {
                        "bsonType": "object",
                        "properties": {
                            "filepath": {
                                "bsonType": ["string", "null"],
                                "description": "Path of audio file uploaded, nullable"
                            },
                        }
                    },
                    "image": {
                        "bsonType": "object",
                        "properties": {
                            "filepath": {
                                "bsonType": ["string", "null"],
                                "description": "Path of image file uploaded, nullable"
                            },
                        }
                    },
                    "media_description" : {
                        'bsonType' : "string", 
                        'description' : 'description of the media provided'
                    },
                    "number_of_similar_complaints": {
                        "bsonType": "int",
                        "description": "Number of similar complaints"
                    },
                    "registration_timestamp": {
                        "bsonType": "date",
                        "description": "Timestamp of complaint registration"
                    },
                    "priority": {
                        "bsonType": "int",
                        "description": "Priority level of the complaint"
                    },
                    "assigned": {
                        "bsonType": "bool",
                        "description": "Boolean indicating if complaint is assigned"
                    },
                    "assigned_official": {
                        "bsonType": ["string", "null"],
                        "description": "Assigned official, nullable if not assigned"
                    }
                }
            }
        }
    }
}
"""

class MilvusDB():
    def __init__(self, uri = os.environ['milvus']):
        self.__client = MilvusClient(
            uri=uri
        )
        self.__ef = SentenceTransformer('BAAI/bge-base-en-v1.5')
        if 'rail_madad' not in self.__client.list_databases():
            self.__client.create_database('rail_madad')

        # Creating collections for every main categories. 
        for dept in ['sanitation', 'security', 'electrical', 'ticketing_booking', 'medical']:
            if  dept not in self.__client.list_collections():
                # Creating custom schema for the collection
                schema  = self.__client.create_schema(
                    auto_id = True,    
                )
                schema.add_field(field_name='complaint_id', datatype=DataType.INT64, is_primary = True)
                schema.add_field(field_name='vector', datatype=DataType.FLOAT_VECTOR, dim = 768)

                # Adding index parameters
                index_params = self.__client.prepare_index_params()

                # adding 2 indices for faster search.
                index_params.add_index(
                    field_name='complaint_id', 
                    index_type='STL_SORT'
                )
                index_params.add_index(
                    field_name='vector', 
                    index_type='FLAT',
                    metric_type = 'L2'
                )
                self.__client.create_collection(
                collection_name=dept, 
                index_params=index_params, 
                schema=schema
                )
                print(f'{dept} collection created')

            else :
                print('Session established with existing collection')
    
    # Insert a new complaint
    def insertData(self, data : str):
        embeds = self.__ef.encode([data], normalize_embeddings= True)
        # print(list(np.array(embeds).squeeze()))
        complaint_ids = self.__client.insert(collection_name='complaints', data={'vector' : list(np.array(embeds).squeeze())})
        return complaint_ids['ids'][0]
    
    # Check for similar complaints
    def findSimilar(self, data : str, dept : str):
        embeds = self.__ef.encode([data], normalize_embeddings= True)
        query_vector = list(np.array(embeds).squeeze())

        THRESHOLD = 0.9
        res = self.__client.search(
            collection_name=dept, 
            anns_field='vector', 
            data = [query_vector], 
            limit=1, 
            search_params= {
                "metric_type" : "IP"
            }
        )
        ## CODE TO CHECK FOR SIMILARITY THRESHOLD
        if len(res[0]) == 0: 
            return None
        return res[0][0]['complaint_id']
    
    def dropCollection(self, collection : str): 
        self.__client.drop_collection(collection_name=collection)
        print('collection dropped')
        return 



class MongoDB():
    def __init__(self, uri = os.environ['mongodb']):
        self.__client = MongoClient(uri)
        self.__db = self.__client['rail-madad']
        '''
        collections in db ->
        complaint-logs : user's number, complaint ID from milvus and original complaint payload 
        departmentatlized complaints collections - 
        '''
        
        # if 'complaints' not in self.__db.list_collection_names():
        #     self.__collection = self.__db.create_collection('complaints')

    def insertData(self, data, collection):
        collec = self.__db[collection]
        res = collec.insert_one(data)
        return res
    
    def updateData(self, collection, filter, query):
        collec = self.__db[collection]
        collec.update_one(filter, query)
        return

    def dropCollection(self, collection : str):
        c = self.__db[collection]
        c.drop()
        return 
