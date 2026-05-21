# 1. Create an Application in Azure Entra ID (Azure AD)
resource "azuread_application" "databricks_app" {
  display_name = "sp-databricks-${var.project_name}-${var.environment}"
}

# 2. Create a Service Principal for the Application
resource "azuread_service_principal" "databricks_sp" {
  client_id = azuread_application.databricks_app.client_id
}

# 3. Create a Client Secret for the Service Principal
resource "azuread_service_principal_password" "databricks_sp_pwd" {
  service_principal_id = azuread_service_principal.databricks_sp.object_id
}

# 4. Give the Service Principal access to the Storage Account
resource "azurerm_role_assignment" "databricks_to_storage" {
  scope                = azurerm_storage_account.datalake.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = azuread_service_principal.databricks_sp.object_id
}

# 5. Store the Client ID in Key Vault
resource "azurerm_key_vault_secret" "db_client_id" {
  name         = "databricks-client-id"
  value        = azuread_application.databricks_app.client_id
  key_vault_id = azurerm_key_vault.main.id
}

# 6. Store the Client Secret in Key Vault
resource "azurerm_key_vault_secret" "db_client_secret" {
  name         = "databricks-client-secret"
  value        = azuread_service_principal_password.databricks_sp_pwd.value
  key_vault_id = azurerm_key_vault.main.id
}

# 7. Store the Tenant ID in Key Vault
resource "azurerm_key_vault_secret" "db_tenant_id" {
  name         = "databricks-tenant-id"
  value        = data.azurerm_client_config.current.tenant_id
  key_vault_id = azurerm_key_vault.main.id
}
