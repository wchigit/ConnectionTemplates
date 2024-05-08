from azure_iac.payloads.models.resource_type import ResourceType

from azure_iac.terraform_engines.modules.resource_engines.appservice_engine import AppServiceEngine
from azure_iac.terraform_engines.modules.resource_engines.containerapp_engine import ContainerAppEngine
from azure_iac.terraform_engines.modules.resource_engines.functionapp_engine import FunctionAppEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_firewall_engine import StorageAccountFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.applicationinsights_engine import ApplicationInsightsEngine
from azure_iac.terraform_engines.modules.resource_engines.botservice_engine import BotServiceEngine
from azure_iac.terraform_engines.modules.resource_engines.containerapp_engine import ContainerAppEngine
from azure_iac.terraform_engines.modules.resource_engines.cosmosdb_engine import CosmosDbEngine
from azure_iac.terraform_engines.modules.resource_engines.keyvault_engine import KeyVaultEngine
from azure_iac.terraform_engines.modules.resource_engines.keyvaultsecret_engine import KeyVaultSecretEngine
from azure_iac.terraform_engines.modules.resource_engines.role_resource_engine import RoleResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_engine import StorageAccountEngine
from azure_iac.terraform_engines.modules.resource_engines.storageaccount_firewall_engine import StorageAccountFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.staticwebapp_engine import StaticWebAppEngine
from azure_iac.terraform_engines.modules.resource_engines.servicebus_engine import ServiceBusEngine
from azure_iac.terraform_engines.modules.resource_engines.servicebus_network_engine import ServiceBusNetworkEngine
from azure_iac.terraform_engines.modules.resource_engines.mysql_engine import MySqlDbEngine
from azure_iac.terraform_engines.modules.resource_engines.mysql_firewall_engine import MySqlDbFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.postgresql_engine import PostgreSqlDbEngine
from azure_iac.terraform_engines.modules.resource_engines.postgresql_firewall_engine import PostgreSqlDbFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.sql_engine import SqlDbEngine
from azure_iac.terraform_engines.modules.resource_engines.sql_firewall_engine import SqlDbFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.redis_engine import RedisEngine
from azure_iac.terraform_engines.modules.resource_engines.redis_firewall_engine import RedisFirewallEngine
from azure_iac.terraform_engines.modules.resource_engines.openai_engine import OpenAIEngine
from azure_iac.terraform_engines.modules.resource_engines.webpubsub_engine import WebPubSubEngine


RESOURCE_ENGINES = {
	ResourceType.AZURE_APP_SERVICE: AppServiceEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppEngine,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountEngine,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsEngine,
    ResourceType.AZURE_BOT_SERVICE: BotServiceEngine,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppEngine,
    ResourceType.AZURE_COSMOS_DB: CosmosDbEngine,
    ResourceType.AZURE_KEYVAULT: KeyVaultEngine,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountEngine,
    ResourceType.AZURE_STATIC_WEB_APP: StaticWebAppEngine,
    ResourceType.AZURE_SERVICE_BUS: ServiceBusEngine,
    ResourceType.AZURE_MYSQL_DB: MySqlDbEngine,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbEngine,
    ResourceType.AZURE_SQL_DB: SqlDbEngine,
    ResourceType.AZURE_REDIS_CACHE: RedisEngine,
    ResourceType.AZURE_OPENAI: OpenAIEngine,
    ResourceType.AZURE_WEBPUBSUB: WebPubSubEngine,
}

FIREWALL_ENGINES = {
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountFirewallEngine,
    ResourceType.AZURE_SERVICE_BUS: ServiceBusNetworkEngine,
    ResourceType.AZURE_MYSQL_DB: MySqlDbFirewallEngine,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbFirewallEngine,
    ResourceType.AZURE_SQL_DB: SqlDbFirewallEngine,
    ResourceType.AZURE_REDIS_CACHE: RedisFirewallEngine,
}

def get_resource_engine_from_type(resource_type: ResourceType):
    return RESOURCE_ENGINES[resource_type]

def get_firewall_engine_from_type(resource_type: ResourceType):
    return FIREWALL_ENGINES.get(resource_type)

def get_role_engine():
    return RoleResourceEngine

def get_key_vault_secret_engine():
	return KeyVaultSecretEngine
