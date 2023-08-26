import json
import versions

model_version_lookup = versions.ModelVersionLookup()
from clarifai_grpc.grpc.api.resources_pb2  import WorkflowNode, NodeInput, Model, ModelVersion
#from workflow_map import ModelWorkflowGenerator
from workflow_labels import FlattenedLabelWorkflowGenerator as WorkflowGenerator
from simple import SimpleContextClarifaiModel

#MODEL_ID_1 = 'llama2-7b-chat'
#MODEL_VERSION_ID_1 = "e52af5d6bc22445aa7a6761f327f7129"

# 1. Create a base class `RakeItUpContext` that extends `SimpleContextClarifaiModel` to provide additional functionality for the RakeItUp process.
# 2. Use the `RakeItUpContext` class to read datasets, generate a dynamic workflow, create the workflow, and trigger its execution.
# 3. Write a Python script using our task API to automate the process of running the RakeItUp task.

#import  clarifai_grpc.grpc.api.resources_pb2

#from clarifai_grpc.grpc.api.status 


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
        workflow_generator = WorkflowGenerator()
        target_model = "llama2_labelling_model_id"
        workflow_definitions = workflow_generator.generate_workflows(concepts,target_model)
        latest_versions = model_version_lookup.get_latest_version(target_model)        
        for concept in workflow_definitions:
            print("CONCEPT",concept)
            workflow_definition = workflow_definitions[concept]
            # Print the generated workflow definition as JSON
            print(json.dumps(workflow_definition, indent=4))        
            # Step 3: Create Workflow
            print("APP",self.app)
            print("WF",self.app.workflow)
            workflow_nodes = []
            print("LATEST VERSIONS",latest_versions)
            latest_version =  list(latest_versions.items())[0]
            print("LATEST VERSION",latest_version)
            model=Model(
                id=latest_version[0],
                model_version=ModelVersion(
                    id=latest_version[1]
                )
            )

            for i,node in enumerate(workflow_definition["nodes"]):
                inputs = []
                for x in  node.get("inputs", {}):
                    inputs.append(NodeInput(node_id=x))
                    
                    if i >= 0:
                        workflow_nodes.append(
                            WorkflowNode(
                                id=node["name"],
                                model=model,
                                node_inputs=inputs,
                            ))
                    else:
                        workflow_nodes.append(
                            WorkflowNode(
                                id=node["name"],
                                #model=model,
                                node_inputs=inputs,
                            ))

                created_workflow = self.app.create_workflow(
                            workflow_id="RakeItUpV1",
                            #name="RakeItUp Workflow",
                    nodes=workflow_nodes)
        
                # Step 4: Trigger Workflow
                created_workflow_result = created_workflow.trigger()
        
                # Print the result of triggering the workflow
                print("Workflow triggered:", created_workflow_result)

        
        
    def get_dataset_names_with_prefix(self, prefix="cf_dataset_"):
        #cf_dataset_
        dataset_names = {}
        app =self.app
        datasets = app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            concept = name.split("-")[0]
            while concept.startswith(prefix):
                concept = concept.replace("__","_").replace("__","_").replace("__","_")
                concept = concept.replace(prefix,"")
            dataset_names[name]=concept
        return dataset_names



if __name__== "__main__":

    # Create an instance of RakeItUpContext
    rake_it_up_context = RakeItUpContext()

    # Execute the RakeItUp workflow
    rake_it_up_context.generate_and_execute_workflow()

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
