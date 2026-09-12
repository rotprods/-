# Decisión de hardware y próxima frontera

## Medición de esta máquina — 12 septiembre 2026
Límite cgroup: 8 CPU equivalentes, 20 GiB de RAM. Espacio libre observado: aproximadamente 27 GiB. No hay /dev/dri ni /dev/nvidia*. Godot 4.7.2 se ejecuta. El log gráfico informa Mesa llvmpipe (LLVM 20.1.2, 256 bits). No se detectaron UnrealEditor ni Blender en PATH. Repetir `python3 tools/project_control.py probe` al cambiar de entorno.

Mesa llvmpipe es un rasterizador por software: usa CPU para shaders y geometría. Instalar librerías gráficas no proporciona una GPU física. Fuente primaria: https://docs.mesa3d.org/drivers/llvmpipe.html

## Qué ejecutar dónde
| Trabajo | Aquí | Blender remoto | Host con GPU / Mac |
|---|---|---|---|
| Código, datos, tests, builds headless de Godot | Verificado | No necesario | Opcional |
| Composición y captura sencilla del prototipo | Verificado por CPU | Render del asset verificado | Mejor para interacción y perfil real |
| Modelado con bpy y fuente editable | Generación de scripts local | Verificado | Opcional mientras la ruta remota sirva |
| Esculpido, materiales y rig profesional interactivo | No cualificado | Evaluar herramientas y límites por tarea | Recomendable con GPU y revisión artística |
| Unreal 5.8 editor, Nanite/Lumen y perfil de producción | No instalado ni validado; recursos inadecuados para aprobarlo | No hay Unreal verificado en Higgsfield | Siguiente host de cualificación |
| Validación de DLSS | No | No demostrada | GPU NVIDIA y SDK/plugin/plataforma compatibles, comprobar versión real |

Epic recomienda para desarrollo Linux 32 GB de RAM y una GPU con 8 GB o más de VRAM; su página especifica Vulkan y requisitos distintos por función. La máquina actual no satisface esa referencia. Fuente: https://dev.epicgames.com/documentation/en-us/unreal-engine/linux-development-requirements-for-unreal-engine

El inventario de game-dev-mcp-hub fechado 31 julio menciona un Mac mini M4 Pro y Unreal 5.8 instalado. Eso es evidencia histórica del inventario, no una conexión verificada hoy. Epic documenta soporte macOS y requisitos de GPU por función; su recomendación es 32 GB o más de memoria. Antes de usar ese Mac: comprobar memoria, disco, versión de macOS/Xcode, editor, proyecto, acceso y rendimiento. Fuente: https://dev.epicgames.com/documentation/en-us/unreal-engine/macos-development-requirements-for-unreal-engine

## Decisión
Seguir aquí con código, pruebas y Godot; continuar modelado por la ruta Blender remota ya demostrada. No hace falta migrar todo al Mac ahora. Para aprobar el aspecto y rendimiento de una escena Unreal de producción sí hace falta un host gráfico adecuado: el Mac disponible puede servir para probar su ruta Metal; una máquina con NVIDIA es una ruta distinta para DLSS. No comprar hardware aún basándose sólo en el prototipo. Medir primero el host disponible y una escena representativa. Compilar o ejecutar utilidades sin render de Unreal aquí sería un experimento separado, no prueba de que podamos producir todo el juego en esta VM.

## EXO-012: prueba concreta antes de migrar
1. Inventario y compatibilidad actuales con evidencia de comandos.
2. Importar portal, personaje representativo y una ruta Terra; conservar fuentes neutras.
3. Jugar la misma ruta con cámara, colisión, combate y guardado.
4. Capturar tiempos CPU/GPU p50/p95/p99, memoria, resolución, preset, carga y stutter sobre build; anotar duración y escenas.
5. Evaluar calidad visual, velocidad de iteración y esfuerzo de portado. Elegir motor con esos resultados. No prometer 60 FPS hasta medirlos en hardware objetivo.
