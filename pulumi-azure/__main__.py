"""An Azure RM Python Pulumi program"""

import resource
import pulumi
from pulumi_azure_native import storage
from pulumi_azure_native import resources, network
import pulumi_azure_native as azure_native
#import pulumi_azure as azure


# Create an Azure Resource Group
resource_group = resources.ResourceGroup('demo-pulumi-rg')

# create ACR
acr = azure_native.containerregistry.Registry("registry",
                                              admin_user_enabled=True,
                                              location=resource_group.location,
                                              registry_name="myRegistryforcmppulumi",
                                              resource_group_name=resource_group.name,
                                              sku=azure_native.containerregistry.SkuArgs(
                                                  name="Standard",
                                              ),
                                              tags={
                                                  "key": "value",
                                              })

# create MySQL
mysqlserver = azure_native.dbformysql.Server("server",
                                             location=resource_group.location,
                                             properties={
                                                 "administratorLogin": "cloudsa",
                                                 "administratorLoginPassword": "<administratorLoginPassword>",
                                                 "createMode": "Default",
                                                 "sslEnforcement": azure_native.dbformysql.SslEnforcementEnum.ENABLED,
                                                 "storageProfile": azure_native.dbformysql.StorageProfileArgs(
                                                     backup_retention_days=7,
                                                     geo_redundant_backup="Enabled",
                                                     storage_mb=128000,
                                                 ),
                                             },
                                             resource_group_name=resource_group.name,
                                             server_name="mysqltestsvc4",
                                             sku=azure_native.dbformysql.SkuArgs(
                                                 capacity=2,
                                                 family="Gen5",
                                                 name="GP_Gen5_2",
                                                 tier="GeneralPurpose",
                                             ),
                                             tags={
                                                 "ElasticServer": "1",
                                             })
database = azure_native.dbformysql.Database("database",
                                            charset="utf8",
                                            collation="utf8_general_ci",
                                            database_name="db1",
                                            resource_group_name=resource_group.name,
                                            server_name="testserver")

# prefix = "demo"
# # Create a VNET
# vnet = network.VirtualNetwork(
#     f"{prefix}-vnet",
#     location="East US",
#     resource_group_name="demo-pulumi-rg",
#     address_space={
#         "address_prefixes": ["10.0.0.0/16"],
#     }
# )
# # Create a Subnet
# subnet = network.Subnet(
#     "dev-subnet",
#     resource_group_name="demo-pulumi-rg",
#     address_prefix="10.0.0.0/24",
#     virtual_network_name=vnet.name
# )


# # # Create a Loadbalancer

# example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
#                                               location="East US",
#                                               resource_group_name="demo-pulumi-rg",
#                                               frontend_ip_configurations=[azure.lb.LoadBalancerFrontendIpConfigurationArgs(
#                                                   name="PublicIPAddress",
#                                                   public_ip_address_id=example_public_ip.id,
#                                               )])

# # # Create a Public IP
# example_public_ip = azure.network.PublicIp("examplePublicIp",
#                                            location="East US",
#                                            resource_group_name="demo-pulumi-rg",
#                                            allocation_method="Static")
# # Create an Azure resource (Storage Account)
# account = storage.StorageAccount('pulumistdemo',
#                                  resource_group_name=resource_group.name,
#                                  sku=storage.SkuArgs(
#                                      name=storage.SkuName.STANDARD_LRS,
#                                  ),
#                                  kind=storage.Kind.STORAGE_V2)

# # Create an App Service Plan
# app_service_plan = azure_native.web.AppServicePlan("appServicePlan",
#                                                    kind="app",
#                                                    location="East US",
#                                                    name="testsf6141",
#                                                    resource_group_name="testrg123",
#                                                    sku=azure_native.web.SkuDescriptionArgs(
#                                                        capacity=1,
#                                                        family="P",
#                                                        name="P1",
#                                                        size="P1",
#                                                        tier="Premium",
#                                                    ))

# # # Create an App Servie
# # app_service = azure_native.web.WebApp(
# #     "demoappfordemo", location="East US", server_farm_id=pulumi.export("id", id))


# # Export the primary key of the Storage Account
# primary_key = pulumi.Output.all(resource_group.name, account.name) \
#     .apply(lambda args: storage.list_storage_account_keys(
#         resource_group_name=args[0],
#         account_name=args[1]
#     )).apply(lambda accountKeys: accountKeys.keys[0].value)


# pulumi.export("primary_storage_key", primary_key)
