# Terra · estación de riego y reliquario

Primera entrega de arte del frente EXO-006-ART-001. Es un **candidato 3D editable** con construcción, UV y materiales portables, separado del gameplay en el PR #1. No completa la tarea del portal anterior ni certifica hiperrealismo AAA.

## Fuente y reproducción

- `EXOVANT_Terra_Kit.blend`: fuente Blender 5.2, metros y Z arriba. Conserva piezas semánticas, modificadores de borde, cámaras, iluminación, mapas empaquetados y colisiones independientes.
- `EXOVANT_Terra_Kit.glb`: exportación glTF 2.0 de la misma revisión; materiales PBR y texturas embebidas. Incluye presentación que debe excluirse al integrar gameplay.
- Ejecutar **una vez y en este orden, en escena vacía**: `build_terra_kit.py`, `refine_delivery.py`, `finish_visual_pass.py`, `finish_normals.py`. Los scripts de refinamiento no son idempotentes; nunca lanzarlos contra una escena desconocida o compartida. Las revisiones remotas preservan su historial.
- Proyecto: https://higgsfield.ai/3d-jutsu/710b21ea-a09a-4f3c-b3a4-ca446ec58bc8 · revisión 4. El portal anterior permanece intacto.
- `delivery.json` identifica binarios, renders, operación remota y límites. `review-history.json` conserva fallos y correcciones.

## Componentes y función

| Raíz | Función / dimensiones nominales de diseño |
|---|---|
| `ENV_TERRA_Foundation_10x8` | Pedestal 10 × 8 m, baldosas, bandas de drenaje y tres peldaños; no equivale a una pieza modular de 4 m |
| `ENV_TERRA_SluiceWall_8x4` | Muro 8 m, paneles cerámicos, zócalo ventilado y reparaciones localizadas |
| `ENV_TERRA_RibPilaster_L/R` | Pilastras de carga, costillas y banda de mantenimiento; pareja, no dos diseños únicos |
| `ENV_TERRA_CrownSpine` | Remate central y apoyo de costillas |
| `PR_TERRA_ResonanceRegulator` | Regulador de 3,22 m; manómetro, carcasas, abrazaderas y conducciones |
| `PR_TERRA_RegulatorValve` | Rueda independiente: pivote Blender local `(0, -0.77, 1.08)` respecto al regulador, rotación local Y |
| `PR_TERRA_ServiceConsole` | Consola a ~1,2 m; luces de estado y actuadores |
| `PR_TERRA_ArchiveCradle` | Cuna de tres contenedores; handles y lectura de memoria |
| `KIT_TERRA_SupplyPipe_3m` | Conducto vertical con abrazaderas |
| `BIO_TERRA_WitnessRoots` | Raíces y pequeños depósitos vegetales; estudio geométrico, vegetación de producción pendiente |

Las medidas finales se leen en Blender/GLB, no se deducen del render. Once raíces incluyen una pieza móvil y una pareja simétrica; no significan once assets únicos de la campaña.

## Material y exportación

Cuatro familias compartidas: basalto marino, cerámica, bronce reparado y acero grafito. Cada una usa BaseColor, Roughness y Normal de 512² píxeles, generados de forma determinista y empaquetados. Emisión jade/ámbar y vegetación usan materiales constantes. Las texturas son mapas de superficie; no sustituyen el modelo. Aproximadamente 512 px/m nominal en la proyección métrica; inspeccionar continuidad de UV en curvas antes de adoptar para producción.

El grano de material es una base procedural. Faltan bake de desgaste por curvatura/contacto, texel density final, UV2, validación de tiling y dirección artística humana de cerca/medio/lejos. No confundir cantidad de triángulos ni emisión intensa con realismo.

La fuente incluye 11 proxies separados con sufijo `-colonly`. Godot los convierte en colisión sin malla visible. La válvula tiene pivote, pero todavía no está conectada a estados de misión. Los LOD automáticos de importación Godot están habilitados; aún deben inspeccionarse sus transiciones y medirse en hardware objetivo. No se entregan LOD de autor aprobados.

## Verificar e integrar sin invadir gameplay

1. `python3 art_source/terra_reliquary_kit/audit_candidate.py` comprueba GLB, buffers, UV, mapas y proxies.
2. En un proyecto temporal, copiar GLB como `candidate.glb` y `native_asset_check.gd`. Importar con Godot 4.7.2 y ejecutar el script: comprueba instanciación, material PBR y una sonda física del suelo. Los recibos no sustituyen recorrer el kit.
3. `render_native_preview.gd` produce una comparación aislada en Godot con display, conservando cámara del GLB; no modifica `scripts/`, `scenes/` o `assets/` del juego.
4. El agente de gameplay integra las raíces pertinentes mediante selección explícita. Excluir `PRESENTATION_Ground`, cámaras y luces de estudio. No reemplazar el portal existente con el kit por coincidencia de nombre.
5. Reconectar interacción, comprobar accesos y cámara, escala/pivotes y sombras; jugar, medir y revisar la escena antes de aprobar ART/PERF.

## Coordinación

Rama `art/terra-reliquary-kit-001`, PR https://github.com/rotprods/-/pull/1 y Linear ROT-98. Ámbito de este frente: `art_source/`. Runtime conserva el SHA de partida. Los documentos globales de la rama son una propuesta de integración que requiere reconciliar con el main que publique el otro agente. La reserva local no demuestra coordinación distribuida; no se ha observado aún su acuse.
