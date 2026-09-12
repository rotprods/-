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

## Verificación externa de INFRA-005

Commit d8fdc7c: CI success, clon limpio con integridad/control/native PASS. Drive: snapshot descargado de nuevo, SHA256 idéntico y 147 entradas del manifiesto verificadas. Contratos de Linear leídos: 6 hitos, 17 tareas. Índices de estudio y aprendizaje leídos tras escritura. Mem sigue pendiente por rate limit tras dos intentos; queda en cola. La primera ejecución programada aún no está demostrada.

## EXO-004-INPUT-001 · Controles y jugabilidad inicial

Implementados movimiento y cámara analógicos, botones de combate, navegación/foco de menús, remapeo persistente y ayudas dinámicas. Corregidos el rechazo de preferencias JSON válidas, la comparación de botones tras recarga y la documentación equivocada de guardia/esquiva. 34 tests Python + 26 estado + 19 integración + 33 input pasan; cinco gates nativos. Recorrido real por inputs desde spawn hasta Inés, sin teletransporte ni avance de estado artificial. UI renderizada en Mesa a 1280×720 y comprobada dentro del viewport; no aprobación artística AAA. EXO-004 permanece en revisión: falta la ruta completa y prueba humana/con mando físico. Mem volvió a limitar solicitudes; cola conserva el tercer intento sin insistir.


## EXO-006-ART-001 · isolated art checkpoint, 12 September 2026
User assigned this agent to remote Blender; gameplay stays with the parallel agent. Branch art/terra-reliquary-kit-001 and PR #1 reserve art_source. External agent acknowledgment has not been observed. Do not replace newer main STATE/PLAN with this branch snapshot blindly.

Original campaign catalog: 318 rows covered, 12 art directions, 21 category contracts, 28 Terra module briefs, all planned. Actual candidate: remote project710b21ea-a09a-4f3c-b3a4-ca446ec58bc8 revision4, editable .blend/GLB, 11 assembly roots, 12 embedded maps, 11 collision sources. Source/art evidence lives in art_source/terra_reliquary_kit/delivery.json and README.md. No runtime scripts/scenes or existing portal changed. Native import/PBR/UV and floor collision probe pass; normal Gauntlet still passes. Renders inspected; no human AAA or GPU gate is claimed.

Failures retained: first render exceeded300000ms, missing presentation UV corrected, close-up faceting corrected, podium contact corrected. Isolated Godot visual capture is blocked by Xvfb listener/display; headless engine works. Telemetry is partial. Mem queue retained without another retry.

Gameplay handoff: EXO-004-ROUTE-002 experimental input driver reached Ines then failed at custodian_0; unclassified cause, not a confirmed gameplay regression. Disabled experiment and world.patch are archived in art_source/coordination. Next gameplay owner investigates route independently.

Next art unit: inspect this candidate with the actual camera on a working display, resolve interaction clearance/texel density/LOD transition and localized wear before expanding the 28-module kit or producing character final topology. The complete twelve-world campaign remains open.
