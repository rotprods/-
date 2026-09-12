# Registro de herramientas y resultados

`telemetry/tool_calls.jsonl` registra las llamadas del runner que están instrumentadas: ID, run, herramienta, fecha, duración, estado técnico, resultado de tarea cuando se verifica y alcance. No registra argumentos, cookies, tokens, contenido de mensajes ni URLs firmadas. `tools/tool_ledger.py` permite envolver comandos locales sin guardar sus argumentos. Para conectores, el orquestador debe añadir metadatos de su llamada y reconciliar el resultado con lectura posterior.

No existe un hook universal instalado en Work Mode para todas las aplicaciones. Los datos anteriores a la instrumentación son cobertura parcial. No se infiere que una herramienta no se usó porque no aparece. `returned` significa que devolvió una respuesta, no que el objetivo se logró. Separar error del proveedor, timeout, retorno sin verificar y éxito comprobado. El resumen cuenta filas reales por herramienta y resultado; la tasa de éxito sólo utiliza resultados verificados.

Aprendizaje por fallo: conservar clase de error, precondiciones, alternativa que funcionó y control de recurrencia. Fallos conocidos: apt restringido por cambio de grupos; sockets UNIX restringidos; URL de proxy Git con ruta incorrecta; búsqueda vacía; rutas históricas 404. No intentar superar controles de acceso; las rutas alternativas deben estar autorizadas y servir a la misma tarea.
