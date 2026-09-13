# EXOVANT — contrato de continuidad

Este repositorio contiene EXOVANT 2950 (nombre inicial del repositorio: Humanity game). La visión y sus doce mundos se conservan; las pruebas del prototipo no completan el videojuego.

## Inicio obligatorio
1. Leer este archivo, `_project_intelligence/STATE.json`, `HANDOFF.md`, `MEMORY.md` y `_project_intelligence/PLAN.json`, `GOALS.md` y `ROADMAP.md`.
2. Leer `learning/README.md`; ejecutar `python3 tools/aprende_runtime.py audit learning/hub` y recuperar los aprendizajes relevantes con `retrieve learning/hub <consulta>`.
3. Leer `git status`, recuperar `origin/main`, anotar el SHA base. Si hay cambios ajenos, reconciliar antes de escribir. No sobrescribir una sesión activa.
4. Comprobar ejecutables, límites y dispositivos actuales. El inventario de game-dev-mcp-hub describe otra máquina y una fecha; no prueba conectividad.
5. Ejecutar `python3 tools/studio.py start TASK --run RUN` para reservar un escritor local y emitir BOOTSTRAP con contexto y aprendizajes. Los hashes identifican los archivos disponibles; no prueban por sí solos comprensión del agente. El recibo no aumenta autoridad.

## Preflight obligatorio de ownership para producción artística multiagente
Antes de seleccionar, reservar o modelar un mundo, región, personaje, criatura, vehículo, boss o kit compartido:

1. Leer la superficie de coordinación activa `https://github.com/rotprods/-/issues/7` y no tratarla como canon narrativo; sirve únicamente para evitar solapes.
2. Recuperar **todas las ramas actuales y los PR abiertos/cerrados relevantes** del repositorio. No decidir disponibilidad con una captura antigua, un mensaje de chat ni solo por ausencia de assignee en Linear.
3. Clasificar la intención como `WORLD_OWNER` o `ATOMIC_SUBCLAIM`:
   - `WORLD_OWNER`: una sola rama posee el mundo completo de arte/modelado.
   - `ATOMIC_SUBCLAIM`: trabajo estrictamente acotado dentro de un mundo ya ocupado, con ID, exclusiones y assets concretos.
4. Una rama de reserva existente basta para considerar un mundo **OCCUPIED**, aunque todavía no exista PR. Solo puede liberarse con evidencia explícita `ABANDONED`, `SUPERSEDED` o cierre equivalente.
5. No confundir ramas históricas abandonadas con owners activos. Cruzar `branch + PR state/title/body + Linear scope` antes de decidir.
6. Para un mundo libre, crear la rama de reserva y la tarea Linear **antes** de producir geometría; después volver a consultar ramas. Si aparece una reserva concurrente, detenerse y reconciliar antes de escribir más.
7. Si el mundo ya tiene owner, no abrir otra rama `full world`. Crear un claim atómico (`CLM-<WORLD>-<DOMAIN>-<NAME>-<NNN>`) y acordar una partición no solapada de asset IDs/colecciones.
8. Cada PR artístico debe declarar: mundo/claim, owner branch, exclusiones, estado de verdad (`planned`, `implemented`, `locally_validated`, etc.), dependencias y handoff.
9. En colisión, el agente posterior abandona o reduce scope; conservar evidencia del conflicto en vez de ocultarlo. Nunca force-push ni sobrescribir trabajo ajeno.
10. Antes de cada nueva ola significativa, repetir este preflight. El ownership puede cambiar mientras varios agentes trabajan en paralelo.

## Desarrollo y Gauntlet
Trabajar en una unidad acotada del backlog, con criterio de aceptación observable. OBSERVE → GRAPHIFY → PLAN → ATTACK → IMPLEMENT → TEST → EVIDENCE → PERSIST → COLD RESUME → NEXT. Corregir regresiones antes de añadir contenido. A la sexta iteración del mismo fallo revisar causa y arquitectura.

El juego debe funcionar offline. No mezclar llamadas a proveedores con runtime del videojuego. No añadir generaciones, compras o infraestructura especulativa. Autorizar un repositorio no convierte todos sus MCP en servicios activos. Las políticas de infraestructura se leen en su propio repositorio antes de modificarlo.

## Cierre de cada cambio significativo
- Ejecutar `python3 tests/run_gauntlet.py --godot /ruta/Godot_v4.7.2-stable_linux.x86_64` para cambios de juego/asset.
- Ejecutar `python3 -m unittest discover -s tests -p 'test_*.py'` y `python3 tools/project_control.py check`.
- Registrar defectos, mecanismo y evidencia; añadir LearningEvent inmutable si hay aprendizaje, o registrar no-promoción. No editar eventos anteriores para fingir una verificación posterior.
- Actualizar STATE (checkpoint global), PLAN (estado de tareas), PROGRESS y HANDOFF. Generar GOALS/ROADMAP y grafo con `studio.py project` y `graphify_project.py`; el check rechaza drift. Ejecutar `python3 tools/project_control.py refresh` y después `check`.
- Un solo commit agrupa fuentes, estado y pruebas. Push normal con padre verificado; nunca force. Si el remoto cambia, recuperar, reconciliar y repetir los gates relevantes.
- Actualizar las proyecciones Linear/Drive después de la escritura canónica. Las proyecciones tienen SHA o checkpoint; si fallan, registrar pendiente y conservar la fuente.
- Cerrar con `studio.py finish --run RUN --outcome checkpoint|blocked|done --next ...`, pasando recibos y learning IDs pertinentes. Done exige todos los gates y dependencias; un checkpoint permite cerrar trabajo parcial sin falsear el estado. Escribir exactamente un CLOSE por run, idempotente para contenido idéntico. Dejar una siguiente acción ejecutable. Los agentes no son procesos permanentes por existir un JSON.

