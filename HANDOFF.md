# EXOVANT — continuidad operativa

Leer AGENTS.md, _project_intelligence/STATE.json, PLAN.json, MEMORY.md y GOALS.md. ROADMAP es una proyección del contrato; la biblia mantiene el objetivo de doce mundos. El juego sigue siendo un prototipo de Terra y no un producto AAA terminado.

## Recuperar

Clonar https://github.com/rotprods/-.git. Ejecutar `python3 tools/project_control.py check` antes de alterar archivos, `python3 tools/bootstrap_godot.py --destination .tools`, `make test`, `make native`. Si el binario no coincide, detener esa instalación; no sobrescribir otro motor. La URL oficial fijada sustituyó un endpoint que devolvía 403 y CI verificó la reparación.

## Trabajar

Consultar PLAN y seleccionar una unidad desbloqueada. Comprobar HEAD remoto y posibles cambios ajenos. `python3 tools/studio.py start EXO-004 --run <id-unico>` reserva el escritor y registra contexto y recuperación de aprendizajes. Implementar, atacar los casos anómalos, ejecutar gates, registrar evidencia. No declarar done sin todas las pruebas requeridas, incluidas las humanas donde aplique. Cerrar run con studio.py finish; actualizar memoria/progreso y publicar checkpoint mediante conector GitHub si la terminal no tiene credenciales.

## Frontera de producto

EXO-004: recorrer una partida nueva completa sin teletransportes ni estados de debug; observar fricción, arreglar bloqueos y después controles/orientación. EXO-006/007: optimizar portal y producir un kit Terra y personaje de referencia dentro del motor. EXO-012: probar Unreal en un host con GPU adecuado antes de decidir migración. Mesa actual renderiza por CPU; Blender remoto está comprobado, el Mac no está conectado por esta sesión.

## Superficies y ejecución

GitHub es fuente del juego; rot.knowledge contiene el índice canónico del Learning OS hacia sus eventos; game-dev-mcp-hub contiene integración y políticas de estudio. Linear organiza las seis fases y unidades; Drive conserva dossier y snapshot; Mem recupera enlaces. Los registros de proveedores están en el dossier operativo y en la entrada EXOVANT de rot.knowledge. No copiar IDs de archivos temporales como si fueran persistentes.

La tarea horaria recupera main y comprueba capacidades en cada activación. Su habilitación no demuestra disponibilidad de shell/motor ni una primera ejecución autónoma. En caso de conflicto, fallo de herramienta o interrupción, conservar el último commit, reconciliar el resultado y registrar el bloqueo; no reiniciar la planificación.

## Estado de la ola

Los recibos actuales y el estado de cierre de INFRA-005 están en STATE, PLAN y evidence. Nunca utilizar un porcentaje de Linear para afirmar avance artístico o de campaña. La última respuesta del chat no es la fuente de verdad.

INFRA-005 se cierra como checkpoint en revisión: controles locales, CI, clon limpio y restauración de Drive comprobados. Pendiente observar la primera activación programada y el espejo Mem (rate limit). EXO-004 no depende de estos pendientes. ops/sync-queue.json evita perderlos; no repetir toda la fase de infraestructura antes de trabajar en producto.

## Próxima unidad tras EXO-004-INPUT-001

Controles y primer tramo ya comprobados: no rehacerlos. Continuar EXO-004-ROUTE-002 con la ruta nueva Inés → riego → archivo → ATLAS → consecuencia → portal, usando controles y colisión normales, sin teletransportes ni concesión de flags/daño. Atacar orden de misiones (incluido llegar a ATLAS antes del archivo), muerte/recuperación y recarga. Guardar fricción y fixes; GATE-PLAY humano sigue pendiente. Para remapeo sintético usar --test-input (preferencias y partida separadas). La captura controls-ui.png es CPU; no demuestra rendimiento ni acabado artístico.


## EXO-006-ART-001 · isolated art checkpoint, 12 September 2026
User assigned this agent to remote Blender; gameplay stays with the parallel agent. Branch art/terra-reliquary-kit-001 and PR #1 reserve art_source. External agent acknowledgment has not been observed. Do not replace newer main STATE/PLAN with this branch snapshot blindly.

Original campaign catalog: 318 rows covered, 12 art directions, 21 category contracts, 28 Terra module briefs, all planned. Actual candidate: remote project710b21ea-a09a-4f3c-b3a4-ca446ec58bc8 revision4, editable .blend/GLB, 11 assembly roots, 12 embedded maps, 11 collision sources. Source/art evidence lives in art_source/terra_reliquary_kit/delivery.json and README.md. No runtime scripts/scenes or existing portal changed. Native import/PBR/UV and floor collision probe pass; normal Gauntlet still passes. Renders inspected; no human AAA or GPU gate is claimed.

Failures retained: first render exceeded300000ms, missing presentation UV corrected, close-up faceting corrected, podium contact corrected. Isolated Godot visual capture is blocked by Xvfb listener/display; headless engine works. Telemetry is partial. Mem queue retained without another retry.

Gameplay handoff: EXO-004-ROUTE-002 experimental input driver reached Ines then failed at custodian_0; unclassified cause, not a confirmed gameplay regression. Disabled experiment and world.patch are archived in art_source/coordination. Next gameplay owner investigates route independently.

Next art unit: inspect this candidate with the actual camera on a working display, resolve interaction clearance/texel density/LOD transition and localized wear before expanding the 28-module kit or producing character final topology. The complete twelve-world campaign remains open.
