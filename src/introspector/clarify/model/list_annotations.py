import pprint
import json
import os

import time
from simple import model
PAGE=1000
import requests 
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

import simple
from ratelimit import limits, RateLimitException


PAT = simple.model.api_key
USER_ID = simple.model.user_id
APP_ID = simple.model.app_id
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)


list_annotations_response = stub.ListAnnotations(
    service_pb2.ListAnnotationsRequest(
        user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
        list_all_annotations=True,
        per_page=100
    ),
    metadata=metadata
)

if list_annotations_response.status.code != status_code_pb2.SUCCESS:
    print(list_annotations_response.status)
    raise Exception("List annotations failed, status: " + list_annotations_response.status.description)

with open("annotations.json","w") as fo:
    for annotation_object in list_annotations_response.annotations:
        for c in annotation_object.data.concepts:
            d = {
                "id": c.id,
                "name" : c.name,
                "value" :c.value,
                "app_id" :c.app_id,
                "annotate_id":annotation_object.id,
                #"data":str(annotation_object.data.concepts),
                "input_id":annotation_object.input_id,
                "model_version_id":annotation_object.model_version_id,
            }
            json.dump(d,fo)
            fo.write("\n")
