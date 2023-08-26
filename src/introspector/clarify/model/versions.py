#MODEL_ID_1 = 'llama2-7b-chat'
#MODEL_VERSION_ID_1 = "e52af5d6bc22445aa7a6761f327f7129"

class ModelVersionLookup:
    def __init__(self):
        # Initialize the model version map with model names and their latest version IDs
        self.model_version_map = {
            "llama2_labelling_model_id": {"llama2-7b-chat":"e52af5d6bc22445aa7a6761f327f7129"}
        }

    def get_latest_version(self, model_name):
        return self.model_version_map.get(model_name, None)

# Example usage
if __name__ =="__main__":
    model_version_lookup = ModelVersionLookup()
    latest_version = model_version_lookup.get_latest_version("llama2_labelling_model_id")
    print("Latest version:", latest_version)
