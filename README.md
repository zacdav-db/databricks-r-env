# R Environment Setup on Databricks

Notes and artifacts (notebooks, templates, etc) to assist with establishing R/RStudio workloads on Databricks.

## AWS
- Cluster policy
- Init Script

## Azure
- Cluster policy
- Init Script

## GCP
- Cluster policy
- Init Script
  - **RStudio is not currently supported**

---

### Using ODBC
Once the init script has run you can use ODBC drivers with the dsn `databricks`.
Below is an example of connecting to a SQL warehouse.

```r
conn <- dbConnect(
  odbc::odbc(),
  dsn             = "databricks",
  host            = "XXXXXXXX.cloud.databricks.com",
  port            = "443",
  ThriftTransport = 2,
  SSL             = 1,
  AuthMech        = 3,
  UID             = "token",
  PWD             = "dapiXXXXXXXXXXXXX",
  HTTPPath        = "/sql/1.0/endpoints/XXXXXXXXXX"
)
```
