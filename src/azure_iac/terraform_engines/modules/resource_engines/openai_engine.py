from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.openai import OpenAIResource

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


# TODO: firewall engine not supported yet
class OpenAIEngine(TargetResourceEngine):

    OpenAIContributorRole = 'Cognitive Services OpenAI Contributor'

    def __init__(self, resource: OpenAIResource) -> None:
        super().__init__(Template.OPENAI_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.OPENAI.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.OPENAI.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('openai', 'account', self.resource.name, 'id'), 
                'azurerm_cognitive_account.{}.id'.format(self.module_name)),
			(string_helper.format_snake('openai', 'deployment', self.resource.name, 'id'),
				'azurerm_cognitive_deployment.{}.id'.format(self.module_name)),
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_cognitive_account.{}.id'.format(self.module_name),
                OpenAIEngine.OpenAIContributorRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        
        # TODO: TF does not support other endpoints for now, so we just concatenate the name
        name = 'azurerm_cognitive_account.{}.name'.format(self.module_name) 
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_OPENAI_BASE', '"https://${' + name + '}.openai.azure.com/"'),
            (AppSettingType.KeyValue, 'AZURE_OPENAI_DEPLOYMENT', 'azurerm_cognitive_deployment.{}.name'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        
        # TODO: TF does not support other endpoints for now, so we just concatenate the name
        name = 'azurerm_cognitive_account.{}.name'.format(self.module_name) 
        deafult_settings = [
            (AppSettingType.KeyValue, 'AZURE_OPENAI_BASE', '"https://${' + name + '}.openai.azure.com/"'),
            (AppSettingType.KeyValue, 'AZURE_OPENAI_DEPLOYMENT', 'azurerm_cognitive_deployment.{}.name'.format(self.module_name)),
            (AppSettingType.SecretReference, 'AZURE_OPENAI_KEY', 'azurerm_cognitive_account.{}.primary_access_key'.format(self.module_name)),
        ]

        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in deafult_settings]