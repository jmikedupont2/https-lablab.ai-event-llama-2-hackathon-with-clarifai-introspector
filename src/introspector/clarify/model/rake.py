import json
# 1. Create a base class `RakeItUpContext` that extends `SimpleContextClarifaiModel` to provide additional functionality for the RakeItUp process.
# 2. Use the `RakeItUpContext` class to read datasets, generate a dynamic workflow, create the workflow, and trigger its execution.
# 3. Write a Python script using our task API to automate the process of running the RakeItUp task.
from workflow_map import ModelWorkflowGenerator
from simple import SimpleContextClarifaiModel
class RakeItUpContext(SimpleContextClarifaiModel):
    def __init__(self):
        super().__init__()
        #self.python_globals_dataset_id = python_globals_dataset_id
        #self.python_globals_dataset = self.app.get_dataset(self.python_globals_dataset_id)

    def get_concepts(self):
        return self.get_dataset_names_with_prefix()
    
    def generate_and_execute_workflow(self):
        # Step 1: Read Datasets
        concepts = self.get_concepts()
        
        # Step 2: Generate Workflow
        workflow_generator = ModelWorkflowGenerator()
        workflow_definition = workflow_generator.generate_workflow(concepts)
        
        # Print the generated workflow definition as JSON
        print(json.dumps(workflow_definition, indent=4))
        
        # Step 3: Create Workflow
        created_workflow = self.app.workflow.create_workflow(name="RakeItUp Workflow", definition=workflow_definition)
        
        # Step 4: Trigger Workflow
        created_workflow_result = created_workflow.trigger()
        
        # Print the result of triggering the workflow
        print("Workflow triggered:", created_workflow_result)

        
        
    def get_dataset_names_with_prefix(self, prefix="cf_dataset"):
        dataset_names = {}
        app =self.app
        datasets = app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            if name.startswith(prefix):
                concept = name.replace(prefix,"")
                dataset_names[name]=concept
        return dataset_names


# 2. Write a Python Script Using Our Task API:

# ```python

if __name__== "__main__":

    # Create an instance of RakeItUpContext
    rake_it_up_context = RakeItUpContext()

    # Execute the RakeItUp workflow
    rake_it_up_context.generate_and_execute_workflow()
# ```

# This script utilizes the `RakeItUpContext` class to perform the entire RakeItUp process, including reading datasets, generating the workflow, creating the workflow, and triggering its execution.

# Please replace `'YOUR_API_KEY'`, `'YOUR_PYTHON_GLOBALS_DATASET_ID'`, and adjust the import statement with your actual values and module names.

# If you need any further assistance or have questions, feel free to ask!


# Sure, here's how you can create a subclass of your `SimpleContextClarifaiModel` to add the `RakeItUp` class:


# # ```python
# class RakeItUpContext(SimpleContextClarifaiModel):
#     def __init__(self, app_id, app_user_id):
#         super().__init__(app_id, app_user_id)
#         self.rake = RakeItUp()
#         self.workflow_generator = WorkflowGenerator()
                
#     def generate_dynamic_workflow(self, dataset_ids):
#         # Generate the dynamic workflow based on dataset IDs
#         self.workflow_generator.generate_workflow(dataset_ids)

#         # Print the generated workflow definition as JSON
#         print(json.dumps(self.workflow_generator.workflow_definition, indent=4))

#     def load_unassigned_inputs(self):
#         unassigned_inputs = []

#         # Fetch unassigned inputs from Clarifai API
#         unassigned_inputs_response = self.app.inputs.list(search=resources_pb2.SearchInputsRequest(unassigned=True))
        
#         # Extract input data from the response
#         for input_ in unassigned_inputs_response.inputs:
#             unassigned_inputs.append(input_.data.text)

#         return unassigned_inputs


#     def sweep_inputs_to_python_globals(self):
#         # Retrieve unassigned inputs using Clarifai API (replace with your API call)
#         unassigned_inputs = self.load_unassigned_inputs()

#         # Create ClarifaiDataLoader instance for PythonGlobals dataset
#         python_globals_loader = ClarifaiDataLoader(dataset=self.python_globals_dataset)

#         # Assign unassigned inputs to PythonGlobals dataset
#         for input_data in unassigned_inputs:
#             input_proto = Input(data=Data(image=input_data))  # Replace with appropriate field
#             response = python_globals_loader.save_inputs([input_proto])

#         # Upload the assigned inputs to the dataset
#         response = python_globals_loader.flush()
#         if response.status.code != status_code_pb2.SUCCESS:
#             print("Error while uploading inputs:", response.status.description)
#         else:
#             print("Inputs successfully uploaded to PythonGlobals dataset.")
# # ```

# # In this code, I've added a method `sweep_inputs_to_python_globals` to the `RakeItUpContext` class. You can replace `unassigned_inputs` with the actual list of unassigned input data you retrieve from the API, and adjust the field name in the `input_proto` creation to match your data structure.

# # By using this `RakeItUpContext` class, you can have the functionalities of both `SimpleContextClarifaiModel` and `RakeItUp` in a single context object.
# Sure, here's how you can modify the `RakeItUpContext` class to set the `python_globals_dataset` based on the dataset ID provided and look up the dataset in the app by name:

# ```python
# class RakeItUpContext(SimpleContextClarifaiModel):
#     def __init__(self, app_id, app_user_id, python_globals_dataset_id):
#         super().__init__(app_id, app_user_id)
#         self.python_globals_dataset_id = python_globals_dataset_id
#         self.python_globals_dataset = self.app.get_dataset(self.python_globals_dataset_id)
        
