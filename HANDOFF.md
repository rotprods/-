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

## INFRA-005-FLEET-001 · Frontera del integrador

Leer primero docs/FLEET_COORDINATION.md, registro main actual e issue #7. Harness con 41 tests nuevos; recibir acuses restantes y checkpoints binarios. Khepri tiene ACK real y rutas/IDs; Sylva requiere confirmar interfaz macro→root-kit; Ares2 conserva artefactos sin checkpoint formal; Origin ya está reservado (#14). No repetir la auditoría desde cero ni crear otro issue de coordinación.

El padre 196ef814 modificó AGENTS sin MANIFEST y falló CI. La reconciliación preserva ese protocolo y añade control ejecutable; confirmar CI del commit final. La excepción de MANIFEST solo admite generación exacta; los productores no tienen acceso libre al estado global. Mantener EXO-004-ROUTE-002 en su frente de gameplay. Tras adoptar guard/receipts, próxima unidad de arte es cualificar y mejorar kit Terra de PR1 en la cámara del juego, no producir otro kit duplicado. Mem sigue pendiente sin reintento en esta sesión.

## INFRA-005-DELIVERY-003
Se rechazaban mal las entregas GLB con cabecera válida y chunks posteriores truncados, desalineados o duplicados. Corregido y cubierto con siete tests adicionales (seis regresiones antes/después y una extensión desconocida válida). No recupera ADOPTION-002 ni acredita fuentes Blender editables. Próximo: admitir una entrega Khepri fijada con prueba nativa real, consultando primero si su owner ya la integró. Mantener gameplay EXO-004 y arte Terra PR1 en sus scopes. Mac requiere sesión y cualificación propias; plan en issue #7 comentario 5648748464.

## Aprendizaje y definición de remediación
Recuperar LRN-EXO-20260912-OWNER-ADMISSION. Se supera la propuesta de recuperar Khepri por iniciativa del integrador: corresponde al owner salvo necesidad explícita de integración. Automatización pausada. Próxima unidad compartida autorizable: reproducir y resolver visualización Godot de una escena existente aquí; conservar diagnóstico, captura y límites. Consultar contrato de remediación en PLAN.json. Acuses de agentes se incorporan a sus entregas habituales; no se presume aprendizaje universal.

VISUAL-005: graphical Godot capture qualified here after resolving absolute xkbcomp dependency and importing cold-clone assets. See evidence/visual-display-qualified.json and visual-display-runbook.md. CPU llvmpipe only; existing capture repositions player. Capture exit code can hide script errors: inspect log and fresh PNG.

MR-EXO-001: contrato de preparación de migración en PLAN y ubicación de assets/aplicaciones en docs/FLEET_COORDINATION.md. Cumplimiento de flota parcial; respaldos de mundos y manifest drift pendientes. No nuevos agentes/automatización; siguiente unidad es una entrega admitida recuperable y CI correcto, no conexión masiva de apps.

REMEDIATION-007: cinco ACKs de productores reconciliados con evidencia; seis productores active contando Khepri. Restricción Sylva de escritor único sigue vigente. Corregido rechazo de production/manifests/<world>/ y production/receipts/<world>/ con tres pruebas adversariales (85 total); qualify control/graph/asset/native PASS. Aurora reparación CI canary 570a61f7d447708c149b0aa6b3fa9bad8739d000, run 34722208068 SUCCESS. Publicaciones restantes se registran en issue #7 con SHA/readback. PR1 conflictos globales, Vanta workflow temporal activo: no sobrescritos. Backups mundiales, capture_visual false-positive y hardware siguen abiertos.
