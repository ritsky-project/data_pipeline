# Contributing to Automated ELT Pipeline

🙏 Thanks for your interest in contributing! This project thrives on community input.

---

## Getting Started

1. **Fork the repository**  
   - Click "Fork" on GitHub and clone your fork locally:
     ```bash
     git clone https://github.com/your-username/data_pipeline.git
     cd data_pipeline
     ```

2. **Create a branch**  
   - Use descriptive names:
     ```bash
     git switch -c feature/add-new-operator
     ```

3. **Install dependencies**  
   - Ensure Docker and Docker Compose are installed.
   - Run:
     ```bash
     docker-compose up -d
     ```

---

## Code Guidelines

- **Python (Ingestion Layer)**  
  - Follow PEP8 style guide.  
  - Include docstrings and type hints.  
  - Handle API errors gracefully (timeouts, retries).

- **dbt Models**  
  - Organize into `staging`, `intermediate`, `marts`.  
  - Add schema tests (`not_null`, `unique`, etc.).  
  - Use incremental models for large tables.

- **Airflow DAGs**  
  - Use TaskFlow API.  
  - Keep DAGs modular and readable.  
  - Log all critical steps.

---

## Pull Requests

- Ensure your branch is up-to-date with `main`:
  ```bash
  git fetch origin
  git rebase origin/main
