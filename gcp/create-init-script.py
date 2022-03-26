# Databricks notebook source
script = '''#!/bin/bash

set -euxo pipefail

sudo apt-get update
sudo apt-get install unixodbc -y

curl -o \
  /dbfs/tmp/odbc-driver.zip \
  https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc/2.6.19/SimbaSparkODBC-2.6.19.1033-Debian-64bit.zip
  
mv /dbfs/tmp/odbc-driver.zip /tmp/
unzip /tmp/odbc-driver.zip -d /tmp/odbc-simba/
sudo apt-get install libsasl2-modules-gssapi-mit -y
sudo dpkg -i /tmp/odbc-simba/simbaspark_2.6.19.1033-2_amd64.deb

echo """
[ODBC Data Sources]
Databricks=Databricks ODBC Connector
[Databricks]
Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so
""" > /etc/odbc.ini

'''

dbutils.fs.mkdirs("/databricks/init")
dbutils.fs.put("/databricks/init/r-env-init-gcp.sh", script, True)

# COMMAND ----------

# MAGIC %fs head /databricks/init/r-env-init-gcp.sh

# COMMAND ----------


