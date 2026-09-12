# Incidentes y conocimiento negativo

| ID | Problema | Causa demostrada | Respuesta | Estado |
|---|---|---|---|---|
| F001 | Paso al portal bloqueado | Rampa termina demasiado pronto y deja desnivel | Geometría corregida; test CharacterBody | Resuelto en cobertura probada |
| F002 | Parser ensucia gate al recuperar JSON corrupto | API de parseo sin gestión explícita | Validación y respaldo explícitos | Resuelto en cobertura probada |
| F003 | Daño a través de paredes | Distancia/altura omiten cobertura | Raycast físico y regresión | Resuelto en cobertura probada |
| INFRA-F004 | CI no obtiene Godot | HTTP 403 de endpoint de descarga | Release oficial fijado, hash de proveedor y tests de bootstrap | Reparación publicada; ver CI |
| INFRA-F005 | Git CLI privado/push sin credencial | La shell no hereda autorización del conector | Conector autenticado para escrituras; clone público para bytes | Ruta operativa definida |
| INFRA-F006 | Lectura GLB falla UTF-8 | Conector orientado a texto | SHA de blob + clone de binarios | Ruta operativa definida |
| INFRA-F007 | Transferencia truncada | Salida demasiado grande por llamada | Bloques acotados con longitud exacta | Corregido en publicación inicial |
| INFRA-F008 | Read APIs no soportadas por fetch genérico | Endpoint fuera de capacidad del wrapper | Descubrir y usar fetch_workflow_job_logs | Ruta operativa definida |
| INFRA-F009 | Muchas tareas abiertas antes del primer checkpoint | Organización de ejecución demasiado amplia | Un escritor, una unidad, checkpoints antes de ampliar superficies | Control local; adopción futura por demostrar |

No se atribuye un fallo a contexto, RAM o GPU sin evidencia. Interrupción de llamada requiere reconciliación; no equivale automáticamente a rollback. No existe telemetría retrospectiva exhaustiva de todo el chat.
