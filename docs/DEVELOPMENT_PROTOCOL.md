# Protocolo operativo y Definition of Done

PLAN.json es el contrato de objetivos y unidades de trabajo. STATE.json conserva checkpoint, estado global y frontera activa; sus proyecciones legibles se generan con studio.py. No duplicar estados de tareas editables en Markdown. La biblia sigue siendo la autoridad creativa del catálogo; modificar alcance exige decisión explícita documentada.

## Empezar una unidad
Leer AGENTS, STATE, HANDOFF, MEMORY y PLAN. Comprobar git limpio/base; recuperar main. Ejecutar `studio.py validate`. `studio.py start TASK --run RUN` rechaza otra unidad activa, dependencias pendientes o un lock local existente; registra lecturas/hash y BOOTSTRAP con aprendizajes. El lock es local: el padre remoto verificado y el push sin force protegen el guardado entre máquinas. No confundir ambos alcances.

## Desarrollar
Escribir el criterio de aceptación que se va a demostrar. Implementar un cambio coherente; probar mecánica y casos anómalos; corregir fallos de mayor gravedad. Registrar incidentes con síntoma, mecanismo, control, evidencia y estado. Usar arte provisional cuando permita medir antes un riesgo de jugabilidad. La siguiente decisión de arte se revisa dentro del motor.

## Gate y cierre
Un test automatizado emite exit code, recibo, fecha y hash de fuentes. El cierre de tarea necesita todos sus gates, evidencia accesible y correspondencia de task_id. Los gates humanos/visuales no se sustituyen por un JSON inventado ni por tests de datos. La herramienta comprueba estructura y referencias; no puede autenticar por sí sola una revisión humana. El operador debe haber realizado esa revisión.

Done exige: comportamiento aceptado, casos anómalos relevantes probados, dependencias resueltas, ausencia de P0/P1 relacionados sin resolver, fuentes/arte editables guardados, docs y grafo actualizados, commit publicado y recuperable, proyecciones reconciliadas y siguiente acción clara. `studio.py finish` puede cerrar una ejecución como checkpoint o blocked sin declarar la tarea done. Nunca escribir done para expresar que se trabajó un rato.

## Pausas y recuperación
Ante resultado remoto ambiguo, leer antes de repetir. Ante cambio de padre remoto, reconciliar y repetir gates afectados. Tras seis intentos fallidos sobre el mismo defecto, detener parches y revisar la causa. Si falta una capacidad, usar una alternativa autorizada o registrar exactamente qué host/permiso/evidencia falta. No pedir autorización de nuevo para trabajo ordinario ya encargado. No comprar ni alquilar hardware sin presupuesto aprobado. La tarea horaria es una activación, no un proceso perpetuo.

## Publicar mediante conector
La terminal actual carece de credenciales Git de escritura; usar el conector GitHub autorizado. `prepare_publish.py` compara con HEAD y prepara JSON en bloques limitados. Releer ref remoto, crear tree sobre ese padre, crear commit y actualizar ref sin force. Guardar resultado y leer ref de vuelta. Ante binarios nuevos: calcular su Git blob SHA, subir una vez y verificar desde clone; fetch_file/fetch_blob de texto no son lectores de GLB. No imprimir base64 ni credenciales en conversación.

## Revisiones
Cada unidad: gate y aprendizaje. Cada fase: aceptación del producto y reestimación. Revisión semanal mientras haya trabajo: tareas bloqueadas, rendimiento real, coste, alcance, deuda y próximo incremento. Las fechas de PLAN son escenarios de capacidad; no hay equipo confirmado ni promesa de fecha de lanzamiento.

## WORLD DENSITY ×100 V2 / gradient-gauntlet

Para cualquier nueva selección de trabajo de mundo/asset, `docs/EXOVANT_X100_V2.md` es la capa de decisión por defecto una vez fusionada. No sustituye la unidad PLAN ni el claim Fleet: ordena qué unidad autorizable ofrece mayor ganancia marginal.

Flujo canónico:

`RESYNC → BOOTSTRAP → VECTORIZE → FLEET → INGEST_RECEIPTS → DIRECTOR_BASELINE → WORLD_GRADIENT → PORTFOLIO_SCORE → SELECT → CLAIM → FIDELITY_ROUTE → BUILD → EXPAND → ENGINE → GAUNTLET → RECEIPT → DIRECTOR_RECOMPUTE → NEXT`.

### Medición
- La completitud del mundo es media geométrica ponderada, no suma de tareas.
- Cobertura `null` = `MEASUREMENT_REQUIRED`; no inventar porcentajes para desbloquear el algoritmo.
- Cualquier dimensión crítica en cero bloquea completion aunque otros dominios estén densos.
- L0–L5 se auditan de forma independiente; no usar microdetalle para ocultar ausencia de escala regional/distrital.
- `x100_director.py` divide cada mundo en **84 células evidence-backed** (14 dimensiones × 6 células). Una célula solo sube de madurez mediante un receipt con `evidence_refs`.
- Separar siempre `strict_score_pct`, `known_evidence_geomean_pct` y `evidence_cell_coverage_pct`. Los dos últimos son diagnóstico, nunca un porcentaje de mundo terminado.

### Selección
- Recalcular pesos efectivos tras cada wave usando el déficit de cobertura.
- Enumerar gaps atómicos, filtrar por Definition of Ready y Fleet antes de score final.
- `claimed_by_other`/conflicto Fleet convierte el candidato en ineligible; no existe score que autorice pisarlo.
- El score favorece dependency unlock, player visibility, reuse, systemic yield, gameplay, image grounding y evidencia; penaliza collision risk, dependencias abiertas, slop y coste.
- El Director genera una cola de oportunidad del portfolio de doce mundos; la cola **no reserva ni reclama** trabajo. Fleet sigue siendo el único admission gate.

### Fidelity route
- Hero/Tier S-A: look target primero; image-to-3D es base candidate. Higgsfield/otros reconstruction tools aceleran formas, no reemplazan cleanup, retopo, material, collision, LOD, engine ni visual regression.
- Systemic/support: modular/procedural-first cuando genere más configuraciones creíbles por hora y geometría más controlable.
- Variaciones: solo environment/manufacturing/age/usage/damage/repair/culture/biology.

### Iteración permanente
Tras cada receipt válido:
1. actualizar el receipt X100 dentro de una ruta owned;
2. recalcular el baseline 84-cell, `WORLD_COMPLETENESS` y gradient pressure;
3. completar la family si sigue incompleta;
4. densificar ecosistema/región si existe un gap de mayor valor dentro del claim;
5. si el claim terminó, resync + Director + Fleet + siguiente gap elegible.

Solo parar por ownership conflict, decisión irreversible, coste significativo no autorizado, riesgo destructivo, bloqueo técnico demostrado o umbral objetivo alcanzado.
