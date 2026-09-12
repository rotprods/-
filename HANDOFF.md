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
