
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
