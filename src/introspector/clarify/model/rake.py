from simple import SimpleContextClarifaiModel
from workflow_labels import FlattenedLabelWorkflowGenerator as WorkflowGenerator
from clarifai_grpc.grpc.api.resources_pb2 import (
    WorkflowNode,
    NodeInput,
    Model,
    ModelVersion,
)
import emojis
import versions
import pprint
from clarifai.models.api import Models

model_version_lookup = versions.ModelVersionLookup()

def to_model(x):
    #x.replace()
    return "generic"+ str(id(x))

concepts1 = {}

class RakeItUpContext(SimpleContextClarifaiModel):
    def __init__(self):
        super().__init__()
        self.seen ={}
    def get_concepts(self):
        #return self.get_dataset_names_with_prefix()
        m  = emojis.Emojis()
        dataset_names = {}

        for x in m.process():
            #print(x)
            #{'combine': ['Create prompt model that will ', "define the <generator object Emojis.prompt_model at 0x7fc73600d770> with args {'emoji': '📥🔗📜'} using example :'''{data.text.raw}'''"]}
            if "combine" in x:
                c1 = x["combine"]
                x1 = c1[0]
                x2 = c1[1]
                #print("DEBUG",c1, x1, x2)

                if x1 not in concepts1:
                    orig = x1
                    print("DEBUG",x1)
                    concepts1[x1] = 1

                    x1 = x1.strip()
                    x1 = x1.replace(" ","_")
                    x1 = x1.replace("__","_")
                    print("CONCEPT",x1)
                    print("ORIG",orig)
                    if len(orig)<3:
                        raise Exception("nope")
                    #
                    for i,p in enumerate([
                            f"The concept of {orig} and its relationship to the concepts contained in '''{{data.text.raw}}'''",
                            f"The concept of {orig} in '''{{data.text.raw}}'''",
                            f"The concept of {orig} in consideration of the special case of {x1} in '''{{data.text.raw}}'''",
                            f"The concept of {orig} and {x1} in '''{{data.text.raw}}'''",
                            f"Relate {orig} to '''{{data.text.raw}}'''",                        
                    ]):
                        print("DEBUG!ORIG", orig)
                        print("DEBUG!",  x1)
                        print("DEBUG!", str(i))
                        print("DEBUG!P", str(p))
                        
                        dataset_names[x1 +str(i)] = p
                
                #dataset_names[x] = x
        return dataset_names
        

    def generate_and_execute_workflow(self):
        # Step 1: Read Datasets
        all_concepts = self.get_concepts()

        concepts = { a : a for a in list(all_concepts.keys())}
        
        # Step 2: Generate Workflow
        workflow_generator = WorkflowGenerator()
        target_model = "llama2_labelling_model_id"
        workflow_definitions = workflow_generator.generate_workflows(
            concepts, target_model
        )

        for concept in workflow_definitions:
            print("CONCEPT", concept)
            #text_versions = workflow_definitions[concept]
            text_version = all_concepts[concept] 
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
                            #prompt_template = f"Hello, From the concept of {concept}, please evalute how the following statement relates  :'''{{data.text.raw}}'''. Your response:"
                            prompt_template =  concept
                            model_id = "p3"+ concept[:46]
                            if model_id in self.seen:
                                continue
                                
                            # Create a prompt model
                            aprompt_model = None
                            try:
                                aprompt_model = self.app.model(model_id)
                            except Exception as e:
                                print(e)

                            #now we create it
                            #for text in text_versions:
                            latest_version = None
                            prompt_template = text_version
                            text = text_version
                            print("DEBUG TEXT 1",text)
                            if len(text )<10 :
                                raise Exception("too short", text)
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
                                print("DEBUG111",latest_version)
                            else:
                                raise Exception(latest_version)
                        print("DEBUG",latest_version)
                        if latest_version:
                            version_id = latest_version[1]
                            model = Model(
                                id=latest_version[0],
                                model_version=ModelVersion(
                                    id=version_id,
                                ),
                            )

                            args = dict(
                                model=model,
                            )

                            if prev_node_id is not None:
                                args["node_inputs"] = [NodeInput(node_id=prev_node_id)]

                            node_id = node["id"]
                            args["id"] = node_id
                            prev_node_id = node_id
                            node2 = WorkflowNode(**args)
                            pprint.pprint({"DEBUG_NODE": [i, node, args]})
                            pprint.pprint({"DEBUG_NODE OUT": [i, node2]})
                            workflow_nodes.append(node2)
                        else:
                            print("no verssion!")

            #pprint.pprint({"WORKFLOW": workflow_nodes})
            #created_workflow = self.app.delete_workflow(
            #    workflow_id="RakeItUpV1" + concept
            #)
            try:
                created_workflow = self.app.create_workflow(
                    workflow_id="RakeItUpV3" + concept, nodes=workflow_nodes
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
