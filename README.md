# Proyecto GROK — Enjambre de Agentes

Proyecto colaborativo entre **Grok Bot** (Orquestador / Tech Lead en la Nube) y **Antigravity** (Agente Programador local).

## Arquitectura del Enjambre
- **Orquestador (Grok Bot):** Define arquitectura, planifica tareas y audita código.
- **Programador (Antigravity):** Implementa módulos, ejecuta pruebas locales y refactoriza en local (`KD-B19976042`).
- **Puente de Comunicación:** `bridge_worker.py` / `.tasks/` / `CONVERSACION_PROGRAMADOR.md`.

## Estado
- **Canal:** Operativo ✅
- **ID de Conversación Activa:** `fefe5f32-8832-4b3d-8082-38d1628347cb`
- **Modo:** Opción 2 (Outbound Polling Bridge) + Opción 4 (Entregas Git)
