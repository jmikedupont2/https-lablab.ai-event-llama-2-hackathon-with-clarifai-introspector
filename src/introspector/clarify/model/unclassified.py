import pprint
import call_api
from simple import model
import requests 
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

import simple

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = simple.model.api_key
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = simple.model.user_id
APP_ID = simple.model.app_id
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
stream_inputs_response = stub.StreamInputs(
    service_pb2.StreamInputsRequest(
        user_app_id=userDataObject,
        per_page=5,
        # descending = True # Set to reverse order
    ),
    metadata=metadata
)

if stream_inputs_response.status.code != status_code_pb2.SUCCESS:
    print(stream_inputs_response.status)
    raise Exception("Stream inputs failed, status: " + stream_inputs_response.status.description)

print("First response (starting from the first input):")
for input_object in stream_inputs_response.inputs:
    print("\t" + input_object.id)

last_id = stream_inputs_response.inputs[-1].id

# Set last_id to get the next set of inputs. The returned inputs will not include the last_id input.
stream_inputs_response = stub.StreamInputs(
    service_pb2.StreamInputsRequest(
        user_app_id=userDataObject,
        per_page=10, 
        last_id=last_id
    ),
    metadata=metadata
)
def get_input(input_id):
    get_input_response = stub.GetInput(
        service_pb2.GetInputRequest(
            user_app_id=userDataObject, 
            input_id=input_id
        ),
        metadata=metadata
    )
    
    if get_input_response.status.code != status_code_pb2.SUCCESS:
        print(get_input_response.status)
        raise Exception("Get input failed, status: " + get_input_response.status.description)

    input_object = get_input_response.input
    print("DEBUG" +str(input_object))
    pprint.pprint(input_object)

print(f"Second response (first input is the one following input ID {last_id}):")
for input_object in stream_inputs_response.inputs:
    print("\t" + input_object.id)
    pprint.pprint(input_object)
    
    get_input(input_object.id)
    
    data_url = input_object.data.text.url
    #print(x.text)
    for workflow in [
            "RakeItUpV1user",
            "RakeItUpV1app",
            "RakeItUpV1dataset",
            "RakeItUpV1pythontypes",
            "RakeItUpV1pythonasts",
            "RakeItUpV1pythonglobals",
    ]:
        call_api.call_workflow(stub, metadata, userDataObject, workflow, data_url)
#unclassified_inputs = app.inputs.get_all(unclassified=True)

# Print the IDs of the unclassified inputs
#for input_data in unclassified_inputs:
#    print("Input ID:", input_data.id)



#INPUT_ID = 'eec128fd81974543bafff48702edca4d'

##########################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
##########################################################################

