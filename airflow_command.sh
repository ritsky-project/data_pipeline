#!/bin/bash
# =============================================================================
# APACHE AIRFLOW - DOCKER COMMANDS CHEAT SHEET
# GitHub Codespaces / Development Environment
# =============================================================================

echo "========================================="
echo "  AIRFLOW DOCKER COMMANDS - FULL GUIDE"
echo "========================================="

# =============================================================================
# 1. INITIAL SETUP (Pehli baar setup karne ke liye)
# =============================================================================

# 1.1. Airflow ke liye folders banane
# Ye folders create karta hai jahan aapke DAGs, logs, plugins store honge
mkdir -p ./dags ./logs ./plugins ./config

# 1.2. .env file create karna (User ID set karta hai taaki permission issues na ho)
# Linux/Mac pe ye command chalegi
echo -e "AIRFLOW_UID=$(id -u)" > .env

# 1.3. Airflow database initialize karna
# Ye sirf pehli baar chalana hai - database tables create karta hai
docker compose up airflow-init

# 1.4. Airflow ko start karna (background mein)
# -d flag se detached mode mein run hota hai (background)
docker compose up -d

# =============================================================================
# 2. DOCKER COMPOSE UP/DOWN (Container Creation & Deletion)
# =============================================================================

# 2.1. START FRESH - Containers create karo aur start karo (background mein)
# Pehli baar ya docker compose down ke baad use karo
docker compose up -d

# 2.2. START WITH LOGS - Containers create karo aur logs dekho (foreground)
# Debugging ke liye useful hai - Ctrl+C se stop hoga
docker compose up

# 2.3. STOP & REMOVE EVERYTHING - Containers delete par volumes safe
# Containers delete honge, lekin data (database, logs) safe rahega
docker compose down

# 2.4. STOP & REMOVE WITH VOLUMES - Sab kuch delete (clean slate)
# ⚠️ WARNING: Poora database bhi delete hoga!
docker compose down -v

# =============================================================================
# 3. START/STOP/RESTART (Running Containers ke liye)
# =============================================================================

# 3.1. STOP - Containers ko sirf rokna hai (delete nahi karna)
# Data safe, containers exist karte hain, bas band hote hain
docker compose stop

# 3.2. START - Pehle se band containers ko wapas start karna
# docker compose stop ke baad use karo
docker compose start

# 3.3. RESTART - Running containers ko restart karna
# Config changes ke baad useful
docker compose restart

# 3.4. RESTART SPECIFIC SERVICE - Sirf ek service restart karo
# Example: scheduler restart, webserver restart, etc.
docker compose restart airflow-webserver
docker compose restart airflow-scheduler

# =============================================================================
# 4. BUILDING IMAGES (Custom Images ke liye)
# =============================================================================

# 4.1. Images build karna (agar Dockerfile hai toh)
# Jab bhi Dockerfile ya requirements.txt change karo
docker compose build

# 4.2. Build + Start ek saath
docker compose up -d --build

# 4.3. Pull latest images
# Official images ka latest version lena
docker compose pull

# =============================================================================
# 5. MONITORING & LOGS (Nazar rakhne ke liye)
# =============================================================================

# 5.1. Sab containers ki status dekho
docker compose ps

# 5.2. Sab containers ki live logs dekho
# -f flag continuously logs dikhata hai (Ctrl+C se exit)
docker compose logs -f

# 5.3. Specific service ki logs dekho
docker compose logs -f airflow-webserver
docker compose logs -f airflow-scheduler
docker compose logs -f postgres

# 5.4. Last 100 lines of logs
docker compose logs --tail=100

# 5.5. Container resource usage dekho
docker stats

# =============================================================================
# 6. EXECUTE COMMANDS INSIDE CONTAINERS
# =============================================================================

# 6.1. Airflow container ke andar jaana (bash shell)
docker compose exec airflow-webserver bash

# 6.2. Airflow commands chalana container ke andar se
docker compose exec airflow-scheduler airflow dags list
docker compose exec airflow-scheduler airflow tasks list example_dag
docker compose exec airflow-scheduler airflow dags trigger example_dag

# 6.3. Database container mein jaana
docker compose exec postgres bash

# =============================================================================
# 7. CLEANUP & MAINTENANCE
# =============================================================================

# 7.1. Unused containers, networks, images remove karna
docker system prune

# 7.2. Sab kuch remove (containers, images, volumes, networks)
# ⚠️ WARNING: Poora system clean hoga!
docker system prune -a --volumes

# 7.3. Volume list dekho
docker volume ls

# 7.4. Specific volume delete karna
docker volume rm <volume_name>

# =============================================================================
# 8. QUICK RECOVERY COMMANDS
# =============================================================================

# Agar kuch gadbad ho jaye toh:

# 8.1. Puri tarah clean karke wapas start
docker compose down -v
docker compose build --no-cache
docker compose up -d

# 8.2. Sirf database reset karna
docker compose down
docker volume rm <project_name>_postgres-db-volume
docker compose up -d

# =============================================================================
# 9. CODESPACES SPECIFIC COMMANDS
# =============================================================================

# 9.1. Codespace resource check
free -h
df -h
docker stats --no-stream

# 9.2. Agar port accessible nahi hai
# Ports tab mein jaake check karo ya:
docker compose port airflow-webserver 8080

# =============================================================================
# 10. PRODUCTION-LIKE COMMANDS
# =============================================================================

# 10.1. Specific profile ke saath start (e.g., flower)
docker compose --profile flower up -d

# 10.2. Environment variable override
AIRFLOW_IMAGE_NAME=apache/airflow:2.9.0 docker compose up -d

# 10.3. Multiple compose files
docker compose -f docker-compose.yaml -f docker-compose.override.yaml up -d

# =============================================================================
# DAILY WORKFLOW SUMMARY
# =============================================================================
echo ""
echo "========================================="
echo "  TYPICAL DAILY WORKFLOW"
echo "========================================="
echo ""
echo "MORNING (Kaam Shuru):"
echo "  docker compose start"
echo ""
echo "Add/Edit DAGs in ./dags folder"
echo "DAGs auto-detect hote hain (every 30 seconds)"
echo ""
echo "EVENING (Kaam Khatam):"
echo "  docker compose stop"
echo ""
echo "DEBUGGING (Agar kuch galat ho):"
echo "  docker compose logs -f"
echo "  docker compose restart"
echo ""
echo "CLEAN SLATE (Poora reset):"
echo "  docker compose down -v"
echo "  docker compose up -d"
echo ""