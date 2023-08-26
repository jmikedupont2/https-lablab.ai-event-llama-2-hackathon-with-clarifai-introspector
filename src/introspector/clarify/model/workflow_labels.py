
class FlattenedLabelWorkflowGenerator:

    def generate_workflows(self, concepts, labelling_model_id):
        workflows = {}

        # Create a workflow for each concept
        for concept in concepts:
            workflow = self._create_workflow_for_concept(concept, labelling_model_id)
            workflows[concept] = workflow

        return workflows

    def _create_workflow_for_concept(self, concept, labelling_model_id):
        # Define the workflow nodes
        nodes = []

        # Create input task
        input_task = {
            "name": f"Input Task for {concept}",
            "model": {"id": "text-embedding"},
            "inputs": {"unassigned": {"concepts": [{"id": "unassigned"}]}}
        }
        nodes.append(input_task)

        # Create a labeller task for the concept
        labeller_task = {
            "name": f"Labeller for {concept}",
            "model": {"id": labelling_model_id},  # Replace with the actual labelling model ID
            "inputs": {"from_node": f"Input Task for {concept}"}
        }
        nodes.append(labeller_task)

        # Create an output task for the labeller
        output_task = {
            "name": f"Output to {concept}",
            "model": None,
            "inputs": {"from_node": f"Labeller for {concept}"}
        }
        nodes.append(output_task)

        # Create the workflow
        workflow_definition = {
            "nodes": nodes,
            "workflow_output": {"id": output_task}
        }

        return workflow_definition

if __name__=="__main__":
    concepts = ["business", "tech"]
    workflow_generator = FlattenedLabelWorkflowGenerator()
    workflows = workflow_generator.generate_workflows(concepts,labelling_model_id="FooBar")
    print(workflows)
