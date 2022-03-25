# Databricks notebook source
script = '''#!/bin/bash

set -euxo pipefail
RSTUDIO_BIN="/usr/sbin/rstudio-server"

if [[ ! -f "$RSTUDIO_BIN" && $DB_IS_DRIVER = "TRUE" ]]; then
  apt-get update
  apt-get install -y gdebi-core
  cd /tmp
  # You can find new releases at https://rstudio.com/products/rstudio/download-server/debian-ubuntu/.
  wget https://s3.amazonaws.com/rstudio-ide-build/desktop/bionic/amd64/rstudio-2022.02.0-daily-335-amd64.deb -O rstudio-server.deb
  sudo gdebi -n rstudio-server.deb
  rstudio-server restart || true
fi

ln -s /usr/lib/jvm/java-8-openjdk-amd64 /usr/lib/jvm/default-java
R CMD javareconf

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

dbutils.fs.mkdirs("/Users/zachary.davies@databricks.com/init")
dbutils.fs.put("/Users/zachary.davies@databricks.com/init/r-demo-init.sh", script, True)
