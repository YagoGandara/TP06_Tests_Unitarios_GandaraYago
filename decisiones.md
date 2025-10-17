# Decisiones técnicas (TP06)

- **Objetivo**: pruebas unitarias y de componentes aisladas (sin BD real).
- **Back**: FastAPI + PyTest + httpx; repo en memoria para aislar persistencia.
- **Front**: Vite/React + Vitest + RTL; mock de `fetch` para API.
- **Reportes**: JUnit XML + cobertura (Cobertura/LCOV).
- **CI**: Azure DevOps con dos jobs (backend/front) y publicación de resultados.
