import os
import json
#from clarifai.client.user import User
from clarifai.client.input import Input
from clarifai.client.dataset import Dataset
from clarifai.datasets.upload.base import ClarifaiDataLoader
from clarifai.datasets.upload.features import (TextFeatures)
from clarifai_grpc.grpc.api import resources_pb2, service_pb2
from clarifai_grpc.grpc.api.resources_pb2 import Input
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai.client.user import User
import random
import string

class BaseClarifaiModel:
    
    def __init__(self,  user_id, app_id):
        self.config = None
        self.user_id = user_id
        self.app_id = app_id
        self.init_client()
        

    def read_config(self):
        if self.config is None:
            with open(os.path.expanduser("~/.clarify")) as fi:
                self.config = json.load(fi)
        return self.config
        
    def read_user_id_from_config(self):
        return self.read_config().get("user_id", None)
    
    def read_app_id_from_config(self):
        return self.read_config().get("app_id", None)

    def init_client(self):
        self.api_key = self.read_config().get("key",None)
        os.environ["CLARIFAI_PAT"] = self.api_key

        #client = User(user_id=CREATE_APP_USER_ID)

        self.client = User(user_id=self.user_id)

    def create_dataset_with_suffix(self, base_id, max_attempts=3):
        for attempt in range(1, max_attempts + 1):
            random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            dataset_id = f"{base_id}-{random_suffix}"
            
            #try:
            dataset = self.create_dataset(dataset_id=dataset_id)
            return dataset

    def create_dataset(self, dataset_id):
        if not self.user_id:
            raise ValueError("User ID is not set")

        dataset = service_pb2.Dataset(
            dataset_id=dataset_id,
            data_type=resources_pb2.Text(),
            user_id=self.user_id
        )
        return dataset
