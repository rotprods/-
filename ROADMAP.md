# Fases, checkpoints y calendario

> Proyección de PLAN.json. Escenarios, no fechas comprometidas.

| Fase | Objetivo | Salida |
|---|---|---|
| P0 Infraestructura reproducible | G-OPS | Clon limpio y hashes; CI verde; Contrato trazable; Superficies reconciliadas |
| P1 Jugabilidad Terra | G-PLAY | Ruta completa; Control y cámara; Recuperación tras muerte |
| P2 Combate y arte representativo | G-ART | Portal de producción; Kit Terra; Personaje y ATLAS legibles |
| P3 Decisión de motor y vertical slice | G-TECH | Escena equivalente medida; 30–45 minutos completos; Playtests externos |
| P4 Campaña por capítulos | G-WORLD | Viaje persistente; Planetas uno por uno; Consecuencias de campaña |
| P5 Cualificación y lanzamiento | G-RELEASE | Plataformas y rendimiento; Licencias y localización; Candidato de lanzamiento |

| Unidad | Fase | Dependencias | Estado |
|---|---|---|---|
| INFRA-005 Base operativa recuperable y proyecciones conectadas | P0 |  | in_progress |
| EXO-004 Complete playability route, input and guidance | P1 |  | planned |
| EXO-005 Player combat and animation pass | P2 | EXO-004 | planned |
| EXO-006 Portal asset production pass | P2 |  | planned |
| EXO-007 Terra art direction proof | P2 | EXO-004, EXO-006 | planned |
| EXO-008 ATLAS authored encounter | P2 | EXO-005, EXO-007 | planned |
| EXO-009 Archive route alternatives | P2 | EXO-004 | planned |
| EXO-010 Ecology and consequences | P2 | EXO-009 | planned |
| EXO-011 Rover physics and accessibility | P2 | EXO-004 | planned |
| EXO-012 Production engine decision | P3 | EXO-006, EXO-007 | planned |
| EXO-013 30–45 minute Terra slice | P3 | EXO-005, EXO-006, EXO-007, EXO-008, EXO-009, EXO-010, EXO-011, EXO-012 | planned |
| EXO-014 Planetary travel framework | P4 | EXO-013 | planned |
| EXO-015 Ares IX chapter | P4 | EXO-014 | planned |
| EXO-016 Remaining Milky Way chapters | P4 | EXO-015 | planned |
| EXO-017 Andromeda chapters | P4 | EXO-016 | planned |
| EXO-018 Extragalactic final act | P4 | EXO-017 | planned |
| EXO-019 Release qualification | P5 | EXO-018 | planned |

## Capacidad del slice

Base heredada: 3200 horas-persona; no estimación de la campaña completa.

| Personas equivalentes | Horas productivas/semana | Semanas ideales |
|---|---|---|
| 1 | 30 | 106.7 |
| 2 | 60 | 53.3 |
| 4 | 120 | 26.7 |

Estos escenarios omiten esperas, dependencias no paralelizables y vacaciones. No hay equipo contratado confirmado. Reestimar con productividad observada tras EXO-007/012. Cada fase requiere sus gates antes de iniciar la expansión siguiente.
