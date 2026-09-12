# Producción visual — estándar y siguiente entrega

La ambición AAA se convierte en criterios de aceptación por asset y escena. La primera pieza de referencia será una ruta Terra del portal al archivo y ATLAS. Paleta propia: basalto húmedo, bronce envejecido, cerámica marfil y luz de tecnología biológica. El colonialismo humano de 2950 debe leerse en infraestructura reutilizada, señalética, prótesis y contraste entre cuidado y extracción.

## Kit mínimo representativo
Portal y módulos de acceso; suelo/pared/arco/escalera modular; trim sheet de bronce y cerámica; vegetación de grieta; NPC Inés con vestuario; custodio con rig y arma; avatar con una familia de arma; ATLAS con silueta legible y puntos de anticipación; rover; props de archivo; VFX de impacto, energía y polvo. El catálogo global ya existe en design: no generar cientos de variaciones antes de validar este kit.

## Definition of done de cada asset
ID y propósito, escala/pivote, fuente editable, licencia/procedencia, malla con nombres, normales y UV consistentes, materiales PBR calibrados, texturas con densidad coherente, colisión separada, LOD o estrategia equivalente, presupuesto documentado y medido, import reproducible, vista de cerca/medio/lejos en iluminación del juego. Para personaje: topología de deformación, rig, piel, sockets, animaciones de locomoción/combate, root motion decidido, hitboxes y lectura visual. El hero asset actual conserva 410 meshes de export; no es aún una entrega optimizada.

## Aprobación de escena
Revisar silueta y navegación desde cámara de juego, escala humana, jerarquía de luces, exposición, variedad controlada, ausencia de ruido visual, contactos/sombras, respuesta de materiales, lectura de ataques, consistencia de estilo y accesibilidad. Comparar la misma cámara antes/después. Los concept arts Nano Banana 2/Pro orientan estilo; la aprobación final usa render del motor y recorrido real.

## Presupuesto inicial, pendiente de calibrar
No fijar límites universales de triángulos como promesa. Registrar triángulos, draws, materiales, texturas/mips, memoria y coste GPU por asset y escena. EXO-006 reduce nodos y separa colisión del portal; EXO-007 decide textura/LOD a partir del host objetivo. Rechazar incrementos de detalle que empeoren legibilidad o p95 sin beneficio visible. DLSS se evalúa al final de una base estable; no sustituye optimización.
