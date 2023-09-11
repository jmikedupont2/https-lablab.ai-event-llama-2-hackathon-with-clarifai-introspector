from simple import SimpleContextClarifaiModel
from workflow_labels import FlattenedLabelWorkflowGenerator as WorkflowGenerator
from clarifai_grpc.grpc.api.resources_pb2 import (
    WorkflowNode,
    NodeInput,
    Model,
    ModelVersion,
)

import pdb

import versions
import pprint
from clarifai.models.api import Models

model_version_lookup = versions.ModelVersionLookup()


class RakeItUpContext(SimpleContextClarifaiModel):
    def __init__(self):
        super().__init__()

    def get_concepts(self):
        return self.get_dataset_names_with_prefix()

    def generate_and_execute_workflow(self):
        # Step 1: Read Datasets
        concepts = self.get_concepts()

        # Step 2: Generate Workflow
        workflow_generator = WorkflowGenerator()
        target_model = "llama2_labelling_model_id"
        workflow_definitions = workflow_generator.generate_workflows(
            concepts, target_model
        )

        for concept in workflow_definitions:
            print("CONCEPT", concept)
            workflow_definition = workflow_definitions[concept]
            print("workflow_definition", workflow_definition)
            # Define your prompt template
            #####
            workflow_nodes = []
            prev_node_id = None
            for i, node in enumerate(workflow_definition["nodes"]):
                inputs = []
                for x in node.get("inputs", {}):
                    # pprint.pprint({"INPUT":x})
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
                            model_id = "pmv2_" + concept
                            try:
                                aprompt_model = self.app.model(model_id)
                            except Exception as e:
                                print(e)

                            #if aprompt_model is not None:
                                #self.app.delete_model(model_id=model_id)
                                #aprompt_model = None
                            latest_version = None
                            if aprompt_model is None:
                                auth = self.get_auth_helper()
                                model_api = Models(auth)
                                resp = model_api.create_prompt_model(
                                    app_id=self.app_id,
                                    user_id=self.user_id,
                                    model_id=model_id,
                                    prompt=prompt_template,
                                    position="TEMPLATE",
                                )
                                latest_version = [resp.id, resp.model_version.id]
                                pprint.pprint(resp)
                            else:
                                latest_versions = aprompt_model.list_versions()
                                #pdb.set_trace()   
                                if latest_versions:
                                    resp = list(latest_versions)[0]
                                    latest_version = [resp.id, resp.model_version.id]
                                    
                        else:
                            print("getlatest2")

                            # called for the t2t model
                            latest_versions = model_version_lookup.get_latest_version(
                                model_id
                            )
                            if latest_versions:
                                latest_version = list(latest_versions.items())[0]
                                #pdb.set_trace()
                                print("DEBUG111",latest_version)
                            else:
                                raise Exception(latest_version)
                        print("DEBUG",latest_version)
                        version_id = latest_version[1]
                        model = Model(
                            id=latest_version[0],
                            model_version=ModelVersion(
                                id=version_id,
                            ),
                        )
                        # print("LATEST MODEL",model)
                        args = dict(
                            model=model,
                        )

                        # if second node, string to first
                        # fixme
                        if prev_node_id is not None:
                            args["node_inputs"] = [NodeInput(node_id=prev_node_id)]
                        # args.update()

                        node_id = node["id"]
                        args["id"] = node_id
                        prev_node_id = node_id
                        node2 = WorkflowNode(**args)
                        pprint.pprint({"DEBUG_NODE": [i, node, args]})
                        pprint.pprint({"DEBUG_NODE OUT": [i, node2]})
                        workflow_nodes.append(node2)

            #pprint.pprint({"WORKFLOW": workflow_nodes})
            #created_workflow = self.app.delete_workflow(
            #    workflow_id="RakeItUpV1" + concept
            #)
            try:
                created_workflow = self.app.create_workflow(
                    workflow_id="RakeItUpV2" + concept, nodes=workflow_nodes
                )
                #return created_workflow
            except Exception as e:
                print("error",e)
                #return None
    def get_dataset_names_with_prefix(self, prefix="cf_dataset_"):
        # cf_dataset_
        dataset_names = {}
        app = self.app
        datasets = app.list_datasets()
        for ds in datasets:
            name = ds.dataset_info.id
            concept = name.split("-")[0]
            while concept.startswith(prefix):
                concept = (
                    concept.replace("__", "_").replace("__", "_").replace("__", "_")
                )
                concept = concept.replace(prefix, "")
            dataset_names[name] = concept
        return dataset_names


if __name__ == "__main__":

    # Create an instance of RakeItUpContext
    rake_it_up_context = RakeItUpContext()

    # Execute the RakeItUp workflow
    rake_it_up_context.generate_and_execute_workflow()