#     # ... (other methods)

#     def sweep_inputs_to_python_globals(self):
#         # Load unassigned inputs
#         unassigned_inputs = self.load_unassigned_inputs()

#         # Add unassigned inputs to PythonGlobals dataset
#         self.python_globals_dataset.add_inputs(unassigned_inputs)

# # Specify the PythonGlobals dataset ID
# python_globals_dataset_id = "your_dataset_id_here"

# # Create an instance of RakeItUpContext
# rake_it_up_context = RakeItUpContext(app_id=self.app_id, app_user_id=self.user_id, python_globals_dataset_id=python_globals_dataset_id)

# # Call the method to sweep unassigned inputs into PythonGlobals dataset
# rake_it_up_context.sweep_inputs_to_python_globals()
# ```

# Make sure to replace `"your_dataset_id_here"` with the actual dataset ID you want to use for the `python_globals_dataset`. This code sets up the `python_globals_dataset` using the provided dataset ID and then adds the unassigned inputs to that dataset.

# Certainly, here's the modified `RakeItUpContext` class that sets the `python_globals_dataset` based on the provided dataset ID and looks up the dataset in the app by name:

# ```python
# class RakeItUpContext(SimpleContextClarifaiModel):
#     def __init__(self, app_id, app_user_id, python_globals_dataset_id):
#         super().__init__(app_id, app_user_id)
#         self.python_globals_dataset_id = python_globals_dataset_id
#         self.python_globals_dataset = self.app.get_dataset(self.python_globals_dataset_id)

#     def load_datasets(self):
#         dataset_index = {}
# for app in apps:                                                                                   datasets = app.list_datasets()
#     for ds in datasets:                                                                                name = ds.dataset_info.id
#         dataset_index[name] = ds
#     for model_name in models:
#         idn = "cf_dataset_"+ model_name.lower()
#         if idn not in dataset_index:
#             dataset = app.create_dataset(dataset_id=idn)
#         else:
#             models[model_name].set_dataset(dataset_index[idn])
#         models[model_name].sync()
        
#     def load_unassigned_inputs(self):
#         unassigned_inputs = []

#         # Fetch unassigned inputs from Clarifai API
#         unassigned_inputs_response = self.app.inputs.list(search=resources_pb2.SearchInputsRequest(unassigned=True))
        
#         # Extract input data from the response
#         for input_ in unassigned_inputs_response.inputs:
#             unassigned_inputs.append(input_.data.text)

#         return unassigned_inputs

#     def sweep_inputs_to_python_globals(self):
#         # Load unassigned inputs
#         unassigned_inputs = self.load_unassigned_inputs()

#         # Add unassigned inputs to PythonGlobals dataset
#         self.python_globals_dataset.add_inputs(unassigned_inputs)

# # Specify the PythonGlobals dataset ID
# python_globals_dataset_id = "your_dataset_id_here"

# # Create an instance of RakeItUpContext
# rake_it_up_context = RakeItUpContext(app_id=self.app_id, app_user_id=self.user_id, python_globals_dataset_id=python_globals_dataset_id)

# # Call the method to sweep unassigned inputs into PythonGlobals dataset
# rake_it_up_context.sweep_inputs_to_python_globals()
# # ```

# # # This code ensures that the `python_globals_dataset` is set based on the provided dataset ID, and then you can call the `sweep_inputs_to_python_globals` method to sweep unassigned inputs into the `python_globals_dataset`. Replace `"your_dataset_id_here"` with the actual dataset ID you want to use.
# # Certainly! Here's the modified `RakeItUpContext` class that uses the `WorkflowGenerator` to generate the workflow definition based on the provided dataset IDs:

# # ```python
# from clarifai.rest import ClarifaiApp
# from clarifai.rest import Image as ClImage
# from clarifai.rest import Data, Input
# from clarifai.grpc.api import resources_pb2
# from clarifai.grpc.api.status import status_code_pb2
# import json

# class RakeItUpContext(SimpleContextClarifaiModel):
#     def __init__(self, app_id, app_user_id, python_globals_dataset_id):
#         super().__init__(app_id, app_user_id)
#         self.python_globals_dataset_id = python_globals_dataset_id
#         self.python_globals_dataset = self.app.get_dataset(self.python_globals_dataset_id)


#     # ... (other methods)


# if __name__== "__main"        
# # Specify the PythonGlobals dataset ID
# python_globals_dataset_id = "your_dataset_id_here"

# # Specify the dataset IDs for generating the dynamic workflow
# dataset_ids = ["dataset_id_1", "dataset_id_2", "dataset_id_3"]

# # Create an instance of RakeItUpContext
# rake_it_up_context = RakeItUpContext(app_id=self.app_id, app_user_id=self.user_id, python_globals_dataset_id=python_globals_dataset_id)

# # Generate and print the dynamic workflow definition
# rake_it_up_context.generate_dynamic_workflow(dataset_ids)

# # ```

# # Replace `"your_dataset_id_here"` with the actual PythonGlobals dataset ID and `"dataset_id_1"`, `"dataset_id_2"`, `"dataset_id_3"` with the dataset IDs you want to use for generating the dynamic workflow.

# # This code creates an instance of `RakeItUpContext`, generates a dynamic workflow using the provided dataset IDs, and prints the generated workflow definition as JSON.
