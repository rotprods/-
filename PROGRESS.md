# Progreso comprobable

| Hito | Resultado | Límite |
|---|---|---|
| Preproducción | Biblia, catálogo y planificación de 12 mundos, 84 misiones y 318 filas de assets | Propuestas, no contenido implementado |
| Blender remoto | Portal editable .blend, GLB, script, render y una animación | 142.916 triángulos indexados del export completo; optimización pendiente |
| Godot local | Proyecto 3D nativo, interacción, combate, puzzle, NPC, ATLAS y guardado | Prototipo; no campaña completa ni arte AAA |
| Gauntlet 003 | 26 comprobaciones de estado + 19 de integración; import y smoke | Setup controlado, no partida humana completa |
| Mesa | Captura real del runtime mediante llvmpipe | CPU; no perfil GPU |
| Recuperación anterior | Extracción sin caché y repetición de gates | Ahora se migra la autoridad a GitHub |
| Persistencia 004 | Contrato de agentes, memoria, arquitectura, grafo, aprendizajes, control de integridad y telemetría | Estado final y recibos en STATE y evidence; no enforcement universal |

Defectos resueltos: rampa con escalón que bloqueaba al personaje; parser de JSON corrupto que ensuciaba el gate; daño a través de cobertura; problemas de inferencia de tipos; exposición y barras de vida ilegibles. Los casos ejecutables permanecen en tests.

Siguiente incremento de producto: EXO-004, recorrido completo sin teletransportes y observación de fricción, después controles y orientación. Mantener este hito de persistencia separado de una mejora de jugabilidad: esta ola no añade mundos ni ataques.

## Infraestructura 005 — reparación de descarga

El fallo de GitHub Actions se reprodujo localmente: HTTP 403 del endpoint de descarga. La URL oficial de release 4.7.2 permitió descargar e instalar con hashes coincidentes. Siete pruebas adicionales cubren corrupción, truncado, tamaño y preservación del binario existente. El clon remoto conservó íntegros los 108 archivos y pasó los cuatro gates nativos. CI corregido pendiente de ejecución remota.

## INFRA-005 · contrato y herramientas

Añadidos PLAN con 6 objetivos, 6 fases, 17 unidades y 10 gates; GOALS/ROADMAP generados; control de escritor local y cierre con evidencia; graph drift check; auditoría GLB; paquete reproducible y restore remoto; telemetry opt-in de conectores; pruebas adversariales adicionales. Linear refleja seis hitos y diecisiete tareas. Integraciones documentales publicadas en game-dev-mcp-hub y rot.knowledge. Mem devolvió rate limit en el primer intento; no se declara sincronizado. Cierre global de infraestructura todavía en cualificación.

## Verificación externa de INFRA-005

Commit d8fdc7c: CI success, clon limpio con integridad/control/native PASS. Drive: snapshot descargado de nuevo, SHA256 idéntico y 147 entradas del manifiesto verificadas. Contratos de Linear leídos: 6 hitos, 17 tareas. Índices de estudio y aprendizaje leídos tras escritura. Mem sigue pendiente por rate limit tras dos intentos; queda en cola. La primera ejecución programada aún no está demostrada.

## EXO-004-INPUT-001 · Controles y jugabilidad inicial

Implementados movimiento y cámara analógicos, botones de combate, navegación/foco de menús, remapeo persistente y ayudas dinámicas. Corregidos el rechazo de preferencias JSON válidas, la comparación de botones tras recarga y la documentación equivocada de guardia/esquiva. 34 tests Python + 26 estado + 19 integración + 33 input pasan; cinco gates nativos. Recorrido real por inputs desde spawn hasta Inés, sin teletransporte ni avance de estado artificial. UI renderizada en Mesa a 1280×720 y comprobada dentro del viewport; no aprobación artística AAA. EXO-004 permanece en revisión: falta la ruta completa y prueba humana/con mando físico. Mem volvió a limitar solicitudes; cola conserva el tercer intento sin insistir.

## INFRA-005-FLEET-001 · Producción paralela y reparación de main

Implementado registro de 13 frentes productores, un tombstone Ares y la unidad integradora; normalización de mundos, conflictos de rutas/ámbitos/proyectos/asset IDs/ramas, ACK y fencing por epoch, guard de cambios Git y recibos de entrega. 41 casos adversariales incluyen dos procesos concurrentes y Git bare real; encontrado y corregido reuse de observación remota al liberar varios proyectos. Primer ACK real de Khepri incorporado. Origin reservado, no libre.

Main avanzó durante el trabajo de 4c2fa044 a 196ef814 con solo AGENTS modificado y MANIFEST viejo. Reproducido mismatch de hash, conservado el preflight mediante merge de tres vías y regenerada integridad. El guard admite manifiesto regenerado EXACTO en ramas artísticas, sin dar propiedad de STATE/herramientas globales. 75 tests Python y 78 nativos aprobados con recibos finales; CI del commit final se verifica después de publicar. No se modifica geometría ni gameplay en esta unidad.

## INFRA-005-DELIVERY-003
Incremento del control de entrega: recorrido completo de chunks GLB y lista explícita de evidencias. Seis casos reproducen la aceptación incorrecta en f78bfdc8; 48 tests de flota pasan tras el fix. Sin geometría nueva ni cambios de runtime. ADOPTION-002 no está recuperado. Fuente de evidencia: evidence/delivery-container-regression.json; gates actuales en evidence/gates/INFRA-005-*.json.

## INFRA-005-LEARNING-004
Corrección del usuario convertida en evento L2 y preflight AGENTS. Objetivo de remediación y criterios por problema dentro de PLAN existente. Difusión por hilo #7; adopción externa pendiente, sin nuevos agentes ni watchers.

VISUAL-005: graphical Godot capture qualified here after resolving absolute xkbcomp dependency and importing cold-clone assets. See evidence/visual-display-qualified.json and visual-display-runbook.md. CPU llvmpipe only; existing capture repositions player. Capture exit code can hide script errors: inspect log and fresh PNG.

MR-EXO-001: contrato de preparación de migración en PLAN y ubicación de assets/aplicaciones en docs/FLEET_COORDINATION.md. Cumplimiento de flota parcial; respaldos de mundos y manifest drift pendientes. No nuevos agentes/automatización; siguiente unidad es una entrega admitida recuperable y CI correcto, no conexión masiva de apps.

REMEDIATION-007: cinco ACKs de productores reconciliados con evidencia; seis productores active contando Khepri. Restricción Sylva de escritor único sigue vigente. Corregido rechazo de production/manifests/<world>/ y production/receipts/<world>/ con tres pruebas adversariales (85 total); qualify control/graph/asset/native PASS. Aurora reparación CI canary 570a61f7d447708c149b0aa6b3fa9bad8739d000, run 34722208068 SUCCESS. Publicaciones restantes se registran en issue #7 con SHA/readback. PR1 conflictos globales, Vanta workflow temporal activo: no sobrescritos. Backups mundiales, capture_visual false-positive y hardware siguen abiertos.
