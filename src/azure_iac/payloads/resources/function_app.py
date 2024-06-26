from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.compute_resource import ComputeResource


class FunctionAppResource(ComputeResource):
    def __init__(self):
        super().__init__()

        self.type = ResourceType.AZURE_FUNCTION_APP
        self.name = ''
    
    def from_json(json):
        result = FunctionAppResource()
        result.name = json.get('name', '')
        return result