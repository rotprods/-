# EXOVANT 2950 · catálogo de producción artística

Este frente convierte las **318 filas canónicas** de `design/EXOVANT_DATA.json` en briefs de producción. Cubre los doce mundos, mantiene sus nombres y funciones, y conserva cantidades y unidades. **Todos estos briefs están `planned`; el catálogo no afirma modelos terminados, hiperrealismo aprobado ni integración jugable.** Los candidatos de Blender conservan sus archivos y recibos propios. Este desglose no sustituye `_project_intelligence/STATE.json` ni `_project_intelligence/PLAN.json`.

El SHA base de diseño es `4c2fa044080004609ea6df45f34b2a784536507a`. La biblia y el catálogo creativo contienen estados históricos de infraestructura; aquí se usan para canon artístico y alcance, nunca como prueba del motor o hardware vigente.

## Archivos y autoridad

| Archivo | Contenido | Qué demuestra |
|---|---|---|
| `ASSET_MANIFEST.json` | 318 IDs originales; función, silueta, materialidad, escala propuesta, prioridad, dependencias y perfil de entrega | Cobertura de diseño por fila; no aceptación de piezas |
| `CATEGORY_PROFILES.json` | 21 contratos de fuente, exportación, rig, LOD, colisión y revisión | Requisitos observables por disciplina |
| `WORLD_ART_DIRECTION.json` | 12 gramáticas de arquitectura, desgaste, luz, vestuario, custodio y cielo; 240 nombres de utilería planetaria | Identidades visuales diferenciadas y coherentes con canon |
| `TERRA_MODULES.json` | 28 briefs de piezas, 17 de prioridad inicial, con dimensiones y funciones | Desglose reutilizable del kit de riego/archivo/reliquario |
| `validate_catalog.py` | Comprobación offline de cobertura, hashes, referencias y dependencias | Detecta drift o claims de entrega indebidos en este snapshot |
| `COVERAGE_EVIDENCE.json` | Resultado y hashes de la comprobación | Evidencia limitada al catálogo y sus contratos |

Una fila puede ser una región, veinte props, una biblioteca de animación o un sistema. No se suman unidades heterogéneas. Los 600 módulos de entorno objetivo, 1.420 clips y demás cantidades de la visión siguen siendo objetivos. El desglose de familias en nombres o cuotas no equivale al diseño final multivista de cada miembro.

## Dirección de calidad

La calidad solicitada se evalúa por construcción creíble, proporción, respuesta a la luz, detalle material causal, animación y lectura en juego. “AAAA+” describe la ambición del usuario; no es una certificación técnica. El criterio de aceptación necesita una revisión humana del conjunto y rendimiento medido en el hardware objetivo.

Tres escalas de detalle se separan en la fuente:

1. **Volumen:** masa portante, apoyos, huecos, carga, agarres y espacio de mantenimiento. La silueta debe funcionar con material gris y cámara de juego.
2. **Construcción:** juntas, bridas, bisagras, paneles de reparación, borde de presión y montaje. Toda pieza tiene un motivo y la repetida comparte geometría/material cuando conviene.
3. **Superficie:** grano, poro, esmalte, desgaste por agarre, polvo, oxidación y humedad. Se resuelve con UV, mapas y bake cuando el detalle no mejora silueta. Más polígonos no sustituyen este trabajo.

En Terra, la humedad se concentra en zócalos, juntas y drenaje; el bronce pulido aparece en controles, y el depósito opaco bajo fugas. La cerámica conserva espesor, bordes y reparaciones. El concreto muestra árido y estratificación a escala, evitando ruido uniforme. Comparar una muestra seca y otra húmeda bajo la misma iluminación antes de extender materiales al kit.

Las luces de refugio son ámbar, memoria cian pálido, hostilidad bermellón y autoridad blanco frío. Posición, forma y sonido repiten el significado. Los doce mundos mantienen una dominante propia sin recolorear toda la escena con el estado de combate.

## Primera unidad de Blender: cámara de riego Terra

La escena de producción propuesta une estación de tres controles, manifold, canal trazable, muro de servicio, contrafuerte, arco, suelo y utilería de archivo. Demuestra que la humanidad ocupa una infraestructura antigua mediante piezas de 2950 reparadas, mantenidas y disputadas. El agua entra, se regula y sale; los tubos no terminan arbitrariamente detrás de un objeto.

