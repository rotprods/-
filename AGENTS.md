# EXOVANT — contrato de continuidad

Este repositorio contiene EXOVANT 2950 (nombre inicial del repositorio: Humanity game). La visión y sus doce mundos se conservan; las pruebas del prototipo no completan el videojuego.

## Inicio obligatorio
1. Leer este archivo, `_project_intelligence/STATE.json`, `HANDOFF.md`, `MEMORY.md` y `_project_intelligence/PLAN.json`, `GOALS.md` y `ROADMAP.md`.
2. Leer `learning/README.md`; ejecutar `python3 tools/aprende_runtime.py audit learning/hub` y recuperar los aprendizajes relevantes con `retrieve learning/hub <consulta>`.
3. Leer `git status`, recuperar `origin/main`, anotar el SHA base. Si hay cambios ajenos, reconciliar antes de escribir. No sobrescribir una sesión activa.
4. Comprobar ejecutables, límites y dispositivos actuales. El inventario de game-dev-mcp-hub describe otra máquina y una fecha; no prueba conectividad.
5. Ejecutar `python3 tools/studio.py start TASK --run RUN` para reservar un escritor local y emitir BOOTSTRAP con contexto y aprendizajes. Los hashes identifican los archivos disponibles; no prueban por sí solos comprensión del agente. El recibo no aumenta autoridad.

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
Usar planned / implemented / locally_validated / empirically_qualified / released con evidencia adecuada. Render de CPU no es benchmark GPU; modelo bonito no valida colisiones; tests con teletransporte no son una partida humana; tarea programada creada no es tarea ejecutada. No afirmar AAA, DLSS, Unreal operativo o campaña final sin sus gates. Calidad artística: silueta, materiales, animación, composición y rendimiento conjunto; la cantidad de polígonos no basta.

## Fuentes del método
Protocolos del usuario en rotprods/rot.knowledge: APRENDE_MASTER, APRENDE_ENFORCEMENT, COS_GRAPH_ENGINE_V2_MASTER, GRAPHIFY_MASTER y GAUNTLET_LOOP_MASTER. Versiones recuperadas en `docs/PROTOCOLS.md`. Aplicación local acotada; no se afirma enforcement universal en aplicaciones ajenas.
