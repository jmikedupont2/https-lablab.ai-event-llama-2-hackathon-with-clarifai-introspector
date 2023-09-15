from clarifai.client.user import User
import click
import re
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
import hashlib

def parse_line(filen, line):
    pattern = r'json\.aline_(?P<line>\d+)(\.?)_(?P<name>[^=]+)=\s+"(?P<text>.*)";'   
    match = re.match(pattern, line)
    
    if match:
        data = match.groupdict()
        m = hashlib.sha256()
        m.update(str(data).encode("utf-8"))

        idd  = m.hexdigest()

        #data["id"]=idd
        data["filen"]=filen
        
        #print(f"Data: {idd} : {data}")
        return [idd,data]
    else:
        #raise Exception(line)
        print("TODO",line)
        return None


class IntrospectorGron(Common):
    def __init__(self, name, path):
        self.path=os.path.expanduser(path)
        self.name= name

    def load_data(self):
        dataset = []
        path = self.path
        print(path)
        with open (path) as fi:
            for x in fi:
                #print(x)
                dd= parse_line(self.name, x)
                if not dd:
                    pass
                else:
                    (idd,fstr) = dd
                    #print("DATA",idd,fstr)                
                    text_data = resources_pb2.Text(raw=json.dumps(fstr))
                    data = resources_pb2.Data(text=text_data)
                    input_proto = resources_pb2.Input(data=data)
                    dataset.append(input_proto)
                
            print("dataset",path, len(dataset))
        return dataset
        #return []
    
@click.command()
@click.option('--input-path', default=".", help='Path to Directory')
@click.option('--input-name', default="Noname", help='Name of dataset')
def main(input_name, input_path ):
    models = {
        "ReadGron": IntrospectorGron(input_name,input_path ),
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


