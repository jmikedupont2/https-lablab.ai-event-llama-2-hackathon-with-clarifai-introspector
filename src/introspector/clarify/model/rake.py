import json
import versions
import pprint
import pdb

from clarifai.models.api import Models
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

        for concept in workflow_definitions:
            print("CONCEPT",concept)
            workflow_definition = workflow_definitions[concept]
            print("workflow_definition",workflow_definition)
            # Define your prompt template
            #####
            #pdb.set_trace()
            workflow_nodes = [
                #WorkflowNode(
                 #   id="Input",
                 #   model= {"id": "text-embedding"},
                #)
            ]
            prev_node_id = None
            for i,node in enumerate(workflow_definition["nodes"]):
                inputs = []
                for x in  node.get("inputs", {}):
                    #pprint.pprint({"INPUT":x})
                    inputs.append(NodeInput(node_id=x))
                    model_id = "None"
                    model = None
                    if "model" in node:
                        if node["model"]:
                            model_id = node["model"]["id"]
                        if model_id == "dynamic-prompter":
                            prompt_template = f"Hello, From the concept of {concept}, please evalute how the following statement relates  :'''{{data.text.raw}}'''. Your response:"

                            # Create a prompt model
                            aprompt_model = None
                            model_id  ='pmv2_' +concept
                            try :
                                aprompt_model =self.app.model(model_id)
                            except Exception as e:
                                print(e)
                
                            if aprompt_model is not None:
                                self.app.delete_model(
                                model_id=model_id)
                                aprompt_model= None
                                
                            if aprompt_model is None:
                                auth = self.get_auth_helper()
                                model_api = Models(auth)
                                resp = model_api.create_prompt_model(
                                    app_id=self.app_id,
                                    user_id=self.user_id,
                                    model_id=model_id,
                                    prompt= prompt_template,
                                    position="TEMPLATE",
                                )
                                #pdb.set_trace()
                                #model_id = resp.id
                                latest_version = [
                                    resp.id, resp.model_version.id
                                ]
                                #pprint.pprint(resp)
                        else:                           
                            latest_versions = model_version_lookup.get_latest_version(
                                model_id)
                            if latest_versions:
                                latest_version =  list(latest_versions.items())[0]
                        version_id = latest_version[1]
                        #print("LATEST VERSION",latest_version,version_id)
                        model=Model(
                            id=latest_version[0],
                            model_version=ModelVersion(
                                id=version_id,
                            ))
                        #print("LATEST MODEL",model)
                        args =dict(
                            model=model,
                        )

                        ### if second node, string to first
                        ### fixme
                        if prev_node_id is not None:
                            args["node_inputs"]=[ 
                                NodeInput(node_id=prev_node_id)
                            ]
                        #args.update()

                        node_id = node["id"]
                        args["id"]=node_id
                        prev_node_id = node_id
                        node2 = WorkflowNode(**args)
                        pprint.pprint({"DEBUG_NODE" : [i, node, args]})
                        pprint.pprint({"DEBUG_NODE OUT" : [i, node2]})
                        workflow_nodes.append(node2)

                        # nodes=[
                        #     WorkflowNode(
                        #         id=NODE_ID_1,
                        #         model=Model(
                        #             id=MODEL_ID_1,
                        #             model_version=ModelVersion(
                        #                 id=MODEL_VERSION_ID_1
                        #         )
                        #         )
                        #     ),
                        #     resources_pb2.WorkflowNode(
                        #     id=NODE_ID_2,
                        #         model=resources_pb2.Model(
                        #             id=MODEL_ID_2,
                        #             model_version=resources_pb2.ModelVersion(
                        #                 id=MODEL_VERSION_ID_2
                        #             )
                        #         ),
                        #     ),
                        # ]

            #pdb.set_trace()    
            pprint.pprint({"WORKFLOW":workflow_nodes})
            created_workflow = self.app.delete_workflow(workflow_id="RakeItUpV1"+concept)
            created_workflow = self.app.create_workflow(
                workflow_id="RakeItUpV1"+concept,
                nodes=workflow_nodes)
            # Step 4: Trigger Workflow
            #created_workflow_result = created_workflow.trigger()
        
            # Print the result of triggering the workflow
            #print("Workflow triggered:", created_workflow_result)
        
        
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
