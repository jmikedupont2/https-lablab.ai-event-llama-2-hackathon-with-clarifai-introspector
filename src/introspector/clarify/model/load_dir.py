from clarifai.client.user import User
import click
import os
import glob
import json
import os.path
import pprint
from clarifai_grpc.grpc.api import resources_pb2
import logging

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# You must initialize logging, otherwise you'll not see debug output.
#logging.basicConfig()
#logging.getLogger().setLevel(logging.DEBUG)
#requests_log = logging.getLogger("requests.packages.urllib3")
#requests_log.setLevel(logging.DEBUG)
#requests_log.propagate = True

chunk_size = 10

MAIN_APP_ID = "main"
MAIN_APP_USER_ID = "clarifai"
GENERAL_MODEL_ID = "general-image-recognition"
General_Workflow_ID = "General"
CREATE_MODEL_ID = "ci_test_model"
CREATE_WORKFLOW_ID = "ci_test_workflow"
CREATE_DATASET_ID = "ci_test_dataset"
CREATE_MODULE_ID = "ci_test_module"


class Common:
    def load_data(self):
        return []

    def __init__(self):
        self.dataset = None

    def set_dataset(self, dataset):
        self.dataset = dataset

    def sync(self):
        inputs = self.load_data()
        if inputs:
            #print("LEN",len(inputs))

            self.dataset.input_object._bulk_upload(inputs=inputs, chunk_size=chunk_size)


# must be set as env vars
config = {}

with open(os.path.expanduser("~/.clarify")) as fi:
    config = json.load(fi)


CREATE_APP_USER_ID = config["user_id"]
CREATE_APP_ID = config["app_id"]
api_key = config["key"]
os.environ["CLARIFAI_PAT"] = api_key

class GitDumpDirectory(Common):
    def __init__(self, path):
        self.path=os.path.expanduser(path)

    def load_data(self):
        dataset = []
        pth = self.path +"/*"
        for objectn in glob.glob(pth):
            print("name",objectn)
            with open (objectn) as fi:
                try:
                    fstr = fi.read()
                except Exception as e:
                    #print(e)
                    with open (objectn,"rb") as fi2:
                        fstr = str("Error:"+ str(e) +"DATA:" +fi.read())
                        
                    
            #print("DATA",fstr)
            text_data = resources_pb2.Text(raw=fstr)
            data = resources_pb2.Data(text=text_data)
            input_proto = resources_pb2.Input(
                data=data,
                # labels=labels,
                # id=str(id(value))
            )
            dataset.append(input_proto)
        print("dataset",objectn, len(dataset))
        return dataset
    
@click.command()
@click.option('--input-path', default=".", help='Path to Directory')
def main(input_path):

    models = {
        "GitDumpDirectory": GitDumpDirectory(input_path),
    }
    dataset_index = {}
    client = User(user_id=CREATE_APP_USER_ID)
    apps = client.list_apps()

    for app in apps:
        datasets = app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            dataset_index[name] = ds
            for model_name in models:
                idn = "cf_dataset_" + model_name.lower()
                if idn not in dataset_index:
                    dataset = app.create_dataset(dataset_id=idn)
                else:
                    models[model_name].set_dataset(dataset_index[idn])
                    models[model_name].sync()
            
    #print({"models":models})
if __name__ == '__main__':
    main()


