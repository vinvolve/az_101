# Retrieve information about the current subscription
data "azurerm_subscription" "primary" {}

# Give Azure Data Factory access to the Storage Account (Data Lake)
resource "azurerm_role_assignment" "adf_to_storage" {
  scope                = azurerm_storage_account.datalake.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azurerm_data_factory.main.identity[0].principal_id
}

# Give Azure Data Factory access to read secrets from Key Vault via Access Policy
resource "azurerm_key_vault_access_policy" "adf_to_kv" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_data_factory.main.identity[0].principal_id

  secret_permissions = [
    "Get",
    "List",
  ]
}
