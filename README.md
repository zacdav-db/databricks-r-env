# R & RStudio Environment Setup on Databricks

Artifacts to assist with establishing R/RStudio workloads on Databricks.

# Init Script

In `/init-scripts` there is currently one notebook which configures & installs:
- Simba Spark ODBC driver (`2.8.2.1013`)
- `{mlflow}` and `{odbc}` (Posit Package Manager snapshot `2024-12-15`)
- ODBC data sources:
  - `databricks-self`: Existing cluster (self)
  - `databricks`: Any databricks endpoint/cluster
- RStudio Connection Snippets

>*[RStudio on Databricks Clusters is no longer recommended](https://docs.databricks.com/en/sparkr/rstudio.html#connect-to-a-databricks-hosted-rstudio-server)*


>*RStudio is not installed as part of the init script as it is pre-installed with the ML variant of the Databricks Runtime (DBR). It is recommended that you use the ML runtime (prefereably LTS) in order to reduce cluster start times.*

To ensure ODBC connections work seamlessly its recommended to update the init script. The start of the script includes the following:

```sh
# SET VARIABLES
WORKSPACE_ID=<Workspace ID>
WORKSPACE_URL=<Workspace URL>
PPM_SNAPSHOT=<MRAN Snapshot Date>
```

This should look something like...
```sh
# SET VARIABLES
WORKSPACE_ID=123123123123123
WORKSPACE_URL=XXXXXXXXXX.cloud.databricks.com
PPM_SNAPSHOT=2022-02-24
```
`WORKSPACE_ID` can be derived via the workspace URL (after `?o=`) or by asking your Databricks account admin.
`MRAN_SNAPSHOT` is found via DBR release notes, see [below](#installing-packages-using-mran-snapshot).

# Cluster Policies
In `/cluster-policies` there are:

- `rstudio-generic.json`:
   - DBR 15.4 ML LTS (`15.4.x-cpu-ml-scala2.12`) (forced)
   - Auto-termination disabled (forced)  
   - Set `purpose` tag to `rstudio` (forced)
   - Set `init_scripts` to include init script `dbfs:/databricks/init/r-env-init.sh` (forced)
   - Policy only works for `all-purpose` clusters, will not work for job clusters
  
- `rstudio-single-node.json`:
   - Extends `rstudio-generic.json` as baseline
   - Sets cluster to `SingleNode` mode

For further information on configuring cluster policies see the [docs](https://docs.databricks.com/administration-guide/clusters/policies.html).

# Connecting to ODBC/JDBC

## ODBC
The init script will configure two ODBC data sources:
1. `databricks-self`: Existing cluster (self)
2. `databricks`: Any databricks endpoint/cluster

These will be available within the [RStudio connections pane](https://db.rstudio.com/tooling/connections/) with preconfigured code snippets.

### **Connection Examples**

`pwd` is expected to be a [Databricks Personal Access Token](https://docs.databricks.com/dev-tools/api/latest/authentication.html).  
`HTTPPath` is provided in the cluster/endpoint UI under ODBC settings ([docs](https://docs.databricks.com/integrations/bi/jdbc-odbc-bi.html#retrieve-the-connection-details)).

```r
# connecting via ODBC to a SQL Endpoint
library(DBI)
conn <- dbConnect(
  odbc::odbc(),
  dsn      = "databricks",
  HTTPPath = "/sql/1.0/endpoints/XXXXXXXXXX",
  pwd      = "dapiXXXXXXXXXXXXX"
)
```

```r
# connecting via ODBC to the same cluster that RStudio is running on
library(DBI)
conn <- dbConnect(
  odbc::odbc(),
  dsn = "databricks-self",
  pwd = "dapiXXXXXXXXXXXXX"
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

# Advanced

## Updating Simba Drivers
Download URL and instructions for using Simba drivers:
- [ODBC (64-BIT)](https://www.databricks.com/spark/odbc-drivers-archive)
- [JDBC](https://www.databricks.com/spark/jdbc-drivers-archive)

To get the URL you will need to `'Copy Link Address'` on the download button, this can then replace line 18 in the init script.

It's possible that the way the driver structures its contents may change with newer/older versions, this would then impact the ODBC configuration.

Therefore in the snippet below, the `Driver` path may require updating.
```
[databricks-self]
Driver = /opt/simba/spark/lib/64/libsparkodbc_sb64.so
```
## Installing Packages Using Posit Package Manager Snapshot
It's recommended to use the PPM snapshot as the Databricks Runtime being used. This is disclosed in the DBR release notes ([example](https://docs.databricks.com/release-notes/runtime/11.0.html#installed-r-libraries)).

It's also possible to use the [wizard](https://packagemanager.posit.co/client/#/repos/cran/setup?snapshot=2024-12-15) to choose a desired snapshot.

## Configuring mlflow
Add these variables to `/etc/R/Renviron.site`:
- `MLFLOW_PYTHON_BIN="/databricks/python/bin/python3"`
- `MLFLOW_BIN="/databricks/python3/bin/mlflow"`

## Configuring `{reticulate}`
- `/etc/R/Renviron.site` needs to be configured with `RETICULATE_PYTHON` variable.
  - This can be changed as neccessary, this is set to `/databricks/python3/bin/python3`.
- `/usr/lib/R/etc/Renviron.site` is adjusted to update `PATH` with the following `PATH=${PATH}:/databricks/conda/bin`

## Configuring RStudio  
>*[RStudio on Databricks Clusters is no longer recommended](https://docs.databricks.com/en/sparkr/rstudio.html#connect-to-a-databricks-hosted-rstudio-server)*

Despite the ML runtime including RStudio there may be cases where a different version is required, or Server Pro/Workbench is prefered. Documentation for these processes is found [here](https://docs.databricks.com/spark/latest/sparkr/rstudio.html).



