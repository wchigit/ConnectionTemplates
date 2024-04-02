from typing import List
from payloads.binding import Binding
from payloads.resources.application_insights import ApplicationInsightsResource

from terraform_engines.models.template import Template
from terraform_engines.models.appsetting import AppSetting, AppSettingType
from terraform_engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper
from helpers.abbrevation import Abbreviation



class ApplicationInsightsEngine(TargetResourceEngine):

    ApplicationInsightsComponentContributor = 'ae349356-3a1b-4a5e-921d-050484c6347e'

    def __init__(self, resource: ApplicationInsightsResource) -> None:
        super().__init__(Template.APP_INSIGHTS_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.APPLICATION_INSIGHTS.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.APPLICATION_INSIGHTS.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('application', 'insights', self.resource.name, 'id'), 
                'azurerm_application_insights.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_application_insights.{}.id'.format(self.module_name),
                ApplicationInsightsEngine.ApplicationInsightsComponentContributor)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        return [
            # TODO: use identity connection string
            AppSetting(AppSettingType.KeyValue, 'AZURE_APPINSIGHTS_CONNECTIONSTRING', 
                       'azurerm_application_insights.{}.connection_string'.format(self.module_name)),
        ]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_APPINSIGHTS_CONNECTIONSTRING'

        return [
            AppSetting(AppSettingType.SecretReference, app_setting_key, 
                'azurerm_application_insights.{}.connection_string'.format(self.module_name))
        ]