# Sure, here's how you can create a subclass of your `SimpleContextClarifaiModel` to add the `RakeItUp` class:

# ```python
class RakeItUpContext(SimpleContextClarifaiModel):
    def __init__(self, app_id, app_user_id):
        super().__init__(app_id, app_user_id)
        self.rake = RakeItUp()
    def load_unassigned_inputs(self):
        unassigned_inputs = []

        # Fetch unassigned inputs from Clarifai API
        unassigned_inputs_response = self.app.inputs.list(search=resources_pb2.SearchInputsRequest(unassigned=True))
        
        # Extract input data from the response
        for input_ in unassigned_inputs_response.inputs:
            unassigned_inputs.append(input_.data.text)

        return unassigned_inputs


    def sweep_inputs_to_python_globals(self):
        # Retrieve unassigned inputs using Clarifai API (replace with your API call)
        unassigned_inputs = self.load_unassigned_inputs()

        # Create ClarifaiDataLoader instance for PythonGlobals dataset
        python_globals_loader = ClarifaiDataLoader(dataset=self.python_globals_dataset)

        # Assign unassigned inputs to PythonGlobals dataset
        for input_data in unassigned_inputs:
            input_proto = Input(data=Data(image=input_data))  # Replace with appropriate field
            response = python_globals_loader.save_inputs([input_proto])

        # Upload the assigned inputs to the dataset
        response = python_globals_loader.flush()
        if response.status.code != status_code_pb2.SUCCESS:
            print("Error while uploading inputs:", response.status.description)
        else:
            print("Inputs successfully uploaded to PythonGlobals dataset.")
# ```

# In this code, I've added a method `sweep_inputs_to_python_globals` to the `RakeItUpContext` class. You can replace `unassigned_inputs` with the actual list of unassigned input data you retrieve from the API, and adjust the field name in the `input_proto` creation to match your data structure.

# By using this `RakeItUpContext` class, you can have the functionalities of both `SimpleContextClarifaiModel` and `RakeItUp` in a single context object.
Sure, here's how you can modify the `RakeItUpContext` class to set the `python_globals_dataset` based on the dataset ID provided and look up the dataset in the app by name:

```python
class RakeItUpContext(SimpleContextClarifaiModel):
    def __init__(self, app_id, app_user_id, python_globals_dataset_id):
        super().__init__(app_id, app_user_id)
        self.python_globals_dataset_id = python_globals_dataset_id
        self.python_globals_dataset = self.app.get_dataset(self.python_globals_dataset_id)
        
    # ... (other methods)

    def sweep_inputs_to_python_globals(self):
        # Load unassigned inputs
        unassigned_inputs = self.load_unassigned_inputs()

        # Add unassigned inputs to PythonGlobals dataset
        self.python_globals_dataset.add_inputs(unassigned_inputs)

# Specify the PythonGlobals dataset ID
python_globals_dataset_id = "your_dataset_id_here"

# Create an instance of RakeItUpContext
rake_it_up_context = RakeItUpContext(app_id=self.app_id, app_user_id=self.user_id, python_globals_dataset_id=python_globals_dataset_id)

# Call the method to sweep unassigned inputs into PythonGlobals dataset
rake_it_up_context.sweep_inputs_to_python_globals()
```

Make sure to replace `"your_dataset_id_here"` with the actual dataset ID you want to use for the `python_globals_dataset`. This code sets up the `python_globals_dataset` using the provided dataset ID and then adds the unassigned inputs to that dataset.
