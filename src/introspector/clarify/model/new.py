from clarifai.client.user import User
import os
import json
import os.path
import pprint
from clarifai_grpc.grpc.api import resources_pb2

chunk_size = 10
# clarifai/datasets/upload/base.py
# from clarifai.datasets.upload.utils import load_dataloader, load_module_dataloader

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
            print(len(inputs))
            self.dataset.input_object._bulk_upload(inputs=inputs, chunk_size=chunk_size)


class Types(Common):
    pass


class Apps(Common):
    pass


class DataSets(Common):
    pass


class Users(Common):
    pass


class Asts(Common):
    pass


# must be set as env vars
config = {}

with open(os.path.expanduser("~/.clarify")) as fi:
    config = json.load(fi)

redaction = list(config.values())


def redact(s):
    for k in redaction:
        s = s.replace(str(k), "REDACTED")
    return s


CREATE_APP_USER_ID = config["user_id"]
CREATE_APP_ID = config["app_id"]
api_key = config["key"]
os.environ["CLARIFAI_PAT"] = api_key


client = User(user_id=CREATE_APP_USER_ID)
apps = client.list_apps()


class Globals(Common):
    def __init__(self):
        pass

    # , split: str = "train"):
    # self.split = split
    # self.image_dir = {"train": os.path.join(os.path.dirname(__file__), "images")}

    def load_data(self):
        dataset = []
        for objectn in globals():
            value = globals()[objectn]
            fstr = redact(str(value))
            labels = [objectn, str(type(value))]
            labels.extend(dir(value))
            labels.extend(dir(type(value)))
            text_data = resources_pb2.Text(raw=fstr)
            data = resources_pb2.Data(text=text_data)
            input_proto = resources_pb2.Input(
                data=data,
                # labels=labels,
                # id=str(id(value))
            )
            dataset.append(input_proto)
        return dataset


models = {
    "User": Users(),
    "App": Apps(),
    "DataSet": DataSets(),
    "PythonGlobals": Globals(),
    "PythonTypes": Types(),
    "PythonAsts": Asts(),
}
dataset_index = {}
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

    # # Get a list of inputs
    # inputs = app.inputs.list()

    # # Print input details
    # for input_ in inputs:
    #     print(f"Input ID: {input_.input_id}")
    #     if 'data' in input_:
    #         print(f"Input Data: {input_.data}")
    #     if 'created_at' in input_:
    #         print(f"Created At: {input_.created_at}")

    # text_data = ["Sample text 1.", "Another example text."]
    # response = app.inputs.create(concepts=text_data)

    # for input_ in response['inputs']:
    #     print(f"Input ID: {input_['id']}, Status: {input_['status']['description']}")

    # # 5. **Label Inputs Programmatically:**
    # #    input_id = 'your_input_id'
    # #    response = app.inputs.update(input_id, concepts=['label1', 'label2'])

    # # 6. **Create Custom Models and Train:**
    # #    You can create custom models and train them using the `app.models.create()` and `model.train()` methods.
    # #    model = app.models.create('your_model_name', concepts=['concept1', 'concept2'])
    # #    model.train()

    # # 7. **Make Predictions:**
    # #    Use the `model.predict()` method to make predictions with your trained models.
    # #    prediction = model.predict(url='https://example.com/image.jpg')

    pprint.pprint(models)
