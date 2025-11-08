# TP06 – Pruebas Unitarias (base limpia)

Repo limpio para el TP06 partiendo de TP05, sin BD persistente ni deploy.

Stack: **FastAPI (Py3.11) + Vitest/RTL (React 18 + Vite)**.

## Requisitos
 - Python 3.11
 - Node.js 18+ (ideal sería el 20)
 - pip, venv, npm

## Estructura
    backend/
        app/
        tests/
    front/
        src/
    coverage/
    azure-pipelines.yml
    decisiones.md

## Backend (correr local)
```bash
# Desde la Raíz

python -m venv .venv && source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
pytest -q backend/tests --cov=backend/app --cov-report=term-missing --cov-report=xml:backend/coverage.xml --junitxml=backend/test-results/pytest-results.xml --cov-fail-under=80
```

## Frontend (correr tests)
```bash
cd front
npm ci
npm test
npm run test:ci #CI + cobertura + JUnit
```
La cobertura generada es:
    * Backend: `backend/coverage.xml`
    * Frontend: `front/coverage/cobertura-coverage.xml` y `front/test-results/test-results.xml`

## Endpoint Relevantes

`GET /admin/touch`  (health)
`GET /todos` con filtros `q, status, priority, overdue, limit, offset`
`POST /todos` (validaciones)
`PATCH /todos/{id}` con concurrencia optimista (`version`), si no coincide da un 409
`POST /todos/{id}/toggle` marca como 'done', si ya está asi da un 400
`POST /todos/bulk` 

## Concurrencia optimista
Cada `Todo` tiene su `version`. `PATCH` exige un `version` y sube en +1 al aplicar cambios. Si no coinciden da 409

## Bulk
Crea un lote reutilizando reglas del `create`. Si 1 de ellos falla, falla todo el lote

## Frontend
1) `services/api.ts`: requests tipados y maneo de error
2) `components/TodoList.tsx`: carga, alta, toggle, manejo de errores y UI condicional 

## CI
Pipeline `azure-pipelines.yml` corre tests de front y back, publica **JUnit** y **Cobertura**.
