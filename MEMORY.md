# Memoria operativa — EXOVANT

Leer `learning/README.md` y recuperar el evento por ID antes de reutilizar una conclusión. Esta memoria dirige la recuperación; los eventos y evidencias contienen sus límites.

| Disparador | Acción aprendida | ID |
|---|---|---|
| Parece que aquí no puede ejecutarse un motor | Comprobar binario portátil y ejecutar gates nativos | LRN-EXO-20260912-GODOT |
| OpenGL muestra una imagen | Inspeccionar renderer y dispositivos; llvmpipe usa CPU | LRN-EXO-20260912-MESA |
| Necesitamos modelado detallado | Reutilizar Blender remoto y conservar .blend + script + GLB | LRN-EXO-20260912-BLENDER |
| Un asset renderiza bien | Probar colisión y recorrido con CharacterBody real | LRN-EXO-20260912-COLLISION |
| Se corrompe el guardado | Analizar JSON explícitamente y recuperar respaldo válido | LRN-EXO-20260912-SAVE |
| Un ataque alcanza a través de cobertura | Verificar raycast sobre la máscara física correcta | LRN-EXO-20260912-COVER |
| Xvfb no conecta entre comandos | Servidor y cliente deben compartir entorno de red y autenticación efímera | LRN-EXO-20260912-DISPLAY |
| Una pasada visual se oculta a sí misma | Revisar desde cámara real y medir legibilidad | LRN-EXO-20260912-ART |
| Se retoma otra sesión | Leer remoto, SHA, AGENTS y estado; reimportar sin caché | LRN-EXO-20260912-PERSISTENCE |
| Se pide progreso continuo | Distinguir activación programada de worker ejecutado | LRN-EXO-20260912-SCHEDULER |
| Se cuentan herramientas | Contar sólo eventos instrumentados; errores y retornos no verificados separados | LRN-EXO-20260912-TELEMETRY |
| Hay MCP en un repositorio | Exigir endpoint alcanzable, política y smoke actual | LRN-EXO-20260912-CAPABILITY |

Preferencias: español claro; ejecutar trabajo autorizado; máximo detalle artístico dentro de una producción verificable; no reiniciar la planificación; diseño original inspirado en cualidades de exploración, atmósfera y combate, sin copiar personajes, mapas o assets de otros juegos. Mantener doce mundos como horizonte y una región representativa como siguiente demostración.

CI: recuperar LRN-EXO-20260912-CI-BOOTSTRAP y CI-BOOTSTRAP-VERIFIED antes de cambiar descargas. Un 403 real se corrigió fijando el release oficial y verificando bytes; siete tests adversariales y CI independiente sostienen L3 del mecanismo acotado. Total actual: 14 eventos; solo uno L3.

Entradas: recuperar LRN-EXO-20260912-INPUT-BOUNDARY y INPUT-PREFERENCES. No asumir que el mapa de juego crea navegación UI ni que JSON conserva el tipo entero en comparaciones. Testear eventos físicos sintéticos atravesando UI/escena y recargar preferencias; no confundirlo con probar un mando conectado.


## EXO-006-ART-001 · isolated art checkpoint, 12 September 2026
User assigned this agent to remote Blender; gameplay stays with the parallel agent. Branch art/terra-reliquary-kit-001 and PR #1 reserve art_source. External agent acknowledgment has not been observed. Do not replace newer main STATE/PLAN with this branch snapshot blindly.

Original campaign catalog: 318 rows covered, 12 art directions, 21 category contracts, 28 Terra module briefs, all planned. Actual candidate: remote project710b21ea-a09a-4f3c-b3a4-ca446ec58bc8 revision4, editable .blend/GLB, 11 assembly roots, 12 embedded maps, 11 collision sources. Source/art evidence lives in art_source/terra_reliquary_kit/delivery.json and README.md. No runtime scripts/scenes or existing portal changed. Native import/PBR/UV and floor collision probe pass; normal Gauntlet still passes. Renders inspected; no human AAA or GPU gate is claimed.

Failures retained: first render exceeded300000ms, missing presentation UV corrected, close-up faceting corrected, podium contact corrected. Isolated Godot visual capture is blocked by Xvfb listener/display; headless engine works. Telemetry is partial. Mem queue retained without another retry.

Gameplay handoff: EXO-004-ROUTE-002 experimental input driver reached Ines then failed at custodian_0; unclassified cause, not a confirmed gameplay regression. Disabled experiment and world.patch are archived in art_source/coordination. Next gameplay owner investigates route independently.

Next art unit: inspect this candidate with the actual camera on a working display, resolve interaction clearance/texel density/LOD transition and localized wear before expanding the 28-module kit or producing character final topology. The complete twelve-world campaign remains open.
