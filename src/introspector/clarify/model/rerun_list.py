import pprint
import call_api
from simple import model
import click
import requests 
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from ratelimit import limits, RateLimitException
import simple
PAT = simple.model.api_key
USER_ID = simple.model.user_id
APP_ID = simple.model.app_id
channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

flows =  [
    "RakeItUpV2user",
    "RakeItUpV2app",
    "RakeItUpV2dataset",
                    "RakeItUpV2pythontypes",
                    "RakeItUpV2pythonasts",
                    "RakeItUpV2pythonglobals",
                    "RakeItUpV2python_globals",
                    "RakeItUpV2gitdumpdirectory",
                    "RakeItUpV2readgron",
                    "RakeItUpV2biomes",
                    "RakeItUpV2environments",
                    "RakeItUpV2surroundings",
                    "RakeItUpV2contexts",
                    "RakeItUpV2recursiveacronyms",
                    "RakeItUpV2acronyms",
                    "RakeItUpV2acronyminterpreters",
                    "RakeItUpV2acronymrules",
                    "RakeItUpV2formalsystems",
                    "RakeItUpV2rewritesystems",
                    "RakeItUpV2pytorchmodels",
                    "RakeItUpV2tensorflow",
                    "RakeItUpV2tensors",
                    "RakeItUpV2vectors",
                    "RakeItUpV2attentionmodels",
                    "RakeItUpV2selflearning",
                    "RakeItUpV2selfimprovement",
                    "RakeItUpV2regression",
                    "RakeItUpV2automl",
                    "RakeItUpV2deeplearning",
                    "RakeItUpV2deepgraphlearning",
                    "RakeItUpV2reenforcementlearning",
                    "RakeItUpV2deepgraphsemanticmodels",
                    "RakeItUpV2semanticweb",
                    "RakeItUpV2linkeddata",
            "RakeItUpV2rdf",
            "RakeItUpV2owl",
            "RakeItUpV2onnxmodels",
            "RakeItUpV2botgymsmodels",
            "RakeItUpV2botarenamodels",
            "RakeItUpV2prompts",
            "RakeItUpV2promptmodels",
            "RakeItUpV2promptmodelversions",
            "RakeItUpV2personas",
            "RakeItUpV2tasks",
            "RakeItUpV2issues",
            "RakeItUpV2pullrequests",
            "RakeItUpV2discussions",
            "RakeItUpV2chats",
            "RakeItUpV2conversations",
            "RakeItUpV2projects",
            "RakeItUpV2epics",
            "RakeItUpV2changerequests",
            "RakeItUpV2infrastructurechanges",
            "RakeItUpV2infrastructure",
            "RakeItUpV2concepts",
            "RakeItUpV2workflows",
            "RakeItUpV2webplatforms",
            "RakeItUpV2ontologies",
            "RakeItUpV2models",
            "RakeItUpV2modelversions",
            "RakeItUpV2servicedefinitions",
            "RakeItUpV2streamlit",
            "RakeItUpV2secrets",
            "RakeItUpV2awsaccounts",
            "RakeItUpV2githuborgs",
            "RakeItUpV2githubdiscussions",
            "RakeItUpV2githubwiki",
            "RakeItUpV2wikipedia",
            "RakeItUpV2mediawikis",
            "RakeItUpV2phpprojects",
            "RakeItUpV2pythonprojects",
            "RakeItUpV2cplusplusprojects",
            "RakeItUpV2clanguageprojects",
            "RakeItUpV2compilerprojects",
            "RakeItUpV2languageprojects",
            "RakeItUpV2coqprojects",
            "RakeItUpV2proofengineprojects",
            "RakeItUpV2githubrepos",
            "RakeItUpV2hackathons",
            "RakeItUpV2agisystems",
            "RakeItUpV2chatbots",
            "RakeItUpV2chatplatforms",
            "RakeItUpV2predictionsystems",
            "RakeItUpV2labelingsystems",
            "RakeItUpV2workflowsystems",
            "RakeItUpV2worksystems",
            "RakeItUpV2computerystems",
            "RakeItUpV2metaprograms",
            "RakeItUpV2metamemes",
            "RakeItUpV2memes",
            "RakeItUpV2metaquines",
            "RakeItUpV2quines",
            "RakeItUpV2dicegames",
            "RakeItUpV2athena",
            "RakeItUpV2zeus",
            "RakeItUpV2calliope",
            "RakeItUpV2clio",
            "RakeItUpV2euterpe",
            "RakeItUpV2thaliamelpomene",
            "RakeItUpV2terpsichore",
            "RakeItUpV2erato",
            "RakeItUpV2polyhymnia",
            #""RakeItUpV1app",
            #"RakeItUpV1dataset",
            #"RakeItUpV1pythontypes",
            #"RakeItUpV1pythonasts",
            #"RakeItUpV1pythonglobals",
            ]
            
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

@click.command()
@click.option('--input-file', help='file with inputs')
def main(input_file):
    inputs = []
    print("\t" + input_file)
    with open(input_file) as fi:
        for l in fi:
            data_url = l.strip()
            for workflow in flows:
                try:
                    print(workflow, data_url)
                    call_api.call_workflow(stub, metadata, userDataObject, workflow, data_url)
                except Exception as e:
                    print(e)

if __name__ == "__main__":
    main()
