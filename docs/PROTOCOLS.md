# Protocolos aplicados y alcance

Recuperados de rotprods/rot.knowledge el 12 septiembre 2026, head observado e8be6757b80eeab243c3f7000e343be076bd8642:
- APRENDE_MASTER.md: b053a912ab433f46fa66a5350a5a3c21c1377433
- COS_GRAPH_ENGINE_V2_MASTER.md: 02f07476d2db5a7bd4ef203fa3fb6d8af5b49414
- GRAPHIFY_MASTER.md: 2be2087021f38e82ea3a729596f32c767648fd7a
- GAUNTLET_LOOP_MASTER.md: 7e3fa190e980936a51858059c014e6cc192e091e
- learning-event.schema.json: 434e4298dcc8255ff49b2af9f8a14ade212e8f8e
- runtime/aprende_runtime.py: fc473bc394d7a977bcd0e34a6129072a3530267b (copia acotada del runtime del usuario en tools, sin cambios).

También se leyó APRENDE_ENFORCEMENT: BOOTSTRAP, exactamente un CLOSE y aprendizaje separado de recibos. La primera ruta consultada no existía; se resolvió el archivo correcto aprende_lifecycle.py (blob 336b6a1500a66e2799b50bdf2aae5800e8326e08), copiado sin cambios en tools. Se usa su SessionLifecycle canónico; no se instala un runtime global.

Skill continuous-learning-v2, metadata 2.1.0, affaan-m/ECC, skills/continuous-learning-v2/SKILL.md, blob 397b3d334dd1fdf5d7648dd619b6a744cd4734a5. Aplicación: aprendizajes atómicos con trigger, acción, evidencia y scope de proyecto. No se instalaron hooks Claude ni un observador de fondo en este entorno; no es lícito afirmar cobertura universal de llamadas. Promoción global requiere evidencia en varios proyectos; no se hace en esta ola.

COS/CGVE2 se implementa como cuatro planos sobre archivos existentes. Graphify produce un grafo tipado comprobable. El mapeo de dimensiones del estudio permanece en su repositorio; no se inventa ni se fusiona con otros proyectos. Las leyes personales no recuperadas no se reemplazan por reglas inventadas con su nombre.

## EXOVANT-X100 V2 — protocolo local de densidad/selección

Creado para EXOVANT 2950 como evolución explícita del mandato WORLD DENSITY ×100 del usuario. Fuente candidata: `docs/EXOVANT_X100_V2.md`; parámetros ejecutables: `ops/x100/config.json`; North Star: `ops/x100/GOAL.json`.

Relación de autoridad:
- **Fleet Coordination** decide ownership/claim/epoch/rutas/assets/projects y bloquea colisiones.
- **EXOVANT-X100 V2** mide cobertura, calcula presión de bottleneck, ordena gaps elegibles, define expansión de families y el fidelity route.
- **Graphify/COS** representa relaciones y provenance; X100 aporta una proyección vectorial espacial-semántica separada, no una segunda autoridad ni un nuevo tipo de nodo canónico.
- **Gauntlet** valida implementación/evidencia; un score X100 alto nunca equivale a PASS.
- **APRENDE** conserva aprendizajes demostrados; X100 no promueve heurísticas sin evidencia.

Vectorización: `ops/x100/x100_spatial.py` genera 64 dimensiones por claim/rama a partir de mundo, escala L0–L5, dominio, status, bounds físicos explícitos y un tail semántico determinista. Coordenadas desconocidas mantienen `spatial_known=0`; inferencias desde el nombre de rama se etiquetan y no son canon ni ownership.

Optimización: `ops/x100/x100_control.py` implementa media geométrica ponderada, pesos adaptativos por déficit y ranking con hard fence de claims ajenos. Configuración exacta en `ops/x100/config.json`; tests en `ops/x100/tests/test_x100.py`.

Fidelity: Tier S/A o familias de identidad fuerte usan por defecto LOOK_LOCK → target visual → image-to-3D base → causality/cleanup/retopo → material → LOD/collision → engine → visual regression. Higgsfield 3D Jutsu puede acelerar la reconstrucción cuando aporta valor; un raw AI mesh nunca se clasifica final.

Adopción: tras merge a `main`, se aplica a nuevas selecciones de trabajo world/asset y en el siguiente resync normal de productores existentes. No crea watchers, no roba claims, no obliga a reabrir trabajo ya aceptado y no se afirma enforcement en ramas que todavía no hayan recuperado el main actualizado.
