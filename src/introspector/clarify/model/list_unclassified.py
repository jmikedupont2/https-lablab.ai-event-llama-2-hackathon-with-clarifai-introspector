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

#import requests

#FIFTEEN_MINUTES = 900

#os.path.

PAT = simple.model.api_key
USER_ID = simple.model.user_id
APP_ID = simple.model.app_id
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
stream_inputs_response = stub.StreamInputs(
    service_pb2.StreamInputsRequest(
        user_app_id=userDataObject,
        per_page=PAGE,
    ),
    metadata=metadata
)
if stream_inputs_response.status.code != status_code_pb2.SUCCESS:
    print(stream_inputs_response.status)
    raise Exception("Stream inputs failed, status: " + stream_inputs_response.status.description)

def write_input(input_object):
    fn = "outputs/"+input_object.id
    overwrite = 0
    if not os.path.exists(fn):
        overwrite = 1
    elif os.path.getsize(fn) == 0 :
        overwrite =1        
    if overwrite:
        data = None
        #import pdb
        #pdb.set_trace()
        data2 =  requests.get(input_object.data.text.url)


        st1 = str(input_object)
        if len (st1) >0:
            with open(fn,"w") as of:               
                of.write("HEADER:"+st1)
                of.write("PAYLOAD:"+data2.text)
                return
            

@limits(calls=5, period=1)
def get_input(input_id):
    get_input_response = stub.GetInput(
        service_pb2.GetInputRequest(
            user_app_id=userDataObject, 
            input_id=input_id
        ),
        metadata=metadata
    )

    #if get_input_response.status.code == 10000:
    #    print("RES1",get_input_response)
    #    print("STAT",get_input_response.status)        
        #print("RATELIMIT")
        #return
        
    if get_input_response.status.code != status_code_pb2.SUCCESS:
        print("STATUS",get_input_response.status)
        print("STATUSCODE",stream_inputs_response.status.code)
        raise Exception("Get input failed, status: " + get_input_response.status.description)

    input_object = get_input_response.input
    #print("DEBUG" +str(input_object))
    #pprint.pprint(
    return input_object
#print(stream_inputs_response)
print("First response (starting from the first input):")
for input_object in stream_inputs_response.inputs:
    #print(stream_inputs_response)
    write_input(input_object)

last_id = stream_inputs_response.inputs[-1].id


    
while last_id != 0:
    stream_inputs_response = stub.StreamInputs(
        service_pb2.StreamInputsRequest(
            user_app_id=userDataObject,
            per_page=PAGE, last_id=last_id), metadata=metadata)

    print(f"Next response (first input is the one following input ID {last_id}):")
    for input_object in stream_inputs_response.inputs:
        write_input(input_object)
    if stream_inputs_response.inputs:
        last_id = stream_inputs_response.inputs[-1].id
    else:
        print(stream_inputs_response)
        last_id = 0
    
