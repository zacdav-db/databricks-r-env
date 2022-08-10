# R & RStudio Environment Setup on Databricks

Artifacts to assist with establishing R/RStudio workloads on Databricks.

# Init Script
In `/init-scripts` there is currently one notebook which configures & installs:
- Simba Spark ODBC driver (`2.6.19`)
- Simba Spark JDBC driver ()
- `{mlflow}` and `{odbc}` (MRAN snapshot `2022-02-24`)
- ODBC data sources:
  - `databricks-self`: Existing cluster (self)
  - `databricks`: Any databricks endpoint/cluster
- RStudio Connection Snippets

>*RStudio is not installed as part of the init script as it is pre-installed with the ML variant of the Databricks Runtime (DBR). It is recommended that you use the ML runtime (prefereably LTS) in order to reduce cluster start times.*

# Cluster Policies
In `/cluster-policies` there are 

- `cluster-policy-rstudio-users.json`: Cluster policy that simplifies creation of clusters using rstudio init script:
   - DBR 10.4 ML LTS (`10.4.x-cpu-ml-scala2.12`) (forced)
   - Auto-termination disabled (forced)  
   - Set `purpose` tag to `rstudio`
   - Policy only works for `all-purpose` clusters, will not work for `job` clusters
  

# Connecting to ODBC/JDBC

## ODBC
The init script will configure two ODBC data sources:
1. `databricks-self`: Existing cluster (self)
2. `databricks`: Any databricks endpoint/cluster

These will be available within the [RStudio connections pane](https://db.rstudio.com/tooling/connections/) with preconfigured code snippets.

### **Connection Examples**

`PWD` arg is expected to be a [Databricks Personal Access Token](https://docs.databricks.com/dev-tools/api/latest/authentication.html)

```r
# connecting via ODBC to a SQL Endpoint
library(DBI)
conn <- dbConnect(
  odbc::odbc(),
  dsn      = "databricks",
  HTTPPath = "/sql/1.0/endpoints/XXXXXXXXXX",
  PWD      = "dapiXXXXXXXXXXXXX"
)
```

```r
# connecting via ODBC to the same cluster that RStudio is running on
library(DBI)
conn <- dbConnect(
  odbc::odbc(),
  dsn = "databricks-self",
  PWD = "dapiXXXXXXXXXXXXX"
)
```

It's recommended to not store tokens or passwords in plain text. Databricks recommends the use of [secret scopes](https://docs.databricks.com/security/secrets/secret-scopes.html) which can be set and accessed through Spark configs on the Datbaricks cluster ([docs](https://docs.databricks.com/security/secrets/secrets.html#syntax-for-referencing-secrets-in-a-spark-configuration-property-or-environment-variable)).

This would enable the following:
```r
library(DBI)
# set `spark.<property-name> {{secrets/<scope-name>/<secret-name>}}` on cluster
conn <- dbConnect(
  odbc::odbc(),
  dsn = "databricks-self",
  PWD = sparkR.conf("<property-name>")
)
```

## JDBC
TODO

# Advanced
TODO

## Changing Simba Drivers
TODO

## Updating MRAN Snapshot
TODO

## Configuring mlflow
TODO

## Configuring Reticulate
TODO

## Configuring RStudio  
Despite the ML runtime including RStudio there may be cases where a different version is required, or Server Pro/Workbench is prefered. Documentation for these processes is found [here](https://docs.databricks.com/spark/latest/sparkr/rstudio.html).


- Install Simba Spark ODBC drivers (version: `2.6.19`)
- Configure `/etc/odbc.ini` 
- Install `{mlflow}` and `{odbc}` (using same MRAN snaphot as DBR 10.4 ML LTS `2022-02-24`)
- Add variables to `/etc/R/Renviron.site`:
  - `MLFLOW_PYTHON_BIN="/databricks/python/bin/python3"`
  - `MLFLOW_BIN="/databricks/python3/bin/mlflow"`
  - `RETICULATE_PYTHON="/databricks/python3/bin/python3"`: Use correct python version for interactive python in RStudio via `{reticulate}`
  - `PATH=${PATH}:/databricks/conda/bin`: 
    (`$PATH` injected at start, subsequent edits won't be captured unless changing init script)



