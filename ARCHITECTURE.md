# Arquitectura EXOVANT 2950

## Autoridad y proyecciones
GitHub `rotprods/-` contiene fuentes, diseño, assets editables, tests y estado. `_project_intelligence/STATE.json` es el estado canónico; los Markdown son vistas legibles. `graph.json` enlaza hechos, decisiones, artefactos, pruebas y fronteras. No es una segunda base de verdad. Linear organiza unidades de trabajo y Drive conserva un dossier y snapshots identificados. Mem ofrece recuperación por conceptos y enlaces. Los MCP de estudio pertenecen a `rotprods/game-dev-mcp-hub`; no se copian sus submódulos al videojuego.

## Runtime actual
`scenes/main.tscn` carga `scripts/world.gd`. World construye Terra y coordina interacciones, NPC, puzzle, enemigos y HUD. Player controla cámara, desplazamiento, stamina, bloqueo, ataques, curación y vehículo básico. Enemy implementa estados de ataque/recuperación y visibilidad física. Progress es la autoridad de misiones/recompensas. SaveStore serializa un sobre versionado con digest, escritura temporal y generación de respaldo. Este guardado es de un proceso; no es base de datos concurrente.

La primera frontera de modularización es extraer datos de encuentros, objetivos y diálogo del World cuando se amplíe EXO-005/009. No trasladar los doce mundos a un único script gigante. Separar dominio persistente de presentación antes de viajes planetarios. Identificadores estables del catálogo sobreviven cambios de escena y motor.

## Pipeline de arte
`art_source/reliquary_gate` conserva Blender, generadores y validación. `assets/reliquary_gate.glb` es el intercambio actual con Godot. Se eliminan nodos de presentación en runtime y se añade colisión jugable; eso debe evolucionar a un export de producción con colisión separada, pivotes, escala, UV, texturas, LOD y presupuesto medido. Blender remoto no equivale a Unreal remoto. Mantener GLB como intercambio y .blend como fuente.

## Cuatro planos COS / CGVE2
Authority: instrucciones vigentes + AGENTS + STATE + fuentes.
Projection/context: MEMORY, PROGRESS, HANDOFF, graph y superficies externas.
Execution: unidades EXO, herramientas disponibles, código, assets y builds.
Assurance: Gauntlet, hash de fuentes, tests adversariales, recibos, aprendizaje y recuperación en frío.

El grafo se actualiza tras cambios significativos y se verifica en cada cierre. No hay observador universal de aplicaciones ni grafo 24/7: la actualización sucede dentro de las ejecuciones reales. JSON versionado es suficiente hoy; no se instala una base de grafos.

## Producción y motor
Godot 4.7.2 es el prototipo ejecutable. Unreal 5.8 sigue como candidato de producción, sujeto a EXO-012: misma escena representativa, controles, geometría, materiales, tiempos CPU/GPU, memoria, carga y export. La migración no se decide por marketing o por tener un conector. Ni DLSS ni el aumento de polígonos resuelven diseño de combate, animación o composición.
