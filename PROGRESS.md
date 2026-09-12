# Progreso comprobable

| Hito | Resultado | Límite |
|---|---|---|
| Preproducción | Biblia, catálogo y planificación de 12 mundos, 84 misiones y 318 filas de assets | Propuestas, no contenido implementado |
| Blender remoto | Portal editable .blend, GLB, script, render y una animación | 142.916 triángulos indexados del export completo; optimización pendiente |
| Godot local | Proyecto 3D nativo, interacción, combate, puzzle, NPC, ATLAS y guardado | Prototipo; no campaña completa ni arte AAA |
| Gauntlet 003 | 26 comprobaciones de estado + 19 de integración; import y smoke | Setup controlado, no partida humana completa |
| Mesa | Captura real del runtime mediante llvmpipe | CPU; no perfil GPU |
| Recuperación anterior | Extracción sin caché y repetición de gates | Ahora se migra la autoridad a GitHub |
| Persistencia 004 | Contrato de agentes, memoria, arquitectura, grafo, aprendizajes, control de integridad y telemetría | Estado final y recibos en STATE y evidence; no enforcement universal |

Defectos resueltos: rampa con escalón que bloqueaba al personaje; parser de JSON corrupto que ensuciaba el gate; daño a través de cobertura; problemas de inferencia de tipos; exposición y barras de vida ilegibles. Los casos ejecutables permanecen en tests.

Siguiente incremento de producto: EXO-004, recorrido completo sin teletransportes y observación de fricción, después controles y orientación. Mantener este hito de persistencia separado de una mejora de jugabilidad: esta ola no añade mundos ni ataques.

## Infraestructura 005 — reparación de descarga

El fallo de GitHub Actions se reprodujo localmente: HTTP 403 del endpoint de descarga. La URL oficial de release 4.7.2 permitió descargar e instalar con hashes coincidentes. Siete pruebas adicionales cubren corrupción, truncado, tamaño y preservación del binario existente. El clon remoto conservó íntegros los 108 archivos y pasó los cuatro gates nativos. CI corregido pendiente de ejecución remota.

## INFRA-005 · contrato y herramientas

Añadidos PLAN con 6 objetivos, 6 fases, 17 unidades y 10 gates; GOALS/ROADMAP generados; control de escritor local y cierre con evidencia; graph drift check; auditoría GLB; paquete reproducible y restore remoto; telemetry opt-in de conectores; pruebas adversariales adicionales. Linear refleja seis hitos y diecisiete tareas. Integraciones documentales publicadas en game-dev-mcp-hub y rot.knowledge. Mem devolvió rate limit en el primer intento; no se declara sincronizado. Cierre global de infraestructura todavía en cualificación.
