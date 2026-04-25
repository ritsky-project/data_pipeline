#!/bin/bash

##############################################################################
########################## DATA ENGINEERING SETUP ############################
##############################################################################

# Fetch the Official Docker Compose File
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml'

# Create Required Directories
mkdir ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

# Initialize Airflow
docker compose up airflow-init

#  Start Airflow
docker compose up -d

## info 
# URL: http://localhost:8080
# Username: airflow
# Password: airflow

# Exit immediately if any command fails

set -e

##############################################################################

# 1. DOCKER DATABASE SETUP

##############################################################################

# Pull required Docker images (PostgreSQL and MariaDB)

docker pull postgres:alpine
docker pull mariadb:10.6

# Run PostgreSQL container with user, password, DB, port and volume

docker run -d 
--name postgres_db 
-e POSTGRES_USER=Ritik 
-e POSTGRES_PASSWORD=Ritik@843313 
-e POSTGRES_DB=testdb 
-p 5432:5432 
-v postgres_data:/var/lib/postgresql/data 
postgres:alpine || true   # Ignore error if container already exists

# Run MariaDB container with credentials, DB, port and volume

docker run -d 
--name maria_db 
-e MYSQL_ROOT_PASSWORD=secret 
-e MYSQL_DATABASE=testdb 
-e MYSQL_USER=Ritik 
-e MYSQL_PASSWORD=Ritik@843313 
-p 3306:3306 
-v mariadb_data:/var/lib/mysql 
mariadb:10.6 || true   # Ignore error if container already exists

# List running containers to verify setup

docker ps

##############################################################################

# 2. PYTHON VIRTUAL ENVIRONMENT

##############################################################################

# Create a Python virtual environment named 'python'

python3 -m venv python

# Activate the virtual environment

source python/bin/activate

# Upgrade pip to latest version

python -m pip install --upgrade pip

# Check Python version inside virtual environment

python --version

##############################################################################

# 3. JAVA SETUP

##############################################################################

# Update system package list

sudo apt update

# Install OpenJDK 17 (required for PySpark)

sudo apt install -y openjdk-17-jdk

# Verify installed Java version

java -version

# Get the actual path of Java binary

readlink -f $(which java)

##############################################################################

# 4. PYTHON DEPENDENCIES

##############################################################################

# Remove existing PySpark installation if present

pip uninstall pyspark -y || true

# Install required Python libraries

# - pyspark: for distributed data processing

# - jupyterlab: for notebooks

# - pandas: for data analysis

# - numpy: for numerical operations

pip install pyspark jupyterlab pandas numpy

##############################################################################

# END OF SETUP

##############################################################################
