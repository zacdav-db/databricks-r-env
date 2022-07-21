# Databricks on AWS

**Use an ML LTS Databricks runtime, these come with RStudio already installed which will result in faster cluster start times relative to non-ML LTS**

- `create-init-script`: Notebook which generates an init script (`/databricks/init/r-env-init-aws.sh`). Init script will: 
   - Install Simba Spark ODBC drivers (version: `2.6.19`)
   - Configure `/etc/odbc.ini` 
   - Install `{mlflow}` and `{odbc}` (using same MRAN snaphot as DBR 10.4 ML LTS `2022-02-24`)
   - Add variables to `/etc/R/Renviron.site`:
      - `MLFLOW_PYTHON_BIN="/databricks/python/bin/python3"`
      - `MLFLOW_BIN="/databricks/python3/bin/mlflow"`
      - `RETICULATE_PYTHON="/databricks/python3/bin/python3"`: Use correct python version for interactive python in RStudio via `{reticulate}`
      - `PATH=${PATH}:/databricks/conda/bin`: 
        (`$PATH` injected at start, subsequent edits won't be captured unless changing init script)
- `cluster-policy-rstudio-users.json`: Cluster policy that simplifies creation of clusters using rstudio init script:
   - DBR 10.4 ML LTS (`10.4.x-cpu-ml-scala2.12`) (forced)
   - Auto-termination disabled (forced)  
   - Set `purpose` tag to `rstudio`
   - Policy only works for `all-purpose` clusters, will not work for `job` clusters
  
