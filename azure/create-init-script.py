# Databricks notebook source
script = '''#!/bin/bash
# install RStudio server
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

# install unixodb
sudo apt-get update
sudo apt-get install unixodbc -y

# install simba spark odbc driver
curl -o \
  /tmp/odbc-driver.zip \
  https://databricks-bi-artifacts.s3.us-east-2.amazonaws.com/simbaspark-drivers/odbc/2.6.19/SimbaSparkODBC-2.6.19.1033-Debian-64bit.zip

unzip /tmp/odbc-driver.zip -d /tmp/odbc-simba/
sudo apt-get install libsasl2-modules-gssapi-mit -y
sudo dpkg -i /tmp/odbc-simba/simbaspark_2.6.19.1033-2_amd64.deb

# configure odbc
echo """
[ODBC Data Sources]
Databricks=Databricks ODBC Connector
[Databricks]
Driver=/opt/simba/sparkodbc/lib/64/libsparkodbc_sb64.so
""" > /etc/odbc.ini

# install mlflow and ODBC as of MRAN snapshot appropriate to the 10.4 LTS DBR 
Rscript -e 'install.packages(c("mlflow", "odbc"), repos="https://cran.microsoft.com/snapshot/2022-02-24/")'

# configure mlflow
echo """
MLFLOW_PYTHON_BIN="/databricks/python/bin/python3"
MLFLOW_BIN="/databricks/python3/bin/mlflow"
RETICULATE_PYTHON="/databricks/python3/bin/python3"
""" >> /etc/R/Renviron.site

# configure reticulate
echo "PATH=${PATH}:/databricks/conda/bin" >> /usr/lib/R/etc/Renviron.site

'''

dbutils.fs.mkdirs("/databricks/init")
dbutils.fs.put("/databricks/init/r-env-init-azure.sh", script, True)

# COMMAND ----------

# MAGIC %fs head /databricks/init/r-env-init-azure.sh

# COMMAND ----------


