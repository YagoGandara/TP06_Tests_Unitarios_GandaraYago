# Decisiones técnicas (TP06)

##Objetivo
Agregar pruebas unitarias y de componentes al proyecto, con cobertura mínima y CI que publique resultados.

##Reglas de Dominio
- **Prioridad**: todas las que tengan prioridad alta **3** deberán tener un `due_date`
- Una `due_date` no puede ser una fecha pasada
- **Transiciones Válidas**: `pending <-> in_progress` y `* -> done`; de `donde` no se puede salir.
- Los títulos deben ser únicos (case-insensitive)
- `PATCH` exige una `version` (da 409 si está desactualizada)
- `toggle` marca `done` y falla si ya estaba en ese estado

El **motivo** de esto fue aumentar la compliejidad de una aplicación antes simple, para justificar les tests hechos


##Backend Test

- **Tipos de Tests**
    - Salud
    - CRUD y validaciones
    - Flitros + paginación
    - Bulk (éxito y error)
    - Concurrencia Optimista (409)
- **Herramientas utilizadas**: `pytest`, `httpx.ASGITransport`, `pytest-asyncio`, `pytest-cov`
- **Cobertura**: `--cov-fail-under=80`


##Frontend Test
- **Servicios**: mocks de `fetch`, asserts de URL's y bodies
- **Componentes**: React Testing Library (interacciones, errorees y UI condicional)
- **Cobertura**: `vitest run --coverage`, umbrales con `vitest.config.ts`
- **JUnit nativo** de Vitest para CI

## CI/CD
- Pipeline en Azure con dos jobs: **backend** y **frontend**.
- Publicación de **JUnit** y **Cobertura**.
- Corte por cobertura baja.