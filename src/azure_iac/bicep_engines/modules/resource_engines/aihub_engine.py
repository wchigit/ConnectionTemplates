from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.aihub import AIHubResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.bicep_engines.modules.resource_engines.containerregistry_engine import ContainerRegistryEngine
from azure_iac.bicep_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine
from azure_iac.bicep_engines.modules.resource_engines.keyvault_engine import KeyVaultEngine
from azure_iac.bicep_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class AIHubEngine(SourceResourceEngine, TargetResourceEngine):
    
    STORAGE_DEPENDENCY_NAME = "hubdep"        

    def __init__(self, resource: AIHubResource) -> None:
        SourceResourceEngine.__init__(self,
                                      Template.AI_HUB_BICEP.value,
                                      Template.AI_HUB_MODULE.value)
        TargetResourceEngine.__init__(self,
                                      Template.AI_HUB_BICEP.value,
                                      Template.AI_HUB_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('aiHub', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('ai-hub', self.resource.name)
        self.module_params_name = string_helper.format_camel('aiHub', self.resource.name, "Name")

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.APP_SERVICE.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('aiHub', self.resource.name, "Id"),
             'string', '{}.outputs.id'.format(self.module_name))]

        # dependency engines
        self.depend_engines = [
            ContainerRegistryEngine(self.resource),
            ApplicationInsightsEngine(self.resource),
            StorageAccountEngine(StorageAccountResource(AIHubEngine.STORAGE_DEPENDENCY_NAME)),
            KeyVaultEngine(self.resource)
        ]

    def assign_role(self, principal_id: str) -> None:
        return super().assign_role(principal_id)
