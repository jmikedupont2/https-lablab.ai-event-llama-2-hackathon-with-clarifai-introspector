import os
import json
from base import BaseClarifaiModel
class SimpleContextClarifaiModel(BaseClarifaiModel):
    def __init__(self):
        self.config = None               
        user_id = self.read_user_id_from_config()
        app_id = self.read_app_id_from_config()

        super().__init__(user_id=user_id,
                         app_id=app_id)
        self.app = self.client.app(app_id=self.app_id)

    def get_user_id_from_config(self):
        config = self.read_config_file()
        return config.get("user_id")

    def read_config_file(self):
        config_file_path = os.path.expanduser("~/.clarify")
        with open(config_file_path) as fi:
            config = json.load(fi)
        return config


    def create_dataset(self, dataset_id):
        if not self.user_id:
            raise ValueError("User ID is not set")

        dataset_index = {}
        datasets = self.app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            dataset_index[name] = ds

        idn = "cf_dataset_" + dataset_id.lower()
        if idn not in dataset_index:
            dataset = self.app.create_dataset(dataset_id=idn)
        else:
            dataset = dataset_index[idn]

        return dataset



if __name__ == "__main__":
    model = SimpleContextClarifaiModel()
#    model.create_datasets()
