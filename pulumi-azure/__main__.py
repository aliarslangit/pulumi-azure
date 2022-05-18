"""An Azure RM Python Pulumi program"""

import pulumi
import pulumi_azure as azure
from pulumi_azure_native import storage
from pulumi_azure_native import resources

# Create an Azure Resource Group
resource_group = resources.ResourceGroup('cmp-pulumi-rg')

# Create an Azure resource (Storage Account)
account = storage.StorageAccount('pulumistcmp',
                                 resource_group_name=resource_group.name,
                                 sku=storage.SkuArgs(
                                     name=storage.SkuName.STANDARD_LRS,
                                 ),
                                 kind=storage.Kind.STORAGE_V2)

# Create an App Service
app_service = azure.appservice.AppService("exampleAppService",
                                          location=example_resource_group.location,
                                          resource_group_name=example_resource_group.name,
                                          app_service_plan_id=example_plan.id,
                                          site_config=azure.appservice.AppServiceSiteConfigArgs(
                                              dotnet_framework_version="v4.0",
                                              scm_type="LocalGit",
                                          ),
                                          app_settings={
                                              "SOME_KEY": "some-value",
                                          })

# Export the primary key of the Storage Account
primary_key = pulumi.Output.all(resource_group.name, account.name) \
    .apply(lambda args: storage.list_storage_account_keys(
        resource_group_name=args[0],
        account_name=args[1]
    )).apply(lambda accountKeys: accountKeys.keys[0].value)


pulumi.export("primary_storage_key", primary_key)
