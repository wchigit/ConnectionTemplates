from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.service_bus import ServiceBusResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ServiceBusEngine(TargetResourceEngine):

    def __init__(self, resource: ServiceBusResource) -> None:
        super().__init__(Template.SERVICE_BUS_BICEP.value,
                         Template.SERVICE_BUS_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('serviceBus', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('servicebus', self.resource.name)
        self.module_params_name = string_helper.format_camel('serviceBus', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('servicebus', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.SERVICE_BUS.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('serviceBus', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyValue, 'AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE', '{}.outputs.endpoint'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyVaultReference, 'AZURE_SERVICEBUS_CONNECTIONSTRING', '{}.outputs.keyVaultSecretUri'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
