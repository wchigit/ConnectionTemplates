from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.storage_account import StorageAccountResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation



class StorageAccountEngine(TargetResourceEngine):

    StorageDataReaderAccessRole = 'Reader and Data Access'

    def __init__(self, resource: StorageAccountResource) -> None:
        super().__init__(Template.STORAGE_ACCOUNT_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.STORAGE_ACCOUNT.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.STORAGE_ACCOUNT.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('storage', 'account', self.resource.name, 'id'), 
                'azurerm_storage_account.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_storage_account.{}.id'.format(self.module_name),
                StorageAccountEngine.StorageDataReaderAccessRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyValue, 'AZURE_STORAGEACCOUNT_BLOBENDPOINT', 'azurerm_storage_account.{}.primary_blob_endpoint'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_STORAGEACCOUNT_TABLEENDPOINT', 'azurerm_storage_account.{}.primary_table_endpoint'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_STORAGEACCOUNT_QUEUEENDPOINT', 'azurerm_storage_account.{}.primary_queue_endpoint'.format(self.module_name)),
            (AppSettingType.KeyValue, 'AZURE_STORAGEACCOUNT_FILEENDPOINT', 'azurerm_storage_account.{}.primary_file_endpoint'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', 'azurerm_storage_account.{}.primary_access_key'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
