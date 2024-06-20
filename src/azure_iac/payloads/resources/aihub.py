from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.base_resource import BaseResource


class AIHubResource(BaseResource):
    def __init__(self):
        self.type = ResourceType.AZURE_AI_HUB
        self.name = ''
    
    def from_json(json):
        result = AIHubResource()
        result.name = json.get('name', '')
        return result