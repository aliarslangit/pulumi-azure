"""An Azure RM Python Pulumi program"""

import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources
import pulumi_azure_native as azure_native

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('cmp-pulumi-rg')

# Create an Azure resource (Storage Account)
account = storage.StorageAccount('pulumistcmp',
                                 resource_group_name=resource_group.name,
                                 sku=storage.SkuArgs(
                                     name=storage.SkuName.STANDARD_LRS,
                                 ),
                                 kind=storage.Kind.STORAGE_V2)

# Create an App Service Plan
app_service_plan = azure_native.web.AppServicePlan("appServicePlan",
                                                   kind="app",
                                                   location="East US",
                                                   name="testsf6141",
                                                   resource_group_name="testrg123",
                                                   sku=azure_native.web.SkuDescriptionArgs(
                                                       capacity=1,
                                                       family="P",
                                                       name="P1",
                                                       size="P1",
                                                       tier="Premium",
                                                   ))

# Create an App Servie
app_service = azure_native.web.WebApp(
    "demoappforcmp", location="East US", server_farm_id=pulumi.export("id", id))
# Export the primary key of the Storage Account
primary_key = pulumi.Output.all(resource_group.name, account.name) \
    .apply(lambda args: storage.list_storage_account_keys(
        resource_group_name=args[0],
        account_name=args[1]
    )).apply(lambda accountKeys: accountKeys.keys[0].value)


pulumi.export("primary_storage_key", primary_key)