## Claims y límites
Para trabajo paralelo, leer `docs/FLEET_COORDINATION.md`, `main:ops/fleet/registry.json` y el [hilo #7](https://github.com/rotprods/-/issues/7). Las reservas de productores importadas no implican acuse. Confirmar owner/claim/rutas/proyecto remoto y publicar reservas mediante padre actual + ref sin force. Ejecutar `fleet_control.py guard-git` sobre el checkout de entrega; preservar cambios globales de otras ramas como propuestas para el integrador. No reemplazar STATE/PLAN/MANIFEST/grafo de main con los de una rama artística. `studio.py` es lock local, no distribuido; ningún heartbeat viejo libera un mundo automáticamente. Ares PR #2 está abandonado; Sylva macro y root-kit necesitan acuse del reparto proveedor/consumidor. Los snapshots no sustituyen lecturas actuales.

Usar planned / implemented / locally_validated / empirically_qualified / released con evidencia adecuada. Render de CPU no es benchmark GPU; modelo bonito no valida colisiones; tests con teletransporte no son una partida humana; tarea programada creada no es tarea ejecutada. No afirmar AAA, DLSS, Unreal operativo o campaña final sin sus gates. Calidad artística: silueta, materiales, animación, composición y rendimiento conjunto; la cantidad de polígonos no basta.

## Fuentes del método
Protocolos del usuario en rotprods/rot.knowledge: APRENDE_MASTER, APRENDE_ENFORCEMENT, COS_GRAPH_ENGINE_V2_MASTER, GRAPHIFY_MASTER y GAUNTLET_LOOP_MASTER. Versiones recuperadas en `docs/PROTOCOLS.md`. Aplicación local acotada; no se afirma enforcement universal en aplicaciones ajenas.

## Admisión y aprendizaje compartido
Antes de aceptar trabajo, recuperar LRN-EXO-20260912-OWNER-ADMISSION. Cada owner produce, recupera y valida sus assets; el integrador interviene por entrega lista, conflicto entre ámbitos, regresión compartida o decisión necesaria. Reutilizar evidencia ligada a fuente/versión/contexto; repetir gates cuando la integración invalide esa evidencia. No duplicar producción ni crear auditorías para mantener actividad. Cada owner incluye en su próximo handoff normal learning_id, claim, commit, acción aplicada y evidencia, o explica por qué no aplica; no emitir heartbeats extra. Publicación no equivale a lectura/adopción. El integrador horario está pausado por decisión del usuario; no reactivarlo automáticamente. La incidencia visual local puede diagnosticarse como tarea compartida, sin asumir que la VM equivale al Mac o que la ausencia de GPU impide todos los trabajos.

## EXOVANT-X100 V2 — protocolo por defecto para mundos y assets

Tras el bootstrap y **antes de seleccionar nuevo trabajo de mundo/asset**, leer `docs/EXOVANT_X100_V2.md` y `ops/x100/config.json`. El orden obligatorio pasa a ser:

`RESYNC → X100_SPATIAL_BUILD → FLEET_PREFLIGHT → X100_COVERAGE_AUDIT → BOTTLENECK_GRADIENT → ELIGIBLE_GAPS → CLAIM → BUILD → GAUNTLET → RECEIPT → RECOMPUTE → NEXT`.

Reglas de adopción:
- Ejecutar `python3 tools/x100_spatial.py build` después de recuperar refs/registro actuales. La proyección vectorial sirve para awareness/retrieval; **Fleet sigue siendo autoridad de ownership**.
- Nunca inventar coordenadas: `spatial_known=0` no significa origen. Inferencias desde nombres de rama se etiquetan y no crean ownership.
- Usar `python3 tools/x100_control.py audit ...` para medir el mundo y `rank ...` para ordenar gaps. Un gap reclamado por otro owner es ineligible aunque tenga mayor score.
- Después de cada wave con evidencia, actualizar el audit X100 dentro de una ruta owned y recalcular el gradiente. No declarar WORLD_COMPLETE por cerrar un asset local.
- Tier S/A o assets de identidad fuerte siguen por defecto `LOOK_LOCK → IMAGE_TARGET → IMAGE_TO_3D_BASE → CLEANUP/RETOPO → MATERIAL → LOD/COLLISION → ENGINE → VISUAL_REGRESSION`. Higgsfield 3D Jutsu es una superficie preferente cuando aporta reconstrucción útil; **raw AI/reconstruction mesh nunca es final**.
- Kits sistémicos pueden usar modelado procedural/manual en lugar de image-to-3D cuando produzca geometría más limpia/reutilizable; registrar waiver.
- El objetivo 5/20/75 HERO/SUPPORT/SYSTEMIC y 100+ configuraciones es una guía de planificación, no permiso para ruido. Variación siempre causal.
- X100 no muta el Fleet registry, no libera claims y no sustituye STATE/PLAN/MANIFEST. Integra selección de trabajo; Fleet controla colisiones; Graphify/COS conserva relaciones; Gauntlet valida evidencia.
