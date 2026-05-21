# Databricks notebook source
# MAGIC %md
# MAGIC # Mount ADLS Gen2 Storage using Service Principal
# MAGIC This notebook mounts the Bronze, Silver, and Gold containers to DBFS using the Service Principal credentials stored in Azure Key Vault.

# COMMAND ----------

# 1. Define configuration variables
storage_account_name = "staz101devvyj1t"
key_vault_scope = "kv-az101-dev-scope" # We will create this scope in the Databricks UI

# 2. Retrieve secrets from Key Vault (via Databricks Secret Scope)
client_id = dbutils.secrets.get(scope=key_vault_scope, key="databricks-client-id")
tenant_id = dbutils.secrets.get(scope=key_vault_scope, key="databricks-tenant-id")
client_secret = dbutils.secrets.get(scope=key_vault_scope, key="databricks-client-secret")

# 3. Define Spark configurations for the OAuth connection
configs = {
  "fs.azure.account.auth.type": "OAuth",
  "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
  "fs.azure.account.oauth2.client.id": client_id,
  "fs.azure.account.oauth2.client.secret": client_secret,
  "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

# COMMAND ----------

# 4. Function to mount a container
def mount_adls(container_name):
  dbfs_mount_point = f"/mnt/{container_name}"
  adls_uri = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/"
  
  # Check if it's already mounted
  if any(mount.mountPoint == dbfs_mount_point for mount in dbutils.fs.mounts()):
    print(f"Directory {dbfs_mount_point} is already mounted.")
  else:
    print(f"Mounting {container_name} to {dbfs_mount_point}...")
    dbutils.fs.mount(
      source = adls_uri,
      mount_point = dbfs_mount_point,
      extra_configs = configs
    )
    print("Success!")

# COMMAND ----------

# 5. Execute the mounts
mount_adls("bronze")
mount_adls("silver")
mount_adls("gold")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Verify Mounts
# MAGIC Let's check if we can list the contents of the bronze container.

# COMMAND ----------

display(dbutils.fs.ls("/mnt/bronze"))
