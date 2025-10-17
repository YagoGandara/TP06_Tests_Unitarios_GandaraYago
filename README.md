# TP06 – Pruebas Unitarias (base limpia)

Repo limpio para el TP06 partiendo de TP05, sin BD persistente ni deploy.

## Backend
```bash
python -m venv .venv && source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn app.main:app --reload
pytest -q backend/tests --cov=backend/app --cov-report=term-missing --cov-report=xml:backend/coverage.xml --junitxml=backend/test-results/pytest-results.xml
```

## Frontend
```bash
cd front
npm ci
npm run test
```

## CI
Pipeline `azure-pipelines.yml` corre tests de front y back, publica **JUnit** y **Cobertura**.
