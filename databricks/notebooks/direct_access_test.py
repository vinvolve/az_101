# Databricks notebook source
# MAGIC %md
# MAGIC # Direct Access Test (No Mounts)
# MAGIC Your workspace has disabled legacy DBFS mounts for security. 
# MAGIC This notebook uses the modern **Direct Access** method with `abfss` paths.

# COMMAND ----------

# 1. Configuration - MAKE SURE THIS MATCHES YOUR SCOPE NAME
storage_account_name = "staz101devvyj1t"
key_vault_scope = "kv-az101-dev-scope"

# 2. Retrieve credentials from Key Vault
client_id = dbutils.secrets.get(scope=key_vault_scope, key="databricks-client-id")
tenant_id = dbutils.secrets.get(scope=key_vault_scope, key="databricks-tenant-id")
client_secret = dbutils.secrets.get(scope=key_vault_scope, key="databricks-client-secret")

# 3. Apply Spark configurations for this session
spark.conf.set(f"fs.azure.account.auth.type.{storage_account_name}.dfs.core.windows.net", "OAuth")
spark.conf.set(f"fs.azure.account.oauth.provider.type.{storage_account_name}.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set(f"fs.azure.account.oauth2.client.id.{storage_account_name}.dfs.core.windows.net", client_id)
spark.conf.set(f"fs.azure.account.oauth2.client.secret.{storage_account_name}.dfs.core.windows.net", client_secret)
spark.conf.set(f"fs.azure.account.oauth2.client.endpoint.{storage_account_name}.dfs.core.windows.net", f"https://login.microsoftonline.com/{tenant_id}/oauth2/token")

# COMMAND ----------

# 4. Test Writing a File
data = [("Bronze", "Raw Data"), ("Silver", "Clean Data"), ("Gold", "Aggregated Data")]
df = spark.createDataFrame(data, ["Layer", "Description"])

test_path = f"abfss://bronze@{storage_account_name}.dfs.core.windows.net/test_connection.csv"

print(f"Attempting to write test file to: {test_path}")
df.write.format("csv").mode("overwrite").option("header", "true").save(test_path)
print("Write Success!")

# COMMAND ----------

# 5. Test Reading the File back
print("Reading file back...")
df_read = spark.read.csv(test_path, header=True)
display(df_read)
