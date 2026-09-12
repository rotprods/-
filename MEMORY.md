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
