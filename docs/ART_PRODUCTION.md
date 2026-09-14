# Producción visual — estándar y siguiente entrega

La ambición AAA se convierte en criterios de aceptación por asset y escena. La primera pieza de referencia será una ruta Terra del portal al archivo y ATLAS. Paleta propia: basalto húmedo, bronce envejecido, cerámica marfil y luz de tecnología biológica. El colonialismo humano de 2950 debe leerse en infraestructura reutilizada, señalética, prótesis y contraste entre cuidado y extracción.

## Corrección de autoridad: source fidelity antes de lookdev final

Leer junto con `docs/AAA_ASSET_FIDELITY_GATE_V1.md`.

`BLOCKOUT != HERO_ASSET` y `MORE_POLYGONS != MORE_REALISM`.

Una malla puede estar técnicamente bien construida, ser reproducible, importar correctamente en el motor y servir para escala/traversal/collision, pero seguir siendo visualmente un proxy. Antes de invertir en acabado hero, material microdetail, renders largos o claims AAA, el source debe demostrar suficiente información de silueta, proporción, construcción, separación semántica y comportamiento de superficie para la exposición prevista.

Si falla, no se maquilla con más ruido/shaders: se enruta a Asset Factory — manual/procedural/CAD/photogrammetry/multiview reconstruction/hybrid — y se reconstruye sólo el gap de identidad que realmente lo necesita. El blockout útil se conserva como scaffold.

## Kit mínimo representativo
Portal y módulos de acceso; suelo/pared/arco/escalera modular; trim sheet de bronce y cerámica; vegetación de grieta; NPC Inés con vestuario; custodio con rig y arma; avatar con una familia de arma; ATLAS con silueta legible y puntos de anticipación; rover; props de archivo; VFX de impacto, energía y polvo. El catálogo global ya existe en design: no generar cientos de variaciones antes de validar este kit.

## Definition of done de cada asset

### Gate 0 — estado de fidelidad
Declarar uno: `BLOCKOUT`, `PROXY`, `SUPPORT_CANDIDATE`, `HERO_CANDIDATE`, `HERO_QUALIFIED`, `RUNTIME_QUALIFIED`, `CINEMATIC_QUALIFIED`.

### Gate 1 — Source/Hero Fidelity
Para un asset hero o de identidad fuerte: look target aprobado, silueta/proporción, lógica constructiva, semantic parts, material-domain readiness, UV/bake readiness y close-up stress. Raw reconstruction nunca es final. Un proxy no puede saltar a hero sólo por acumular polígonos, materiales o luces.

### Gate 2 — asset técnico
ID y propósito, escala/pivote, fuente editable, licencia/procedencia, malla con nombres, normales y UV consistentes, materiales PBR calibrados, texturas con densidad coherente, colisión separada, LOD o estrategia equivalente, presupuesto documentado y medido, import reproducible, vista de cerca/medio/lejos en iluminación del juego.

Para personaje: topología de deformación, rig, piel, sockets, animaciones de locomoción/combate, root motion decidido, hitboxes y lectura visual.

### Gate 3 — derivación runtime/cinematic
Mantener `SOURCE_MASTER` y derivar, cuando aplique:
- `CINEMATIC_MASTER`: máxima información útil para render/close-up/passes;
- `RUNTIME_MASTER`: retopo/bakes/LOD/HLOD/collision/streaming/material budget preservando identidad.

El source high-poly no se considera shipping asset por defecto.

El hero asset actual conserva 410 meshes de export; no es aún una entrega optimizada ni una prueba de fidelidad hero por conteo.

## Aprobación de escena
Revisar silueta y navegación desde cámara de juego, escala humana, jerarquía de luces, exposición, variedad controlada, ausencia de ruido visual, contactos/sombras, respuesta de materiales, lectura de ataques, consistencia de estilo y accesibilidad. Comparar la misma cámara antes/después. Los concept arts Nano Banana 2/Pro orientan estilo; la aprobación final usa render del motor y recorrido real.

Para escenas con hero assets, comparar además contra el look target en misma cámara/focal cuando sea posible. Registrar residual de silueta, proporción, construcción, material, densidad, escala y legibilidad; corregir primero el residual estructural de mayor impacto.

## Asset Factory / reconstruction

Para Tier S/A, boss, personaje, vehículo, landmark o hero architecture, evaluar rutas en vez de asumir que el blockout actual debe llegar a final:

- manual Blender;
- procedural/Geometry Nodes;
- CAD;
- photogrammetry/scan;
- multiview image-to-3D;
- hybrid reconstruction + manual correction.

Tripo H3.1 multiview, Meshy multi-image y Hunyuan3D v3 fueron candidatos vivos observados el 2026-09-14 en la superficie conectada. Revalidar catálogo, inputs, coste y versión antes de cada spend. Tier S/A usa bakeoff de candidatos cuando no exista una ruta ya cualificada para esa clase.

## Presupuesto inicial, pendiente de calibrar
No fijar límites universales de triángulos como promesa. Registrar triángulos, draws, materiales, texturas/mips, memoria y coste GPU por asset y escena. EXO-006 reduce nodos y separa colisión del portal; EXO-007 decide textura/LOD a partir del host objetivo. Rechazar incrementos de detalle que empeoren legibilidad o p95 sin beneficio visible. DLSS se evalúa al final de una base estable; no sustituye optimización.

### Render economics
Tampoco fijar horas/coste de un render por resolución. Antes de render offline significativo medir `EASY`, `MEDIAN`, `WORST` con el engine/device/settings reales; estimar frames × segundos/frame y aplicar sólo entonces el rate vigente del hardware/farm. Persistir fecha/proveedor/rate. Workers reducen wall-time; no borran compute-hours.