Los 28 briefs permiten reutilizar piezas en cámara de riego, acceso al reliquario y Archivo Abisal. La retícula es de 1 m; las dimensiones de herrajes y ergonomía usan fracciones justificadas. El humano de referencia es de 1,85 m, según biblia. Los centros de controles a 1,05 m y holgura frontal de 1,2 m son propuestas de diseño que deben cotejarse con la cámara y el controlador existentes.

La entrega mínima de un candidato requiere `.blend` editable, GLB, medidas reales, lista de componentes, materiales y render de la escena. El siguiente paso incluye UV, bake PBR, colisión separada, LOD donde proceda e importación. Si una fase falta, el recibo la mantiene pendiente. Un render de Blender no prueba texturas portables, colisión, rendimiento GPU ni calidad dentro del motor.

## Candidatos reales y límites de correspondencia

El primer kit remoto se conserva por separado en [`terra_reliquary_kit`](../terra_reliquary_kit/): [fuente Blender](../terra_reliquary_kit/EXOVANT_Terra_Kit.blend), [intercambio GLB](../terra_reliquary_kit/EXOVANT_Terra_Kit.glb), [auditoría geométrica](../terra_reliquary_kit/glb-audit.json) y [comprobación nativa](../terra_reliquary_kit/native-asset-check.json). Sus recibos describen lo que existe; el catálogo describe el objetivo de producción. La revisión artística humana sigue pendiente.

El pedestal de presentación de ese candidato tiene un diseño propio. No se identifica automáticamente con `TERRA_FLOOR_4M`, ni una pieza parecida supera por similitud el contrato de un módulo de 4 m. Cualquier correspondencia posterior debe registrar ID de hijo, dimensiones medidas, archivos, estado de exportación y diferencias aceptadas. Los 28 briefs permanecen `planned` hasta esa reconciliación explícita.

## Coordinación con gameplay

Este paquete ocupa únicamente `art_source/production_catalog/`. El frente artístico propone IDs hijos con padre canónico, pivotes, escala, sockets y estados visuales; el integrador conserva autoridad sobre `scripts/`, escenas jugables, guardado y misiones. Un modelo no cambia automáticamente alcance de ataque, collider, área de interacción ni bandera de misión.

Antes de integrar una pieza, ambos frentes necesitan acordar: ID de padre, nombre del nodo que se reemplaza, pivote, dimensiones importadas, estado inicial, partes móviles y qué se considera colisión. Publicar fuentes en rama de arte permite revisar este contrato sin sobrescribir el trabajo paralelo. La reserva local del coordinador no es un bloqueo distribuido ni prueba de confirmación del otro agente.

No se asigna `RIG_HUMAN` automáticamente a Siete-en-Uno, Faro-3 o La Voz Entre Rutas. Tampoco se exige esqueleto de locomoción al musgo, liquen, coral u otras formas estáticas: el manifest conserva la dependencia histórica y registra la excepción propuesta, que deberá aceptar integración.

## Gates de promoción

| Etapa | Evidencia necesaria | Estado de este catálogo |
|---|---|---|
| Brief cubierto | ID, función, silueta, materiales, escala y contrato | Validado por cobertura; dirección propuesta |
| Candidato geométrico | Fuente editable, exportación y medidas reales | Se registra por pieza fuera del snapshot |
| Candidato portable | UV, texturas, materiales, rig si aplica y reimportación | Pendiente por pieza |
| Candidato jugable | Colisión/LOD, sockets, animación e integración sin regresión | Pendiente por pieza |
| Aprobación artística | Misma cámara de juego, cerca/medio/lejos y revisión humana | Pendiente |
| Rendimiento aprobado | Hardware, ajustes, escena, memoria y tiempos de frame declarados | Pendiente |

No se amplía producción masiva de variantes por haber aprobado el JSON. Primero se inspecciona la unidad representativa y se corrigen escala, dibujo de materiales y coste de escena. Las bibliotecas, personajes y mundos posteriores usan lo aprendido sin dar por terminada la campaña global.

Para repetir la comprobación:

```bash
python art_source/production_catalog/validate_catalog.py --write-report
```

Este comando no llama proveedores, no modifica el runtime y no supera gates humanos o de hardware.
