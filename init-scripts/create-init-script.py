# Databricks notebook source
script = '''#!/bin/bash
if [[ $DB_IS_DRIVER = "TRUE" ]]; then
  
  # SET VARIABLES
  WORKSPACE_ID=XXXXXXXXXXXXXXXX
  WORKSPACE_URL=XXXXXXXXXXXX.cloud.databricks.com
  PPM_SNAPSHOT=2024-12-15
  
  RELEASE=$(lsb_release -c --short)

  # install unixodb
  sudo apt-get update
  sudo apt-get install odbcinst1debian2 libsasl2-modules-gssapi-mit -y

  # install simba spark odbc driver
  curl -o \
    /tmp/odbc-driver.zip \
    https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc/2.8.2/SimbaSparkODBC-2.8.2.1013-Debian-64bit.zip

  unzip /tmp/odbc-driver.zip -d /tmp/odbc-simba/
  sudo dpkg -i /tmp/odbc-simba/simbaspark_2.8.2.1013-2_amd64.deb

  # configure odbc
  echo """
[ODBC Data Sources]
databricks=Databricks ODBC Connector

[databricks-self]
Driver          = /opt/simba/spark/lib/64/libsparkodbc_sb64.so
host            = ${WORKSPACE_URL}
port            = 443
SparkServerType = 3
Schema          = default
ThriftTransport = 2
SSL             = 1
AuthMech        = 3
UID             = token
HTTPPath        = sql/protocolv1/o/${WORKSPACE_ID}/${DB_CLUSTER_ID}

[databricks]
Driver          = /opt/simba/spark/lib/64/libsparkodbc_sb64.so
host            = ${WORKSPACE_URL}
port            = 443
SparkServerType = 3
Schema          = default
ThriftTransport = 2
SSL             = 1
AuthMech        = 3
UID             = token

  """ > /etc/odbc.ini

  # configure mlflow
  echo """
MLFLOW_PYTHON_BIN="/databricks/python/bin/python3"
MLFLOW_BIN="/databricks/python3/bin/mlflow"
RETICULATE_PYTHON="/databricks/python3/bin/python3"
  """ >> /etc/R/Renviron.site

  # configure reticulate
  echo "PATH=${PATH}:/databricks/conda/bin" >> /usr/lib/R/etc/Renviron.site
  
  # install mlflow and ODBC as of MRAN snapshot appropriate to DBR
  options(HTTPUserAgent = sprintf('R/%s R (%s)', getRversion(), paste(getRversion(), R.version['platform'], R.version['arch'], R.version['os'])));
  install.packages(c('mlflow', 'odbc'), repos='https://packagemanager.posit.co/cran/__linux__/${RELEASE}/${PPM_SNAPSHOT}/')

  # RStudio connectio pane configs
  mkdir /etc/rstudio/connections
  echo """library(DBI)
con <- dbConnect(
  odbc::databricks(),
  uid = 'databricks-self',
  pwd = \${0:Password/Token=sparkR.conf('USER_TOKEN')}
)
  """ > /etc/rstudio/connections/'ODBC to RStudio Cluster Spark Session.R'

  echo """library(DBI)
con <- dbConnect(
  odbc::databricks(),
  dsn = 'databricks',
  HTTPPath = '\${0:HTTPPath=\"\"}'
  uid = 'token',
  pwd = \${1:Password/Token=sparkR.conf('USER_TOKEN')}
)
  """ >> /etc/rstudio/connections/'Databricks ODBC.R'

fi
'''

dbutils.fs.mkdirs("/databricks/init")
dbutils.fs.put("/databricks/init/r-env-init.sh", script, True)