# EXOVANT — coordinación de producción paralela

La campaña de doce mundos sigue siendo la misión. Este harness reduce conflictos entre productores; no crea trabajadores permanentes ni certifica arte AAAA+.

## Autoridad y superficies

- `main:ops/fleet/registry.json` es el registro ejecutable de reservas publicadas. Leer el main actual antes de reservar y publicar. Un archivo local es una propuesta hasta confirmar el ref remoto.
- [Issue #7](https://github.com/rotprods/-/issues/7) es el hilo compartido de avisos, correcciones y acuses. Se conserva el hilo abierto por otra célula, sin crear otro registro social competidor.
- Las ramas, claims originales y observaciones del proveedor aportan evidencia. Los snapshots fechados son históricos; no sustituyen una lectura actual.
- El catálogo `design/EXOVANT_DATA.json` conserva los IDs de los doce mundos. Parámetros planetarios propuestos no se convierten en canon al crear geometría.
- `studio.py` reserva un escritor por checkout. **No es un lock distribuido**. El PLAN global admite una unidad integradora activa; los ámbitos de arte se coordinan mediante el registro de flota.

## Reservas verificables

Cada reserva contiene ID único, owner declarado, rama, epoch, rutas, ámbitos semánticos, proyectos remotos y IDs exactos de assets. Los productores importados comienzan `reserved`: protege el trabajo observado, pero no significa acuse del owner ni worker vivo. `UNCONFIRMED@...` es un marcador de identidad desconocida; no es un agente inventado. Las rutas inferidas y propuestas se señalan explícitamente.

`active` exige acuse del owner y epoch vigente. `blocked` conserva la reserva: un bloqueo o heartbeat antiguo no permite apropiarse de su trabajo. `released` y `abandoned` permanecen como tombstones; no bloquean otra reserva, pero sus IDs no se reutilizan. No hay caducidad que robe automáticamente una escena.

El validador rechaza colisiones de rutas, ámbitos semánticos jerárquicos, proyectos Blender, IDs de assets y ramas. Normaliza `SYLVA PRIME`, `sylva_prime` y `sylva`, entre otros alias canónicos. Las rutas son archivos exactos o directorios acabados en `/`, sin comodines. `art_source/ares/` no cubre `art_source/ares2/`.

El vocabulario semántico debe acordarse antes de reservar: usar `art/macro-foundation`, `art/structural-root-kit`, `art/environment`, `art/proxy-families`, etc. `art` cubre todos sus descendientes. El programa detecta solapamientos declarados; no puede deducir que dos descripciones artísticas distintas significan lo mismo. Esa revisión sigue siendo responsabilidad del integrador.

## Flujo por unidad

1. Recuperar main vigente, AGENTS, STATE, PLAN, HANDOFF, memoria y aprendizajes. Examinar ramas, PRs y el issue #7. Un PR cerrado solo libera un frente cuando existe abandono explícito; un merge no autoriza borrar o reutilizar su escena.
2. El productor comunica en el PR/issue su owner real, claim, rutas, inclusiones/exclusiones, IDs de assets y asociación rama↔proyecto. Si cambia el ámbito, proponer una reserva nueva y cerrar la anterior con evidencia; nunca editarla a escondidas.
3. El integrador aplica la transición sobre una copia actual del registro, comprueba colisiones, prepara commit contra el padre leído y mueve el ref **sin force**. Otro commit concurrente obliga a releer y reconciliar; no se reenvía el mismo overwrite. Verificar el readback.
4. El integrador registra el acuse real. El productor recupera ese main y comprueba el digest y su epoch. El acuse es identidad cooperativa; GitHub compartido no autentica agentes individuales.
5. Ejecutar una unidad acotada y preservar fuente Blender, generadores, semilla/parámetros, GLB y evidencia. Antes de cada mutación remota: lectura fresca del proyecto, revisión y scene sequence exactos, ninguna operación pendiente. Si hay operación activa, reconciliar ese ID antes de enviar otra. Un ID no autoriza otra máquina o servicio.
6. El productor entrega un diff de su ámbito y un handoff; el integrador reconcilia pruebas, manifiesto global, estado, proyecciones y grafo. Cerrar la sesión con `studio.py finish` y resultado honesto. Una entrega artística continúa como candidato hasta satisfacer sus gates humanos y de hardware.

### Evitar conflictos con la continuidad global

El integrador ejecuta `studio.py start TASK --run RUN` y `finish` en su checkout, y mantiene el estado global. Los productores con versiones anteriores de `studio.py` pueden tener cambios globales de lifecycle en sus ramas: **son propuestas de integración, nunca un reemplazo del STATE actual**. Preservarlas en su handoff; no copiar todo el árbol al main. Antes de publicar una entrega de arte, preparar un checkout limpio con solo los cambios del ámbito. `guard-git` debe ejecutarse allí. No borrar cambios ajenos para conseguir que el gate pase.

Excepción de proyección generada: cada productor puede ejecutar `python3 tools/project_control.py refresh` en su rama para incluir los hashes de sus archivos y evitar un CI rojo por manifiesto viejo. `guard-git` acepta ese `MANIFEST.json` únicamente si coincide exactamente con los archivos actuales y SHA256 calculados; sigue rechazando cualquier otro cambio global fuera de ámbito. El manifiesto no se convierte en una ruta de propiedad libre. Al integrar varios PR, regenerarlo sobre el árbol combinado en vez de escoger a mano el manifiesto de un productor.

La migración de los productores existentes necesita su acuse. El guard no se inserta en un proceso remoto que ya estaba ejecutándose. No se afirma enforcement universal ni adopción de todos los agentes.

## CLI

No requiere red, GPU ni dependencias Python externas:

```sh
python3 tools/fleet_control.py validate
python3 tools/fleet_control.py digest
python3 tools/fleet_control.py transition --request .tools/reservation-request.json
python3 tools/fleet_control.py guard-git --base COMMIT_MAIN_LEIDO --request .tools/guard-request.json
python3 tools/fleet_control.py delivery --root RUTA_CHECKOUT_ASSETS --request RUTA_RECIBO_ENTREGA.json
```

Transición de acuse (la escribe el integrador después del acuse observable, no en nombre de un owner silencioso):

```json
{
  "action": "ack",
  "expected_digest": "SHA256_DEL_REGISTRO_ACTUAL",
  "claim_id": "CLM-SYLVA-MACRO-001",
  "owner": "AGENT-SYLVA-MACRO-01",
  "epoch": 1,
  "evidence_ref": "URL_DEL_COMENTARIO_DE_ACUSE"
}
```

`reserve` recibe `expected_digest` y `claim` completo con `status: reserved`, `epoch: 1` y sin ack. `release`/`abandon` reciben claim, owner, epoch, evidencia y `remote_observations` por cada projectId propio. Cada observación debe corresponder exactamente a su clave, estar fechada con zona horaria, tener menos de cinco minutos, revisión/sequence y `active_operation_id: null`.

`guard-git` recibe `claim_id`, `owner`, `epoch`, `expected_digest` y, opcionalmente, `remote`, `expected_revision`, `expected_scene_sequence`. Deriva la rama real y TODOS los cambios contra el padre, incluidas eliminaciones, ambos extremos de renombrados y archivos nuevos. Rechaza escapes de ruta y symlinks hacia otro ámbito. El modo `guard` de bajo nivel acepta listas explícitas y no garantiza que el llamante haya enumerado todas las rutas.

Las transacciones locales usan un lock de directorio y reemplazo atómico. Eso solo serializa procesos del mismo filesystem. La publicación Git normal de commits hermanos impide que gane el segundo overwrite: se prueba con un repositorio bare real. La comprobación es cooperativa; una operación que omita el wrapper no queda mágicamente controlada. Releer main inmediatamente antes de publicar continúa siendo obligatorio.

## Gates de entrega 3D

`delivery` verifica recuperación local de `.blend` y GLB con SHA256, cabecera GLB, presencia de mallas y ausencia de recursos externos, más un recibo nativo ligado al hash exacto del GLB. Formato:

```json
{
  "blend": {"path": "art_source/mi_kit/source.blend", "sha256": "HASH"},
  "glb": {"path": "art_source/mi_kit/export.glb", "sha256": "HASH"},
  "native_receipt": {"path": "art_source/mi_kit/native-receipt.json", "sha256": "HASH"}
}
```

El recibo nativo incluye `passed`, `artifact_sha256` del GLB, `executed_at`, `engine` y `evidence_refs` locales existentes. Los tests o logs se conservan con el mismo commit. Es una comprobación de transporte y trazabilidad; no valida por sí sola editabilidad en Blender, topología, UV, rig, colisiones ni que un humano haya jugado. Reabrir la fuente en Blender, importar en motor y ejecutar los gates relevantes sigue siendo necesario. Render o URL de proveedor no sustituyen fuente recuperada. La revisión humana y el rendimiento en hardware objetivo son gates separados.

## Repartos que requieren acuse

- **Ares:** PR #2 abandonado, conservar tombstone. Agente-02 mantiene artefactos remotos; falta checkpoint y declaración formal. No reactivar el primer frente.
- **Sylva:** macro conserva composición regional, rutas, centerlines, sockets y proxies diagnósticos. Root-kit fabrica generadores/módulos reutilizables, pivotes, dimensiones y material IDs. Los proxies del macro no se promocionan en paralelo a módulos finales duplicados. Mantener ambas escenas y fuentes. Requiere acuse de ambos.
- **Khepri/Nacre:** macro/fundación está reservado; no confundirlo con ownership de todo el arte final. Nuevas especialidades deben acordar rutas e IDs concretos.
- **Terra:** el kit de PR #1 es candidato delimitado, no entrega de todo Terra. La partida EXO-004 permanece en el frente de gameplay.
- **Vanta/Elysium/Ares-02:** la identidad individual del owner debe confirmarse; no derivarla del login compartido.
- **Origin:** ya reservado en issue #14 y claim `CLM-ORIGIN-WORLD-001`; primera célula interna `CLM-ORIGIN-MEGA-ATRIO-001`. No ofrecerlo como libre basándose en el primer snapshot.

Khepri envió el primer acuse de productor en issue #7, comentario `5648289971`, con rutas, IDs y proyecto. El registro lo conserva como `active`; sus bloqueos de recuperación binaria/revisión artística continúan pendientes. Los demás acuses no se presuponen.

## Capacidad y fallos

El probe de esta sesión observó cuota equivalente a 8 CPU, límite de 20 GiB y ausencia de dispositivos GPU expuestos. Godot portátil funciona para pruebas headless. Los remotos Blender son escenas independientes con guard de operación; su existencia no prueba capacidad ilimitada ni un proceso permanente. No se compra GPU ni se inicia otro servicio para este harness.

Si hay rate limit, conservar operación/cola y aplicar backoff; no reintentos rápidos. Mem es un espejo secundario pendiente y no bloquea arte ni código. CI sin runner/pasos ejecutados es ENV_BLOCKED, no fallo del juego ni permiso para un rerun ciego. La telemetría declara cobertura parcial de llamadas instrumentadas.

## Ubicación de assets y aplicaciones

Contrato MR-EXO-001 en PLAN; distingue reglas definidas de mecanismos ejecutados. Cumplimiento externo parcial, no enforcement universal.

### Dónde vive cada entrega

- GitHub `rotprods/-`: autoridad de código, generadores, manifiestos, claims y recibos. Respetar las rutas existentes `art_source/<kit>/`, `art_source/worlds/<world>/` y `production/...`; no renombrar mundos de otros owners para uniformar carpetas.
- Fuente artística en trabajo: proyecto Blender remoto identificado por claim + project ID + revisión. Es fuente de producción, pero no respaldo independiente.
- Checkpoint binario: `.blend`, GLB, texturas y dependencias en su rama Git cuando el transporte lo soporte, como Terra; en otro caso bundle persistente en la carpeta Drive EXOVANT existente con ID estable, hashes y recibo versionado en Git. No activar LFS nuevo ni almacenamiento de pago sin decisión aplicable.
- Runtime: solamente exports aceptados en las rutas de assets del juego; no importar toda la producción ni depender de Drive/Higgsfield en ejecución.
- Scratch/descargas locales/cachés: copias de trabajo, nunca única persistencia.
- Un paquete debe ser independiente del proveedor: fuente reabierta en Blender, GLB importado, recursos externos incluidos/resueltos, licencias y atribuciones registradas para material de terceros. Hash y tamaño no prueban editabilidad ni calidad.
- Nombre recomendado para nuevos bundles: `EXOVANT_<claim>_<revision>_<source-sha>.zip`; conservar nombres/IDs existentes cuando ya son estables. No usar enlaces firmados expirables como localizador duradero.
- Recibo mínimo: asset IDs, owner/claim/epoch, commit fuente, proyecto/revisión, archivo/ruta o Drive ID, SHA256 y bytes por archivo, versión Blender/exportador/motor, dependencias/licencias, pruebas y resultado, fecha, limitaciones. Cada owner entrega; el integrador revisa el checkpoint sin reconstruir producción por iniciativa propia.

### Función concreta de las superficies

| Superficie | Función en EXOVANT | Estado/condición |
|---|---|---|
| GitHub | Código, PR, manifests, recibos, learning/hub y releases del juego | Autoridad existente |
| Linear | Tareas/dependencias y bloqueos por IDs existentes | Proyección; enlazar SHA, no duplicar backlog |
| Google Drive | Bundles duraderos, dossier y previews por checkpoint | Proyección/backup; descarga y hash antes de declarar restore |
| rot.knowledge | Índice a aprendizajes/protocolos canónicos | No duplicar eventos del juego |
| game-dev-mcp-hub | Políticas, adaptadores y rutas autorizadas de herramientas | Código de MCP no equivale a servicio conectado |
| Higgsfield/Blender remoto | Modelado con escenas exclusivas, export, render de revisión | Reconciliar operación/revisión antes de mutar; costes nuevos requieren presupuesto |
| Godot + Mesa local | Runtime prototipo, importación, física y captura CPU | Capacidad demostrada; no benchmark GPU |
| Mac + Blender | Edición interactiva, Metal, revisión y medición gráfica | Pendiente cualificación real |
| Unreal | Evaluación de motor en escena equivalente EXO-012 | Candidato; no migración automática ni MCP en cuarentena |
| Mem | Enlace de recuperación mediante nota estable | Espejo opcional, rate limit pendiente, sin ráfagas |
| Adobe | Retoque y preparación de texturas/decals cuando haya tarea | Opcional, pipeline aún no cualificado |
| Figma | UI/HUD, flujos y tokens si se admite trabajo de interfaz | Opcional; export versionado y validación en motor |
| Canva | Dossiers y presentaciones de revisión | Opcional; no autoridad de modelos ni backlog |
| Notion/Airtable | Vista de revisión si aporta necesidad concreta | Inactivos para este flujo; no segundo STATE/catálogo editable |
| Todoist/TickTick/Structured/Calendar/24-7 | Compromisos humanos concretos de pruebas | Bajo demanda, no copiar cada tarea de Linear |
| Slack/email | Comunicación solicitada a personas | No envío automático ni campañas por esta autorización |
| PostHog | Analítica de pruebas futuras, con diseño explícito | No dependencia del runtime offline ni telemetría añadida aquí |
| n8n/OpenClaw/Ollama/Qdrant | Automatización o búsqueda local si resuelve bloqueo medido | No instalar como paso obligatorio; respetar host/políticas |
| HubSpot/Klaviyo/Resend/Stripe | Comercialización futura | Fuera de producción técnica actual; sin campañas/cobros |
| Supabase/Vercel/Sites | Portal/build distribution si hay producto web aprobado | No necesarios para fabricar/ejecutar assets offline |
| Hugging Face/buscadores | Investigación de recursos y licencias por tarea | No descarga masiva ni entrenamiento/cómputo de pago |

Esta matriz asigna funciones; no certifica conexión ni uso de todas las aplicaciones. Las demás apps quedan sin activar hasta tener tarea, owner, permisos, entrada/salida y beneficio verificable. Más conectores no implica mejor producción. Las credenciales permanecen en los mecanismos de autenticación, nunca en manifests o prompts.

### Integridad, adopción y coste

Antes de un push, refrescar y comprobar el manifiesto en el checkout exacto, revisar el diff y guard de scope. Al combinar ramas, regenerar sobre el árbol combinado; no elegir el manifiesto de un productor por conveniencia. No debilitar ni regenerar el manifest en CI para hacer verde una entrega inconsistente.

Un fallo de continuidad no prueba fallo de geometría; tampoco permite afirmar que Godot pasó cuando su paso fue omitido. Detener nuevos reintentos del mismo problema sin un cambio causal verificado. Después de seis fallos, revisar mecanismo/arquitectura antes de seguir publicando.

El informe por entrega debe separar contrato declarado, prueba ejecutada y adopción observada. No deducir todos los agentes activos/cumplidores desde ramas o JSON. Un conflicto de escritor congela solamente el ámbito afectado hasta reconciliar; no operar proyectos de otros owners. Una sesión sin acuse no obtiene autoridad por antigüedad.

La próxima unidad integradora es una entrega corregida y recuperada, no conectar cuarenta aplicaciones. Usar issue #7 para deltas y acuses ordinarios; Linear/Drive por checkpoint. Mantener automatización pausada y telemetría con cobertura parcial. La evaluación de hardware puede comenzar con Terra aislada; la migración completa de producción exige el inventario y los respaldos aceptados.
