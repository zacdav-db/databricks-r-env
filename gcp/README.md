# Databricks on GCP

- `create-init-script`: notebook which generates an init script (`/databricks/init/r-env-init-gcp.sh`). Init script will: 
   - Install Simba Spark ODBC drivers (version: `2.6.19`)
   - ~~Install RStudio Server (version: `rstudio-2022.02.0-daily-335-amd64`)~~  
     *This feature is unavailable on Databricks on Google Cloud as of this release.*

  
