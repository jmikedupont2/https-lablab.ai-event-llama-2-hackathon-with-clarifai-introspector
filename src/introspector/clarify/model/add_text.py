from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

def add_text(stub,userDataObject,metadata,fstr):
    text_data = resources_pb2.Text(raw=fstr)
    data = resources_pb2.Data(text=text_data)
    post_inputs_response = stub.PostInputs(
        service_pb2.PostInputsRequest(
            user_app_id=userDataObject,
            inputs=[
                resources_pb2.Input( data=data)                
            ]
        ),
        metadata=metadata
    )
    
    if post_inputs_response.status.code != status_code_pb2.SUCCESS:
        print(post_inputs_response.status)
        raise Exception("Post inputs failed, status: " + post_inputs_response.status.description)
             
