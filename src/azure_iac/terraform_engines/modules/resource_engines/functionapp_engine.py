from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.function_app import FunctionAppResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.appserviceplan_engine import AppServicePlanEngine
from azure_iac.terraform_engines.modules.resource_engines.functionstorageengine import FunctionStorageEngine
from azure_iac.terraform_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class FunctionAppEngine(SourceResourceEngine, TargetResourceEngine):
    # use linux web app as default
    def __init__(self, resource: FunctionAppResource) -> None:
        SourceResourceEngine.__init__(self, Template.FUNCTION_APP_LINUX_TF.value)
        TargetResourceEngine.__init__(self, Template.FUNCTION_APP_LINUX_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.FUNCTION_APP.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.FUNCTION_APP.value) + '${var.resource_suffix}'
        self.module_var_principal_id_name = 'azurerm_linux_function_app.{}.identity[0].principal_id'.format(self.module_name)
        self.module_var_outbound_ip_name = 'azurerm_linux_function_app.{}.possible_outbound_ip_address_list'.format(self.module_name)

        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('function', 'app', self.resource.name, 'id'), 
             'azurerm_linux_function_app.{}.id'.format(self.module_name))
        ]

        # dependency engines
        self.depend_engines = [
            AppServicePlanEngine(self.resource),
            FunctionStorageEngine(StorageAccountResource()),
            ApplicationInsightsEngine(ApplicationInsightsResource())
        ]
    
    def get_app_settings_http(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'SERVICE{}_URL'.format(self.resource.name.upper())
        
        return [
            AppSetting(AppSettingType.KeyValue, app_setting_key,
                'azurerm_linux_function_app.{}.default_hostname'.format(self.module_name))
        ]
    
    
    