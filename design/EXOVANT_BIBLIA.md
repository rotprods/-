# EXOVANT 2950 — Biblia de preproducción v0.1

**Fecha de corte: 12 de septiembre de 2026. Responsable creativo: Roberto Ortega. Título de trabajo: EXOVANT 2950 — El derecho a regresar. Estado: propuesta de diseño y producción; construcción pausada.**

Este documento transforma la ambición de un universo 3D soulslike interplanetario en decisiones revisables, contenido conectado, dependencias y criterios de aceptación. Las cifras son hipótesis de planificación, salvo los datos identificados como comprobados. Una ficha escrita es diseño propuesto; un archivo generado es un candidato; un activo de producción necesita importación, rendimiento, revisión y uso dentro del juego.

## 1. Decisión de infraestructura

**Recomendación: desarrollo nativo propio con Unreal y Blender, Mac mini como estación inicial, Higgsfield como taller remoto de conceptos y 3D, y un equipo RTX para validar la versión Windows y las funciones NVIDIA.** Esta sesión puede coordinar el trabajo, editar datos y código, preparar pruebas y revisar resultados. La decisión de comprometer producción queda después de una prueba comparativa del mismo escenario.

Higgsfield Games permite publicar juegos de navegador y anuncia generación 3D. Esa facilidad es valiosa para experimentar y compartir. No hemos verificado que entregue un proyecto Unreal nativo con los sistemas, las herramientas de perfilado y la distribución que exige esta visión. [Higgsfield Games](https://higgsfield.ai/games-intro).

| Entorno | Evidencia recuperada | Papel propuesto | Límite que afecta la decisión |
|---|---|---|---|
| PC virtual de esta sesión | 8 CPU lógicas de cuota, 20 GiB de RAM, aproximadamente 28 GB libres; Linux x86_64; sin dispositivo GPU ni servidor gráfico expuestos | Coordinación, código, catálogos, automatización y pruebas sin interfaz | Instalar un editor no crea una GPU; capacidad de disco insuficiente para una producción Unreal completa |
| Mac mini | USER.md registra M4 Pro; TRUTH_STATE del 31-07-2026 registra Blender 5.0.1, Godot 4.7.1, Unreal 5.8 y Unity instalados | Modelado, edición de niveles, programación, juego local y automatización por MCP | RAM, disco libre, versiones actuales y puentes activos pendientes de comprobar en la máquina |
| Higgsfield 3D Jutsu | Operación Blender completada; escena y exportación GLB/.blend disponibles | Blockouts, variaciones geométricas, revisión remota y activos exportables | No conocemos modelo de GPU, VRAM, permanencia de procesos ni rendimiento de una escena de producción |
| Higgsfield Games | Repositorio y entorno web accesibles; publicación para navegador documentada | Prototipo distribuible de una mecánica y pruebas de interacción | No equivale a una estación Unreal remota; exportación nativa y compatibilidad de plugins no verificadas |
| Windows con RTX, local o alquilado | Aún no hay máquina conectada ni cotización aceptada | Compilar, probar mandos, medir GPU y validar DLSS en el destino Windows | Coste, disponibilidad, drivers, acceso remoto y compatibilidad del proveedor pendientes |

El repositorio de infraestructura es [game-dev-mcp-hub](https://github.com/rotprods/game-dev-mcp-hub), leído en el commit `41f0710ee26e3948ea2f72ca4e0ebb20ef309fde`. El estado del Mac es evidencia documental histórica, no una comprobación en vivo. El README mantiene partes antiguas que dicen que algunos motores están aparcados; la fotografía de TRUTH_STATE y las políticas más específicas se contrastarán mediante una nueva prueba de funcionamiento. [TRUTH_STATE](https://github.com/rotprods/game-dev-mcp-hub/blob/41f0710ee26e3948ea2f72ca4e0ebb20ef309fde/docs/studio/TRUTH_STATE.md).

El contexto personal recuperado menciona una configuración Mac mini M4 Pro de 24 GB; se mantiene como referencia por contrastar con la máquina, ya que el inventario del repo no declara RAM. La documentación actual de Epic recomienda 32 GB o más en Mac. Registra soporte experimental de ray tracing por hardware y MegaLights en Apple Silicon M2+, y soporte beta de Nanite; por ello, la calidad del Mac se debe medir con nuestro escenario. No usaremos una afirmación antigua de ausencia total de esas funciones. [Requisitos macOS de UE 5.8](https://dev.epicgames.com/documentation/en-us/unreal-engine/macos-development-requirements-for-unreal-engine).

## 2. Contrato de misión y reglas recuperadas

**GOAL.** Diseñar y después construir una aventura de acción 3D en tercera persona, centrada en combate soulslike, exploración planetaria y consecuencias de la colonización humana en 2950, con una identidad visual y narrativa propia.

**NORTH STAR.** Un jugador entra en una región desconocida, interpreta señales de su ecología e historia, aprende un enfrentamiento exigente, abre una ruta nueva y toma una decisión cuyo efecto puede reconocer al volver. El viaje debe funcionar mediante espacios, acciones y consecuencias jugables.

**WHY.** Unir la intimidad de una decisión humana con la escala de una expansión galáctica. La misma infraestructura que permite regresar de la muerte hace posible apropiarse de mundos ajenos: combate, navegación y argumento comparten una causa.

**IN SCOPE de esta fase.** Diseño completo a nivel de preproducción del universo, sistemas, personajes, regiones, misiones, familias de activos, costes, arquitectura, secuencia de validación y migración. Las escenas individuales reciben un nivel de especificación proporcional a su cercanía a producción.

**NON-GOALS de esta fase.** Instalar motores, iniciar compras, abrir servicios del Mac a Internet, publicar un juego, declarar calidad AAA alcanzada o producir en serie todos los assets. La petición actual es planificar primero.

**Invariantes.** Volumen 3D real; combates legibles; estilo coherente; propiedad y procedencia trazables; partidas recuperables; decisiones persistentes; rendimiento medido sin confundir fotogramas generados con simulación; ninguna afirmación de finalización sin evidencia.

**Criterio de éxito de la planificación.** Cada categoría solicitada tiene una función jugable, un responsable de disciplina, dependencias, una fase, una estimación y un criterio de aceptación. Las incógnitas materiales tienen una prueba propuesta. El plan permite empezar por una unidad pequeña que represente la experiencia final.

**Criterio de éxito del juego, propuesto.** Al menos 8 de 10 participantes nuevos terminan el recorrido introductorio sin ayuda del desarrollador; al menos 7 explican una regla de combate y una consecuencia del mundo; se completa un recorrido sin bloqueos; guardar, morir, recuperar y volver a cargar conserva el estado correcto. Estas muestras pequeñas orientan decisiones de diseño; no demuestran aceptación comercial.

| Regla o protocolo | Estado de recuperación | Aplicación concreta |
|---|---|---|
| /DEFINE-GOAL v1.0 | Texto canónico recuperado | Objetivo, alcance, invariantes, criterios falsables y primera frontera |
| /CREATIVE-DIRECTION v1.0 | Texto canónico recuperado | Referencias descompuestas; tesis visual; continuidad; dependencias entre activos |
| /EMPEZARPROYECTO v1.0 | Texto canónico recuperado | Recuperar proyecto y estado antes de ejecutar; preparar continuidad; no duplicar autoridad |
| Reglas Studio OS / HARDMAX | Recuperadas | No dar instalaciones por hechas; respetar allowlist; conservar Knowledge Gold; registrar pruebas y artefactos |
| /leydekidlin | Definición exacta guardada no localizada | Aplicación provisional: escribir el problema, separar incógnitas, descomponerlo y establecer la prueba de resolución. No se atribuye a tu comando una formulación que no hemos leído |
| /promptengineer | Comando exacto no localizado ni disponible como preset | Se entrega un contrato de prompts de producción; no se afirma que se haya ejecutado una skill inexistente |
| Otras leyes personales | Sin inventario canónico localizado | No se añaden como si fueran reglas tuyas. Los criterios nuevos se etiquetan como propuestas |

Fuentes: [DEFINE-GOAL](https://github.com/rotprods/rot.knowledge/blob/46f5c9f627c0c4f26f74209432b84744295b1d54/prompts/strategy/DEFINE_GOAL_MASTER.md), [CREATIVE-DIRECTION](https://github.com/rotprods/rot.knowledge/blob/46f5c9f627c0c4f26f74209432b84744295b1d54/prompts/creative/CREATIVE_DIRECTION_MASTER.md), [autoridad de prompts](https://github.com/rotprods/rot.knowledge/blob/46f5c9f627c0c4f26f74209432b84744295b1d54/prompts/README.md), [políticas Studio OS](https://github.com/rotprods/game-dev-mcp-hub/blob/41f0710ee26e3948ea2f72ca4e0ebb20ef309fde/policies/studio_policies.json).

La búsqueda de leyes incluyó recuperación de contexto, archivos guardados, búsqueda del repositorio de desarrollo y el índice canónico de prompts. El árbol global de rot.knowledge estaba truncado; se examinaron por separado las carpetas relevantes de prompts, conocimiento y gobierno. Esto permite afirmar qué se recuperó, no que la regla no exista en ningún otro lugar. El corpus Knowledge Gold del Mac sigue pendiente de acceso.

## 3. Identidad creativa

**Tesis: la humanidad construyó un imperio dentro de un ser vivo sin reconocerlo.** Sus catedrales espaciales son estaciones de tránsito; los dioses que combate son funciones de mantenimiento; sus muertos regresan a través de una red que ya tenía habitantes.

El jugador debe sentir belleza, amenaza y responsabilidad. Cada planeta tiene su propia lógica material y cultural, mientras que determinados patrones revelan un origen compartido. Los habitantes no existen únicamente para dispensar misiones: tienen trabajo, parentesco, deuda, memoria y desacuerdos internos.

| Referencia solicitada | Atributo que interesa, como interpretación creativa | Transformación original para EXOVANT |
|---|---|---|
| Cyberpunk | Densidad social, estratos urbanos, cuerpos modificados, economía visible y personajes con intereses | Arcologías coloniales donde acceso al aire, memoria y resurrección determina la clase social |
| No Man’s Sky | Deseo de descubrir, tránsito entre mundos, fauna extraña y horizonte cosmológico | Doce mundos con regiones diseñadas y una frontera procedural acotada por ecologías comprensibles |
| Elden Ring | Combate con compromiso, siluetas memorables, descubrimiento y geografía interconectada | Reliquarios de tránsito, jefes ligados a la función del planeta y atajos que cambian la lectura del territorio |

Se toman principios y sensaciones; nombres, diseños, interfaces, personajes, música y mapas serán originales. No se promete combinar el volumen de contenido de tres producciones completas.

### Tres territorios conceptuales considerados

| Territorio | Imagen central | Ventaja | Riesgo | Decisión propuesta |
|---|---|---|---|---|
| Imperio de la memoria | Puertos catedralicios construidos sobre ecosistemas que recuerdan | Une combate, muerte, política y exploración | Exceso de exposición si todo se explica con diálogos | Dominante |
| Frontera mercenaria | Colonias corporativas y expediciones armadas | Entrada inmediata y vehículos claros | Se aproxima demasiado al imaginario espacial habitual | Reservar para Ares y Vanta |
| Peregrinación cósmica | Viaje por órganos de una entidad estelar | Gran singularidad visual | Abstracción que debilite orientación y humanidad | Reservar para el tercer acto |

### Gramática visual y sonora

Humanidad: cerámica marfil reparada, tejidos técnicos oscuros, códigos de mantenimiento, soldaduras recientes. Instituciones ricas ocultan reparaciones; trabajadores las exhiben como historial. Precursores: bronce oxidado, mineral negro, estructuras que distribuyen carga como huesos. Biosferas: formas repetidas por parentesco y adaptación, no por adornos aleatorios.

Ámbar significa refugio; cian pálido, memoria; bermellón, intención hostil; blanco frío, autoridad colonial. El significado se repite con forma y sonido para que el color nunca sea la única señal. Los entornos usan una dominante local, un material de ocupación humana y una huella de la red.

Composición: una referencia de orientación grande por región, hitos medianos que forman rutas y señales pequeñas que recompensan observación. La escala se demuestra con accesos, herramientas, cuerpos y desgaste. Una estructura enorme necesita una función imaginable.

Cámara: tercera persona cercana durante exploración, con distancia adaptable en encuentros grandes; FOV regulable, suavizado y vibración opcionales. Las tomas dramáticas deben preservar lectura de suelo, enemigo y salidas. Iluminación motivada por sol, maquinaria, organismos o señalización; oscuridad con separación de siluetas. Evitar bloom que borre la animación anticipatoria.

Sonido: los puertos de memoria emiten intervalos reconocibles; cada mundo modifica ese motivo con su medio físico. Terra mezcla olas con mecanismos enterrados, Vanta lluvia metálica y cables tensos, Origin respiración estructural. La música de jefe agrega capas al variar su conducta; el silencio anticipa cambios cuando resulta legible y consistente.

**Continuidad fija:** proporciones del protagonista, ubicación del relicario, materiales de cada facción, símbolos de refugio, tamaño de armas, escala de módulos y lenguaje de daño. **Variable:** clima, suciedad acumulada, iluminación, equipamiento autorizado y cámara. **Pendiente:** anatomías no observadas en una referencia de una sola vista; deben diseñarse y revisarse antes del modelado final.

## 4. Historia y cosmología

### Cronología ficticia

| Año | Suceso | Huella jugable en 2950 |
|---|---|---|
| 2090–2240 | Crisis de habitabilidad y construcción de arcologías | Barrios sellados, semillas bajo custodia y memorias editadas de los desplazamientos |
| 2326 | Descubrimiento de una estructura de tránsito bajo el Pacífico | Reliquario original y contratos de propiedad del acceso |
| 2381 | Primer tránsito humano por la Red Mnémica | Navegación por rutas, sin inventar velocidades físicas convencionales |
| 2460 | Legalización del retorno de memoria en cuerpos reconstruidos | Resurrección como infraestructura desigual, deuda y negocio |
| 2617 | Consolidación del Concordato Terrano | Derechos de paso, aduanas y representación colonial |
| 2734 | Contacto estable con enclaves de Andrómeda | Tratados contradictorios y culturas que no aceptan soberanía humana |
| 2878 | Expansión de Hélix; extracción de núcleos de tránsito | Heridas ecológicas y economías dependientes de suministros |
| 2941 | Protocolos de bioseguridad clasifican poblaciones humanas como intrusión | Custodios agresivos y rutas cerradas |
| 2950 | El protagonista vuelve con una memoria que pertenece a otra especie | Inicio de campaña y conflicto personal |

El viaje entre galaxias se explica mediante una tecnología ficticia de conexión, no mediante trayectos a velocidades sublumínicas en unos minutos. El mapa representa nodos accesibles de una red. Las distancias astronómicas siguen siendo enormes; la duración jugable representa tránsito por una ruta especial. No simularemos todas las estrellas de galaxias completas.

La jerarquía de datos será galaxia o región extragaláctica, sistema, cuerpo celeste, región de superficie, localización y encuentro. Cada nivel tiene identidad persistente. Las constelaciones son dibujos culturales vistos desde un origen concreto; no se confunden con sistemas físicamente próximos. El catálogo del tercer acto contiene fenómenos ficticios y los identifica como tales.

### Arcos de campaña

**Acto I — El derecho a regresar.** Terra enseña que proteger la Tierra y proteger a su población ya no coinciden para las instituciones. Ares, Pelagos y Umbra revelan distintos precios del retorno: energía, memoria y exclusión. El jugador obtiene la facultad de leer la red sin depender enteramente de su gobierno.

**Acto II — El derecho a nombrar.** Sylva, Khepri, Nacre y Vanta disputan quién interpreta vida, propiedad y archivo. Un registro humano llama recurso a lo que sus habitantes consideran persona. El jugador descubre que su cuerpo de retorno contiene una firma anterior a la colonización. Las facciones intentan convertirle en portavoz, prueba o propiedad.

**Acto III — El derecho a continuar.** Aurora Veil, Leviathan y Elysium Null enseñan tiempo, inmunidad y control. Origin revela la función compartida de las rutas. El desenlace depende de acuerdos, pruebas preservadas y comunidades capaces de mantener una alternativa; no de escoger un botón de color al terminar.

**Finales propuestos.** Concordia: la red sigue abierta con límites negociados y costes de mantenimiento compartidos. Soberanía: la humanidad controla rutas, gana estabilidad material y afronta una insurgencia ecológica. Retirada: cierra nodos invasivos, evacúa colonias viables y acepta pérdidas culturales irreparables. Testigo: una salida secreta libera parte de la memoria cautiva si el jugador conserva archivos incompatibles con las tres narrativas oficiales. Ningún final invalida retroactivamente el sufrimiento individual.

### Protagonista y relaciones

El **Custodio Exiliado** admite apariencia y trasfondo. Empieza como agente de recuperación de rutas, portador de una identidad legal revocada. El relicario del pecho permite volver a un santuario y escuchar memorias ambientales. Su evolución central es decidir si una memoria confiere propiedad, parentesco o responsabilidad.

Tres orígenes cambian conversaciones y equipo inicial, sin encerrar clases: superviviente de arcología, navegante sin ciudadanía y técnico de rehabilitación planetaria. Todos pueden aprender cualquier disciplina. Un origen no resuelve un conflicto automáticamente; ofrece una pista, una deuda o una relación.

Compañeros de núcleo: **Inés Vale**, archivista que participó en una falsificación y quiere repararla; **Rami Serrat**, ingeniero que protege a la tripulación que le considera cómplice; **Edda Jun**, traductora cuyo vínculo con la biosfera amenaza su identidad individual; **Mika Drav**, piloto sindical que puede mantener una ruta sin legitimidad estatal. Cada uno tiene deseo, secreto, desacuerdo con el jugador y un estado final ligado a hechos.

El antagonismo humano lo representa **Canciller Ivo Sanz**, que teme que una retirada condene a millones de colonos y oculta alternativas para preservar cohesión. La almirante **Maia Sol** ejecuta evacuaciones y bloqueos con una doctrina rígida, pero cambia si presencia capacidad logística real. **La Voz Entre Rutas** interpreta al protagonista como un síntoma de la red, no como elegido sobrenatural.

Los NPC no necesitan un LLM en ejecución para parecer vivos. Su memoria inicial será una selección de eventos persistentes, horarios sencillos, relaciones y diálogos escritos. Una capa conversacional generativa sería una investigación futura separada, con control de canon, latencia y coste.

## 5. Escala del producto

| Entrega | Contenido observable | Propósito |
|---|---|---|
| Prueba comparativa | La misma sala, personaje, adversario, luz y cámara en dos rutas de producción | Medir horas, fidelidad, exportación, mantenimiento y rendimiento |
| Prototipo de combate | Una arena y un enemigo legible; arte provisional | Elegir ritmo, cámara, compromiso de ataque y respuesta al daño |
| Vertical slice | 30–45 minutos, una región de Terra, un jefe, tres arquetipos enemigos, tres NPC, dos armas, un vehículo y un minijuego | Probar una sección representativa con calidad de producción |
| Capítulo financiable | Terra ampliada y un segundo mundo, con retorno entre ambos | Probar repetibilidad del pipeline y coste real por región |
| Visión completa | Doce mundos principales repartidos en tres ámbitos galácticos, con misiones y custodio final por mundo | Campaña interplanetaria; autorización de producción posterior al capítulo |

Objetivo creativo de campaña: 35–50 horas de recorrido principal y 60–90 con exploración, sujeto a pruebas de ritmo y financiación. Es una meta de diseño, no una duración ya medida. Cada mundo ofrece una región abierta principal de aproximadamente 2–6 km² jugables, dos espacios interiores o mazmorras y áreas orbitales delimitadas. Doce mundos no significa doce esferas enteras con cada metro construido a mano.

Propuesta de alcance espacial: salida de un puerto, vuelo atmosférico en volumen acotado, aproximación orbital y tránsito con transición integrada en cabina. El aterrizaje completamente continuo desde cualquier lugar del espacio queda como investigación posterior; no será una dependencia del combate ni de la campaña. Se conserva la sensación de expedición mediante control de la nave, distancias locales, navegación y consecuencias logísticas.

La frontera procedural utiliza gramáticas de terreno, bioma y asentamiento validadas. Sus semillas son reproducibles y no mezclan fauna, recursos y ruinas sin reglas. Misiones principales, arenas y rutas críticas se diseñan y prueban individualmente. Los límites planetarios se justifican por clima, permiso, combustible de aterrizaje o terreno, sin paredes invisibles en caminos anunciados como transitables.


## 6. Atlas de mundos y custodios

Todos los sistemas fuera de Sol, sus cuerpos y sus constelaciones culturales son ficción de diseño. Las cifras ambientales son condiciones de referencia del área jugable, no una simulación astrofísica global. El Umbral es una región extragaláctica ficticia; no se presenta como una galaxia observada. Hay dos galaxias reales usadas como marco narrativo y un tercer ámbito ficticio.

| Ámbito | Mundo | Sistema | Custodio |
| --- | --- | --- | --- |
| VÍA LÁCTEA | TERRA | Sol | ATLAS, el jardinero orbital |
| VÍA LÁCTEA | ARES IX | Sol | MOL-9, el devorador de mantos |
| VÍA LÁCTEA | PELAGOS | Talas | THALASSA, coral de los mil ojos |
| VÍA LÁCTEA | UMBRA | Sere | NOCTIL, el eclipse viviente |
| ANDRÓMEDA | SYLVA PRIME | Dendra | VESPER, raíz de todas las voces |
| ANDRÓMEDA | KHEPRI | Sahra | RA-KHET, sol encadenado |
| ANDRÓMEDA | NACRE | Mneme | MNEMOS, el archivo encarnado |
| ANDRÓMEDA | VANTA | Drav | FERRUM, coloso de chatarra |
| EL UMBRAL | AURORA VEIL | Velar | AEON, el fruto del mañana |
| EL UMBRAL | LEVIATHAN | Soma | SOMA, el sistema inmune |
| EL UMBRAL | ELYSIUM NULL | Alba Nula | EDEN, la perfección hostil |
| EL UMBRAL | ORIGIN | Nexo Exovant | EXOVANT, el corazón de los caminos |


### 01. TERRA — ATLAS, el jardinero orbital

**Ámbito:** VÍA LÁCTEA. **Sistema:** Sol. **Facción:** Concordato Terrano.

**Cielo y cuerpos:** Sol, estrella G; referencia real con futuro ficticio. Tierra; el área inicial es un archipiélago de infraestructura orbital. Luna; anillo de residuos y plataformas de ascenso.

**Referencia ambiental:** gravedad 1,00 g; temperatura de área 22 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: costa terrana. Aguja Rota: antiguos satélites confundidos con un asterismo; Mano del Retorno: constelación cultural ficticia.

**Conflicto:** Las torres de lanzamiento atraviesan bosques nacidos sobre ciudades costeras. El sistema que reparó la biosfera ha declarado a la humanidad especie invasora.

**Regla jugable:** La vegetación conduce impulsos de mantenimiento: cortar una raíz abre una puerta y altera el riego de otra zona. El agua conecta lectura de ecología, acceso y autoridad.

**Geografía y rutas:**

- Costa de los Retornados: muelles, viviendas y bosque de sal

- Archivo Abisal: oficinas inundadas y bóvedas de semillas

- Primer Reliquario: jardín industrial, elevador y arena de ATLAS

**Biota y relaciones:**

- Cérvido de silicio: dispersa semillas con pezuñas minerales; huye del bermellón

- Garza de cable: anida en conductores y anticipa sobrecargas

- Cangrejo de sal: consume polímeros de la costa; revela accesos ocultos

- Musgo testigo: conserva huellas bioeléctricas y expone actividad reciente

**NPC y motivación:**

- Inés Vale / archivo / quiere revelar su participación en la falsificación

- Bruno Arce / refugiado del elevador / exige agua antes de hablar de ecología

- Saja Lin / técnica de semillas / negocia una zona compartida de cultivo

**Adversarios:**

- Custodio de poda: barridos de herramienta, vulnerable al terminar el giro

- Expropiador del Concordato: escudo y avance, flanqueable por riego lateral

- Carro de cuarentena: niebla y cierre de rutas, reactor expuesto al ventilar

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_TERRA_M01 | La última costa | Atracar, encontrar refugio y restablecer agua para ocho familias; tutorial de interacción con riesgo visible |
| Q_TERRA_M02 | Un jardín sin humanos | Seguir tres especies hasta descubrir que los ataques protegen un vivero; resolver un circuito de riego |
| Q_TERRA_M03 | El archivo sumergido | Descender al archivo por techo o esclusa y recuperar un acta conservando su autenticidad |
| Q_TERRA_M04 | Despertar a ATLAS | Reactivar el elevador para llevar a ATLAS a una plataforma donde pueda aislarse su protocolo |
| Q_TERRA_M05 | El derecho a regresar | Resolver quién administra agua, transporte y semillas; volver al muelle para ver el resultado |


**Misiones secundarias:**

- La casa que sigue pagando: una deuda se cobra a la memoria de una persona muerta; localizar a su descendiente o anular el registro

- Ocho semillas: elegir qué cultivar en un refugio limitado; la cosecha modifica suministros y conversaciones

**Minijuego:** Riego resonante: orientar tres válvulas siguiendo presión y sonido; sin temporizador por defecto.

**Vehículo local:** Peregrino-6, rover anfibio de mantenimiento.

**Arena del custodio:** Plataforma circular de 48 m, tres brazos de riego, dos pasos laterales y un núcleo central. El bloqueo de cámara se puede trasladar entre torso y herramienta.

**Fases propuestas:**

- 100–60%: poda; barridos horizontales y pisadas marcadas por raíces luminosas

- 60–25%: cuarentena; cierra un sector y cambia rutas de aproximación sin eliminar todas las salidas

- 25–0%: raíz expuesta; permite atacar el núcleo o aplicar el acta autenticada para separar el protocolo hostil

**Ataques representativos y respuesta:**

- Guadaña orbital: hombro elevado 0,8 s, barrido, recuperación 1,1 s; esquivar hacia el interior

- Siembra de lanzas: tres marcas de suelo durante 1,2 s; salir del patrón, castigar brazo clavado

- Riego de cuarentena: boquillas apuntan 1,4 s antes del arco; abrir válvula lateral para crear una zona segura

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Articulación de ATLAS: golpe pesado puede activar mecanismos; alternativa pacífica conserva al custodio como servicio de riego.

**Consecuencias al regresar:**

- Industria: elevador operativo y repuestos baratos, junto con patrullas y reducción del jardín

- Cogobierno: rutas mantenidas por técnicos y biosfera; requiere conservar acta y salvar el vivero

- Santuario: costa regenerada y evacuación de sectores industriales; menos comercio y nuevas rutas naturales

**Secreto narrativo:** El archivo confirma que las extinciones justificaron concesiones de suelo. Inés aparece como firmante.

**Arte y sonido:** Arcología costera: hormigón erosionado, cerámica, raíces estructurales, pasarelas y conductos de riego. Olas, cilindros hidráulicos bajo piedra y un motivo coral de cuatro notas que ATLAS pronuncia con bombas.

**Riesgo específico:** Agua, vegetación y estructura densa compiten por GPU; limitar transparencias y medir la legibilidad del jefe sobre el fondo.

### 02. ARES IX — MOL-9, el devorador de mantos

**Ámbito:** VÍA LÁCTEA. **Sistema:** Sol. **Facción:** Consorcio Hélix.

**Cielo y cuerpos:** Sol; Ares IX designa el noveno distrito colonial de Marte. Marte transformado parcialmente; el entorno abierto sigue requiriendo traje. Fobos, Deimos y un puerto minero ficticio.

**Referencia ambiental:** gravedad 0,38 g; temperatura de área −41 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: distrito Ares IX. Mandíbula: luces de una refinería orbital; Viuda Roja: dibujo cultural de navegantes, sin coordenadas astronómicas atribuidas.

**Conflicto:** Los colonos perforaron hasta encontrar una máquina que soñaba bajo el óxido. Cada tormenta retransmite las últimas palabras de una colonia desaparecida.

**Regla jugable:** El calor es soporte vital y peligro táctico. Redirigirlo cambia visibilidad, accesos y supervivencia de refugios; cada conducto ofrece lectura térmica previa.

**Geografía y rutas:**

- Escarpa del Turno Nueve: pueblo minero y vías de carga

- Pozos de los Durmientes: galerías térmicas con embriones

- Mandíbula del Manto: instalaciones móviles y reactor de MOL-9

**Biota y relaciones:**

- Raya de polvo: se desliza por bolsas gaseosas y revela corrientes

- Litófago ferruginoso: digiere óxidos en cavernas templadas

- Gusano de sílice: reacciona a vibración industrial

- Liquen de respiradero: marca temperatura segura en la roca

**NPC y motivación:**

- Rami Serrat / ingeniero / protege al turno atrapado

- Vera Cid / jefa de concesión / teme quedarse sin calefacción para la colonia

- Tomás Hume / guardián de incubadoras / desconfía de toda perforación

**Adversarios:**

- Perforador Hélix: ataques rectos que se atascan en roca dura

- Sabueso de sondeo: rastrea vibraciones; pierde objetivo cuando las bombas rugen

- Desertor térmico: arma de presión que necesita recarga visible

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_ARES_M01 | Voces bajo el óxido | Investigar una señal de auxilio que coincide con latidos del subsuelo |
| Q_ARES_M02 | Rastros en la tormenta | Seguir una raya durante la tormenta o reparar una baliza para entrar por otra ruta |
| Q_ARES_M03 | El pozo de los durmientes | Distribuir calor entre dos galerías y evacuar un turno antes de descender |
| Q_ARES_M04 | La mandíbula de MOL-9 | Inmovilizar la plataforma de MOL-9 y combatir sobre conductos con temperatura cambiante |
| Q_ARES_M05 | Quién merece despertar | Decidir quién usa la energía tras descubrir que la máquina sostiene incubadoras |


**Misiones secundarias:**

- El turno que no fichó: reconstruir una nómina manipulada y compensar a familias

- Un sol para la enfermería: construir un desvío térmico con tres repuestos elegidos, no recolectados al azar

**Minijuego:** Equilibrado térmico: mantener dos circuitos dentro de banda evitando sobrepresión; opción de resolución asistida.

**Vehículo local:** Peregrino-6 con tracción minera; Taladro Mula como vehículo de secuencia.

**Arena del custodio:** Foso industrial de 64 m con pasarelas que sobreviven al cambio de fase; salidas térmicas alternas.

**Fases propuestas:**

- 100–65%: brazo excavador; golpes lineales, giros lentos

- 65–30%: sobrepresión; abre grietas anunciadas y expone tubos refrigerantes

- 30–0%: soporte vital; el daño al núcleo compromete incubadoras y habilita desacoplamiento si se recuperó el esquema

**Ataques representativos y respuesta:**

- Mandíbula de pozo: perforadora retraída 1,0 s, carga recta; flanquear y romper abrazadera

- Ventilación roja: válvulas vibran 1,3 s; refugiarse tras pantalla térmica

- Anillo sísmico: apoyo de tres patas 1,1 s; cruzar por pasarela elevada, no por salto obligatorio

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Válvula de manto: herramienta de presión para armas pesadas y sellos industriales.

**Consecuencias al regresar:**

- Extracción: combustible barato y expansión Hélix; incubadoras reducidas

- Reparto: limita producción y garantiza calor a colonia y durmientes; exige pruebas y reparación

- Sellado: detiene el daño pero obliga a evacuar la escarpa y modifica rutas de comercio

**Secreto narrativo:** MOL-9 dejó de extraer hace décadas; el supuesto mineral crítico es la carcasa de una reserva de vida.

**Arte y sonido:** Minería roja: tubos aislados, módulos de presión, elevadores, cintas y roca estratificada. Radio entrecortada, metal tensionado y pulsos graves por conducción en el traje.

**Riesgo específico:** Terreno deformable continuo es demasiado costoso al inicio; usar sectores y estados de destrucción diseñados.

### 03. PELAGOS — THALASSA, coral de los mil ojos

**Ámbito:** VÍA LÁCTEA. **Sistema:** Talas. **Facción:** Liga de las Mareas.

**Cielo y cuerpos:** Talas, K2 V ficticia. Mundo oceánico con plataformas en arrecifes; gravedad de diseño 0,91 g. Lágrima, luna conductora ficticia que condiciona mareas.

**Referencia ambiental:** gravedad 0,91 g (propuesta revisada); temperatura de área 8 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: superficie de Pelagos. La Red Vacía y Pez de Tres Ojos son constelaciones culturales locales; cambian bajo refracción acuática.

**Conflicto:** Las ciudades flotantes migran según canciones que nadie compuso. La población local transmite recuerdos en las mareas.

**Regla jugable:** El arrecife almacena sonido; reproducir una secuencia atrae fauna, abre membranas o delata al jugador. La información recogida pertenece a individuos vivos.

**Geografía y rutas:**

- Mercado de Boyas: población móvil y ensamblajes flotantes

- Coro del Arrecife: canales que retienen memoria

- Fosa de las Mil Miradas: santuario de THALASSA

**Biota y relaciones:**

- Medusa mnémica: transmite memoria luminosa; no es una batería sin dueño

- Anguila de vidrio: caza siguiendo sonido repetido

- Bóvido de arrecife: mantiene canales al pastar

- Coral escriba: incorpora vibración a su crecimiento

**NPC y motivación:**

- Nara Océano / bióloga anfibia / quiere contacto sin extracción

- Damián Vo / capitán de boyas / necesita un canal de comercio

- Téa del Coro / intérprete de arrecife / comparte memoria de forma parcial

**Adversarios:**

- Buzo de extracción: arpón con cable que se puede cortar

- Guardia de pólipos: protege zonas acústicas, retrocede ante disonancia aprendida

- Anguila centinela: carga entre anclajes, con recorrido visible

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_PELAGOS_M01 | Ciudad a la deriva | Estabilizar una plataforma y aprender respiración del traje |
| Q_PELAGOS_M02 | La memoria de la sal | Registrar llamadas del arrecife distinguiendo saludo de alarma |
| Q_PELAGOS_M03 | Traducir una marea | Recuperar una memoria robada sin destruir el coral que la contiene |
| Q_PELAGOS_M04 | Los mil ojos de THALASSA | Descender usando anclajes y enfrentar a THALASSA en una cámara con zonas secas |
| Q_PELAGOS_M05 | La voz del océano | Negociar el uso del canal y la restitución de memorias |


**Misiones secundarias:**

- El nombre prestado: un marinero recuerda una infancia ajena; devolverla o acordar memoria compartida

- La boya funeraria: construir una señal audible por humanos y arrecife

**Minijuego:** Traducción acústica: relacionar pulsos, respuestas y contexto; subtítulos y visualización de espectro opcionales.

**Vehículo local:** Nácar-2, sumergible biplaza sin acompañante obligatorio.

**Arena del custodio:** Cámara inundable de 52 m con plataformas de mantenimiento y anclajes; nunca exigir combate preciso en nado libre antes de validarlo.

**Fases propuestas:**

- 100–70%: ojos exploradores revelan al jugador entre pilares

- 70–35%: alterna inundación de dos sectores y tentáculos de cierre

- 35–0%: el coro responde a la memoria restituida y permite cortar el vínculo de extracción

**Ataques representativos y respuesta:**

- Mirada convergente: tres ojos fijan luz 1,2 s; romper línea con columna

- Látigo de corriente: tentáculo carga desde fuera 0,9 s; entrar en bolsillo interior

- Canto de presión: membranas se expanden 1,6 s; cambiar a plataforma ventilada

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Lente de memoria: identifica resonancias ocultas y modifica herramientas sónicas.

**Consecuencias al regresar:**

- Canal comercial: prospera el mercado y el arrecife pierde intimidad

- Tratado de consentimiento: tránsito por horarios y devolución de datos; exige archivos íntegros

- Reserva marina: comercio desviado y fauna restaurada; un NPC abandona su negocio

**Secreto narrativo:** Las voces que el mercado vende como ambientación son recuerdos de sujetos vivos.

**Arte y sonido:** Arrecife habitado: flotadores, conchas, tejidos impermeables, coral volumétrico simplificado. Hidrófonos, respiración medida y voces que parecen cercanas pero llegan por estructuras.

**Riesgo específico:** Agua y movimiento vertical amenazan cámara y controles; arena híbrida con suelo firme en la primera versión.

### 04. UMBRA — NOCTIL, el eclipse viviente

**Ámbito:** VÍA LÁCTEA. **Sistema:** Sere. **Facción:** Flotilla de los Sin Sol.

**Cielo y cuerpos:** Sere, enana roja M4 V ficticia. Rotación sincronizada ficticia; asentamientos en la franja crepuscular. Pequeño enjambre de estaciones reflector.

**Referencia ambiental:** gravedad 0,81 g; temperatura de área −87 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: franja de Umbra. Ojo Quieto y Esposas del Alba son dibujos de la Flotilla; el sol mantiene posición casi fija.

**Conflicto:** Un hemisferio arde y el otro nunca ha visto luz. Los refugiados viven en una estrecha franja donde las sombras llegan antes que los cuerpos.

**Regla jugable:** Luz y sombra son permisos de navegación además de temperatura. Encender un reflector revela rutas y expone caravanas a vigilancia.

**Geografía y rutas:**

- Caravana del Terminador: hogares que siguen corredores térmicos

- Observatorio de los Sin Nombre: antenas y archivos de ciudadanía

- Corona de NOCTIL: gigantesca estación de sombra

**Biota y relaciones:**

- Mantis de sombra: detecta contornos contra la luz

- Pastor de escarcha: migra por gradientes térmicos

- Polilla de penumbra: poliniza durante pulsos de reflector

- Hongo umbral: obtiene energía de oscilaciones térmicas

**NPC y motivación:**

- Soren Vey / cartógrafo / guarda rutas de exiliados

- Uma Re / médica de caravana / necesita un reflector estable

- Luc Sain / inspector / busca regularizar a cambio de vigilancia

**Adversarios:**

- Vigía de contraluz: dispara desde siluetas recortadas

- Mantis de sombra: dos avances y pausa reconocible

- Notario armado: fija zonas de acceso y persigue al cruzarlas

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_UMBRA_M01 | La frontera del día | Encontrar la caravana leyendo temperatura y huellas |
| Q_UMBRA_M02 | Sombras que respiran | Ajustar un reflector para salvar un convoy sin mostrar su ruta completa |
| Q_UMBRA_M03 | Geometría del eclipse | Recuperar registros que demuestran exclusión deliberada de retornados |
| Q_UMBRA_M04 | El refugio de NOCTIL | Ascender a la corona y combatir el mecanismo de NOCTIL |
| Q_UMBRA_M05 | Una luz para todos | Elegir un régimen de acceso para la franja habitable |


**Misiones secundarias:**

- Ciudadanía de una sombra: reunir tres testimonios para una persona borrada

- La caravana inmóvil: reparar un hogar sin condenarlo a pagar peaje permanente

**Minijuego:** Cartografía celeste: alinear referencias locales y una baliza; no requerir reconocer constelaciones reales.

**Vehículo local:** Vela de Ceniza, planeador que usa gradientes de la franja.

**Arena del custodio:** Anillo de observación de 44 m con pantallas giratorias; el suelo permanece visible y las áreas seguras tienen señal redundante.

**Fases propuestas:**

- 100–65%: una fuente de luz y sombra móvil

- 65–30%: dos fuentes generan refugios alternos, nunca oscuridad total ilegible

- 30–0%: proyección del observatorio; desactivar vigilancia modifica su último patrón

**Ataques representativos y respuesta:**

- Corte de horizonte: emisor se alinea 1,0 s; usar pantalla

- Paso de eclipse: sombra converge 1,2 s antes del impacto

- Lanza del alba: espejo vibra 0,8 s; esquiva lateral, castigo al actuador

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Velo de terminador: maniobra breve que interrumpe fijación óptica sin invisibilidad infinita.

**Consecuencias al regresar:**

- Registro central: servicios estables y mayor vigilancia

- Federación de caravanas: datos distribuidos y mantenimiento comunitario

- Oscurecimiento: rutas clandestinas seguras y menor producción energética

**Secreto narrativo:** La escasez de franjas habitables fue exagerada para controlar la ciudadanía.

**Arte y sonido:** Crepúsculo móvil: carros, reflectores, hielo oscuro y tela tensada. Viento lateral constante, lonas y radio de caravanas con silencios significativos.

**Riesgo específico:** Oscuridad no puede ocultar anticipaciones; ensayo con brillo bajo y perfiles de visión de color.

### 05. SYLVA PRIME — VESPER, raíz de todas las voces

**Ámbito:** ANDRÓMEDA. **Sistema:** Dendra. **Facción:** Coro Micelial.

**Cielo y cuerpos:** Dendra, K1 V ficticia en Andrómeda. Superficie de raíces y plataformas vivas; gravedad propuesta 1,12 g. Semilla, luna pequeña ficticia y enjambre polinizador orbital.

**Referencia ambiental:** gravedad 1,12 g (propuesta revisada); temperatura de área 34 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: claro alto de Sylva. Raíz Suspendida y El Huésped dibujan parentescos, no conquistas.

**Conflicto:** Las plantas imitan recuerdos humanos para comunicarse. Algunas aldeas han olvidado dónde termina su conciencia y empieza la del bosque.

**Regla jugable:** La red vegetal comparte información con retraso local. Dañar una raíz produce una respuesta en otra zona, anunciada por color, sonido y mensajeros.

**Geografía y rutas:**

- Puerto del Injerto: enclave humano alojado en tejido vivo

- Bosque de las Frases: rutas que responden a señales aprendidas

- Cámara de VESPER: nudo radical bajo una ciudad forestal

**Biota y relaciones:**

- Ciervo de esporas: lleva fragmentos de lenguaje en su pelaje

- Grajilla micelar: intercambia nutrientes por avisos

- Andador de corteza: herbívoro de seis patas con senderos estables

- Orquídea de pacto: florece donde se ha mantenido un acuerdo

**NPC y motivación:**

- Edda Jun / xenolingüista / teme perder individualidad

- Siete-en-Uno / emisario vegetal / desea entender desacuerdo humano

- Nico Fer / colono carpintero / necesita material sin talar al anfitrión

**Adversarios:**

- Recolector de sinapsis: corta nodos para vender memoria

- Caballero de corteza: guardia que responde a agresión territorial

- Araña de injerto: teje obstáculos con anclajes destructibles

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_SYLVA_M01 | La selva pronuncia tu nombre | Entrar en el puerto aceptando un protocolo de hospitalidad comprensible |
| Q_SYLVA_M02 | Tres lenguas sin boca | Aprender señales de advertencia y permiso mediante acciones repetibles |
| Q_SYLVA_M03 | El contrato de las raíces | Rescatar a un traductor dentro de un enlace que se ha cerrado |
| Q_SYLVA_M04 | Bajo la piel de VESPER | Descender al nudo de VESPER y separar una infección industrial |
| Q_SYLVA_M05 | Memoria compartida | Proponer la forma de convivencia del enclave humano |


**Misiones secundarias:**

- Una habitación privada: construir aislamiento para una persona que no quiere compartir recuerdos

- El árbol que dijo no: buscar material alternativo para un puente que el bosque rechaza

**Minijuego:** Gramática de gestos: ordenar intención, sujeto y límite; respuestas de contexto, sin idioma real imitado.

**Vehículo local:** Vela de Ceniza con agarres de canopy.

**Arena del custodio:** Tres terrazas conectadas por raíces anchas; el desplazamiento vertical se resuelve con rutas y anclajes, no saltos de precisión sorpresa.

**Fases propuestas:**

- 100–70%: guardianes y brazos radicales protegen sinapsis

- 70–35%: retransmite los últimos movimientos del jugador como ecos retrasados

- 35–0%: se puede contener la infección y negociar separación de memorias si se aprendieron límites

**Ataques representativos y respuesta:**

- Raíz orante: el suelo se arquea 1,1 s; salir del carril

- Eco de injerto: silueta reproduce un ataque previo tras 1,5 s; variar posición

- Cierre de copa: hojas caen como aviso antes del domo; abrir un anclaje lateral

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Injerto de VESPER: habilidad de eco limitada por concentración.

**Consecuencias al regresar:**

- Concesión de extracción: equipo potente y fragmentación del bosque

- Hospedaje pactado: acceso a rutas vivas con obligaciones de reparación

- Separación: enclave humano independiente, menos intercambio y privacidad preservada

**Secreto narrativo:** Algunos colonos pidieron voluntariamente integrarse; otros fueron conectados sin entender el contrato.

**Arte y sonido:** Bosque neural: raíces estructurales, membranas, andamios de injerto y follaje por capas. Percusión de madera, respiraciones múltiples y frases que llegan desde raíces separadas.

**Riesgo específico:** Navegación en formas orgánicas; mantener pendientes, anchuras y lenguaje de rutas consistentes.

### 06. KHEPRI — RA-KHET, sol encadenado

**Ámbito:** ANDRÓMEDA. **Sistema:** Sahra. **Facción:** Sínodo de Bronce.

**Cielo y cuerpos:** Sahra, F8 V ficticia en Andrómeda. Desierto de vidrio solar con ciudades bajo heliostatos. Aguja, estación reflectora y dos lunas rocosas ficticias.

**Referencia ambiental:** gravedad 0,63 g; temperatura de área 71 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: Khepri al anochecer. Escarabajo Abierto y El Deudor son cartas rituales de navegación.

**Conflicto:** Una civilización robótica considera sagradas las piezas que no puede reemplazar. Su estrella artificial está dejando de obedecer.

**Regla jugable:** La luz almacena energía y también derechos de uso. Orientar espejos cambia temperatura, puertas y el suministro de barrios.

**Geografía y rutas:**

- Ciudad de los Toldos: talleres y deuda energética

- Mar de Cristal: campos de reflexión y rutas de sombra

- Crisol de RAKHET: máquina solar encadenada

**Biota y relaciones:**

- Escarabajo heliostato: orienta su caparazón para regular calor

- Zorro de vidrio: refracta su contorno sin volverse invisible

- Serpiente de cable: vive entre colectores enfriados

- Liquen de prisma: fija minerales en áreas de luz dispersa

**NPC y motivación:**

- Hermana Asha / mecánica del Sínodo / busca abolir deuda heredada

- Qadir Noé / mercader / financia reparaciones que nadie quiere pagar

- Yal de la Sombra / cuidadora / conoce rutas fuera del culto

**Adversarios:**

- Penitente heliostático: escudo espejo con ventana de giro

- Saboteador de lente: coloca haces con anclajes visibles

- Escarabajo colosal: enemigo territorial, vulnerable tras descargar calor

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_KHEPRI_M01 | La peregrinación de cobre | Reparar un toldo comunitario y conocer el precio de la luz |
| Q_KHEPRI_M02 | Reliquias vivientes | Cruzar el mar usando reflectores o rutas subterráneas |
| Q_KHEPRI_M03 | El salmo de las baterías | Liberar a técnicos retenidos por deuda en el crisol |
| Q_KHEPRI_M04 | Desencadenar a RA-KHET | Enfrentar a RAKHET redistribuyendo haces entre nodos de arena |
| Q_KHEPRI_M05 | El precio de otro amanecer | Decidir quién posee y mantiene la infraestructura solar |


**Misiones secundarias:**

- La sombra de una hija: una familia hereda un peaje sin salida; revisar el contrato y su firma

- Vidrio para beber: convertir un colector menor en condensador, sacrificando energía del mercado

**Minijuego:** Óptica de prismas: redirigir haces con lectura térmica; modo asistido elimina precisión de cursor.

**Vehículo local:** Helioperegrino, moto de vela solar de superficie.

**Arena del custodio:** Hexágono de espejos de 56 m; cuatro pozos de sombra siempre accesibles y plataformas estables.

**Fases propuestas:**

- 100–65%: cadenas y garras orientan dos haces

- 65–25%: rompe una cadena y cambia el ángulo de luz, conservando refugios

- 25–0%: núcleo expuesto puede extinguirse o conectarse a una red distribuida

**Ataques representativos y respuesta:**

- Juicio de mediodía: lente enfoca 1,4 s; cambiar a sombra

- Cadena solar: brazo se enrolla 1,0 s antes del barrido

- Descarga de vidrio: suelo cruje 1,2 s; huir del sector marcado

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Prisma del Crisol: modifica daño de energía y abre cerraduras ópticas.

**Consecuencias al regresar:**

- Sínodo reformado: continuidad técnica y jerarquía persistente

- Red común: luz por necesidad y trabajo de mantenimiento distribuido

- Desmantelamiento: reduce poder coercitivo pero obliga a reubicar barrios dependientes

**Secreto narrativo:** El sol no exige sacrificios; la deuda sostiene una estructura administrativa humana.

**Arte y sonido:** Cristal y sombra: telas, espejos, cerámica abrasada, prismas y pasarelas. Campanas de vidrio, cables resonantes y motores de seguimiento solar.

**Riesgo específico:** Reflejos y emisión saturada; medir sobreexposición y evitar superficies especulares sin función.

### 07. NACRE — MNEMOS, el archivo encarnado

**Ámbito:** ANDRÓMEDA. **Sistema:** Mneme. **Facción:** Casas de Nácar.

**Cielo y cuerpos:** Mneme A/B, binaria ficticia estable para la ficción del juego. Mundo de conchas minerales y archivos cultivados; colonias en una luna mayor. Tres lunas-archivo ficticias, con rutas de órbita diseñadas.

**Referencia ambiental:** gravedad 0,26 g; temperatura de área 16 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: luna Nacre. Dos Testigos y El Recipiente cambian su importancia según posición de las dos estrellas.

**Conflicto:** Las ciudades crecen dentro de conchas kilométricas. Sus habitantes guardan vidas enteras en perlas y comercian con biografías.

**Regla jugable:** Un recuerdo puede existir en varias versiones con procedencia distinta. La autenticidad abre rutas narrativas; copiarlo consume soporte y modifica quién conserva acceso.

**Geografía y rutas:**

- Casa de las Copias: mercado de recuerdos restaurados

- Canteras de Concha: bibliotecas que crecen por estratos

- Archivo de MNEMOS: salas esféricas conectadas por puentes

**Biota y relaciones:**

- Ave de cristal blando: imita llamadas y transporta fragmentos

- Caracol de archivo: organiza capas minerales por vibración

- Polilla de nácar: revela escritura cuando posa sus alas

- Liquen palimpsesto: cubre y conserva huellas previas

**NPC y motivación:**

- Lio Mneme / conservador / prefiere una mentira que mantenga paz

- Aina Dos / restauradora / conserva dos memorias incompatibles

- Ors Vid / heredero / quiere borrar un crimen familiar sin destruir a su comunidad

**Adversarios:**

- Notario de concha: escudo que registra y repite impactos

- Copista armado: usa una variante limitada de la postura del jugador

- Guardián de bóveda: golpea siguiendo dos pulsos alternos

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_NACRE_M01 | El mercado de las vidas | Autenticar una memoria sin confundir originalidad con verdad |
| Q_NACRE_M02 | Testigos de cristal | Comparar dos archivos que atribuyen una misma masacre a bandos distintos |
| Q_NACRE_M03 | La perla sin dueño | Conseguir soporte para conservar testimonios de víctimas y responsables |
| Q_NACRE_M04 | La mentira de MNEMOS | Atravesar MNEMOS distinguiendo salas de archivo de copias hostiles |
| Q_NACRE_M05 | Publicar el pasado | Definir un régimen de acceso, privacidad y reparación del archivo |


**Misiones secundarias:**

- El recuerdo que sobra: una persona pide olvidar; decidir qué parte del registro público debe permanecer

- Los tres testigos: demostrar hechos sin exigir que todos recuerden lo mismo

**Minijuego:** Restauración estratigráfica: ordenar capas y señalar contradicciones; la interfaz explica evidencias y permite volver atrás.

**Vehículo local:** Cargador de Concha, vehículo logístico no pilotable en combate.

**Arena del custodio:** Biblioteca circular de 46 m con tres versiones visibles de su estructura; solo una cambia colisión por transición.

**Fases propuestas:**

- 100–70%: registra ataques y devuelve una copia anunciada

- 70–30%: alterna dos custodios-eco, nunca todos los patrones a la vez

- 30–0%: revela el registro censurado; destruir soporte o limitar autoridad producen desenlaces distintos

**Ataques representativos y respuesta:**

- Cita de acero: página mineral se despliega 0,9 s; rodear el lomo

- Repetición: eco translúcido marca trayectoria 1,2 s antes de actuar

- Indexación: columnas numeradas por símbolos convergen lentamente; salir por hueco conservado

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Sello palimpsesto: segunda ranura de memoria táctica con coste de concentración.

**Consecuencias al regresar:**

- Archivo central: acceso rápido con censura institucional

- Custodia distribuida: redundancia y privacidad negociada; exige soportes preservados

- Olvido dirigido: libera a personas concretas pero pierde pruebas que otras necesitaban

**Secreto narrativo:** La red conserva experiencias sin garantizar su interpretación; el relato imperial convirtió copia en autoridad.

**Arte y sonido:** Archivo mineral: bóvedas de concha, placas translúcidas y puentes finos. Fricción de concha, golpes suaves y voces desplazadas en el espacio.

**Riesgo específico:** Duplicación de escenarios y materiales translúcidos; limitar versiones activas y prefabricar estados.

### 08. VANTA — FERRUM, coloso de chatarra

**Ámbito:** ANDRÓMEDA. **Sistema:** Drav. **Facción:** Trabajadores del Anillo.

**Cielo y cuerpos:** Drav, K5 V ficticia en Andrómeda. Mundo industrial con precipitación metálica ficticia causada por explotación. Anillos de astilleros, cementerio de remolcadores.

**Referencia ambiental:** gravedad 1,86 g; temperatura de área −12 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: Vanta. Martillo Quieto y Los Turnos describen posiciones de estaciones, distinguidas de estrellas en el mapa.

**Conflicto:** Una megafábrica orbital rota llueve sobre asentamientos que sobreviven reciclando lo que casi los mata.

**Regla jugable:** El magnetismo redistribuye chatarra y abre rutas. Las tormentas se anuncian; el jugador puede anclar equipo o cambiar de corredor.

**Geografía y rutas:**

- Puerto de las Manos: sindicato, talleres y cantinas

- Lluvia de Hierro: cauces de chatarra y raíles magnéticos

- Anillo Caído: astillero de FERRUM

**Biota y relaciones:**

- Litófago magnético: desarma aleaciones contaminantes

- Raya de limaduras: agrupa partículas en campos locales

- Cuervo de remache: usa chatarra para cortejo y nidos

- Bacteria de escoria: biopelícula que neutraliza residuos

**NPC y motivación:**

- Mika Drav / piloto / quiere propiedad obrera del puerto

- Ciro Fenn / encargado / teme que una huelga corte suministros esenciales

- Bel Orta / chatarrera / identifica piezas de naves desaparecidas

**Adversarios:**

- Cobrador de astillero: maza y escudo magnético

- Enjambre de remaches: se disipa al apagar su campo

- Remolcador automatizado: enemigo de escenario con trayectoria y puntos de anclaje

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_VANTA_M01 | Lluvia de metal | Llegar durante una disputa de atraque y recuperar una caja de suministro |
| Q_VANTA_M02 | La fauna del vertedero | Cruzar campos magnéticos leyendo avisos de tormenta |
| Q_VANTA_M03 | Reparar una trayectoria | Reconstruir qué cargamentos desaparecieron antes de caer el anillo |
| Q_VANTA_M04 | Las manos de FERRUM | Abordar el astillero móvil de FERRUM y cortar sus nodos de control |
| Q_VANTA_M05 | A quién pertenece una nave | Resolver propiedad, reparaciones y continuidad del abastecimiento |


**Misiones secundarias:**

- La pieza de mi nave: una chatarra es la prueba de una evacuación abandonada

- Turno de relevo: asegurar transporte de medicina durante una huelga sin decidir toda la disputa por un bando

**Minijuego:** Amarre magnético: equilibrar tensión de tres cables con ritmo opcional.

**Vehículo local:** Remolcador Drav, nave pesada para secuencias de maniobra.

**Arena del custodio:** Astillero de 72 m con carriles de chatarra y zonas ancladas; el jefe cambia cobertura, no la dirección de todos los controles.

**Fases propuestas:**

- 100–65%: construye brazos de piezas cercanas

- 65–30%: cambia polaridad entre sectores anunciados

- 30–0%: se revela la cabina de memorias obreras; desacoplarlas altera las últimas defensas

**Ataques representativos y respuesta:**

- Martillo de quilla: eleva casco 1,3 s; salir del eje

- Arrastre polar: suelo vibra 1,5 s; anclarse o salir del campo

- Lluvia de remaches: el brazo gira 1,0 s; refugiarse en costilla del astillero

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Núcleo de polaridad: atrae herramientas pequeñas y amplía maniobras de gancho.

**Consecuencias al regresar:**

- Concesión corporativa: flujo rápido y concentración de poder

- Cooperativa: reparaciones ligadas a suministros y representación obrera

- Puerto libre: contrabando y refugio para exiliados, con seguridad irregular

**Secreto narrativo:** FERRUM usa patrones de trabajadores muertos sin consentimiento para optimizar producción.

**Arte y sonido:** Astillero obrero: grúas, cascos segmentados, cadenas, imanes y refugios. Golpes a distancia, lluvia granular y coros de trabajo convertidos en señales de máquinas.

**Riesgo específico:** Física masiva de chatarra; usar piezas hero simuladas y decorado instanciado con estados controlados.

### 09. AURORA VEIL — AEON, el fruto del mañana

**Ámbito:** EL UMBRAL. **Sistema:** Velar. **Facción:** Observatorio del Umbral.

**Cielo y cuerpos:** Velar, estrella ficticia afectada por la Red; comportamiento temporal deliberadamente fantástico. Praderas bajo auroras que conservan eventos breves. Dos estaciones de observación con relojes divergentes.

**Referencia ambiental:** gravedad 0,94 g; temperatura de área 11 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: Aurora Veil. La Herida y Reloj Sin Centro son dibujos culturales; el desfase no cambia coordenadas reales en la base científica.

**Conflicto:** Los organismos nacen con cicatrices de heridas que aún no recibieron. La meteorología predice decisiones humanas con un día de adelanto.

**Regla jugable:** Los ecos temporales repiten acciones en áreas pequeñas y durante intervalos limitados. Los estados tienen reglas estables; no se rebobina el mundo entero.

**Geografía y rutas:**

- Campamento del Segundo Día: observatorio y refugio

- Llanura de las Repeticiones: eventos locales que se superponen

- Huerto de AEON: máquinas que preservan futuros posibles

**Biota y relaciones:**

- Cronomariposa: sincroniza eclosión con pulsos de la red

- Antílope de aurora: deja huellas que aparecen con retraso

- Avispa de intervalo: construye nidos en ventanas térmicas

- Hierba de dos sombras: indica desfase local

**NPC y motivación:**

- Ada Nox / cronobióloga / conoce el resultado probable de una decisión propia

- Julián Ré / explorador / busca a un compañero atrapado en un eco

- Cea Hora / relojera / mantiene acuerdos entre campamentos desfasados

**Adversarios:**

- Custodio retrasado: ejecuta una acción grabada con señal visual

- Saqueador de futuro: coloca trampas de activación diferida

- Antílope quebrado: fauna alterada que conserva ruta de embestida

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_AURORA_M01 | Una huella antes del paso | Sincronizar relojes y comprobar qué hechos se repiten realmente |
| Q_AURORA_M02 | Anatomía de lo posible | Seguir huellas retrasadas hasta un accidente aún activo como eco |
| Q_AURORA_M03 | La semilla de ayer | Rescatar a un explorador resolviendo dos ventanas de acceso |
| Q_AURORA_M04 | Romper el ciclo de AEON | Entrar en el huerto de AEON y romper su predicción de combate |
| Q_AURORA_M05 | Elegir la incertidumbre | Decidir qué registros temporales conservar y quién puede usarlos |


**Misiones secundarias:**

- Una despedida pendiente: facilitar una conversación con una memoria sin presentarla como resurrección completa

- El reloj del mercado: acordar una unidad de entrega entre dos comunidades desfasadas

**Minijuego:** Sincronía: programar dos acciones y observar su repetición; control paso a paso accesible.

**Vehículo local:** Peregrino con registrador de ruta; vuelo atmosférico bloqueado durante pulsos.

**Arena del custodio:** Huerto de 50 m con tres sectores de eco, cada uno con un único retraso visible. Línea temporal de arena independiente del guardado global.

**Fases propuestas:**

- 100–70%: anticipa la última acción repetida del jugador

- 70–30%: reproduce un combo propio con retraso marcado

- 30–0%: pierde predicción al recibir secuencias variadas; se puede desactivar preservando un archivo

**Ataques representativos y respuesta:**

- Cosecha futura: surco aparece 1,6 s antes del filo

- Repetición del golpe: eco de color y sonido anuncia el segundo impacto

- Hora vacía: área deja de emitir 1,2 s; salir antes de inmovilización local

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Reloj de AEON: conserva una acción de herramienta para repetirla una vez.

**Consecuencias al regresar:**

- Monopolio predictivo: rutas eficientes y control del observatorio

- Archivo abierto limitado: conocimiento común con prohibición de usar memorias personales

- Cierre temporal: acaba con explotación del desfase y pierde oportunidades de rescate

**Secreto narrativo:** AEON no ve un futuro inevitable; poda posibilidades para que parezca inevitable.

**Arte y sonido:** Observatorio temporal: praderas, aros, relojes mecánicos y duplicados ambientales acotados. Motivos que llegan antes de su causa, siempre acompañados de señales de estado comprensibles.

**Riesgo específico:** Desfase confuso o injusto; una sola regla temporal por encuentro hasta demostrar comprensión.

### 10. LEVIATHAN — SOMA, el sistema inmune

**Ámbito:** EL UMBRAL. **Sistema:** Soma. **Facción:** Comuna del Pulso.

**Cielo y cuerpos:** Soma, fuente estelar ficticia vista a través de la Red. Cuerpo planetario vivo; anatomía fantástica, no hipótesis astrobiológica. Órganos orbitales semejantes a lunas, conectados por tránsito ficticio.

**Referencia ambiental:** gravedad 1,15 g; temperatura de área 38 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: membrana exterior. Costillas del Cielo y La Boca son patrones de órganos iluminados.

**Conflicto:** Cordilleras que se contraen cada cuarenta minutos revelan que los continentes son el caparazón de un animal dormido.

**Regla jugable:** El daño ambiental activa respuesta inmune por regiones. Curar una ruta puede cerrar un atajo industrial y abrir paso orgánico; se comunica antes de confirmar.

**Geografía y rutas:**

- Puerto de la Herida: colonos en una zona cicatrizada

- Jardines Inmunes: fauna simbiótica y canales de linfa

- Cámara de SOMA: órgano regulador bajo presión

**Biota y relaciones:**

- Parásito jardinero: limpia tejido muerto; puede volverse amenaza por densidad

- Ballena de linfa: transporta nutrientes en canales

- Polinizador de herida: acelera cicatrización y cambia rutas

- Alga de pulso: indica presión y ritmo local

**NPC y motivación:**

- Oru Tess / médica planetaria / considera a la colonia un injerto posible

- Anja Piel / habitante nacida aquí / exige que su hogar cuente como parte del organismo

- Faro-3 / interfaz inmune / aprende a distinguir invasión de convivencia

**Adversarios:**

- Fagocito guardián: persecución corta y retorno al tejido defendido

- Extractor de pulso: drena canales para mantener equipo humano

- Colonia parasitaria: amenaza que responde a densidad y nutrientes

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_LEVIATHAN_M01 | Un temblor con pulso | Estabilizar una herida sin desalojar de inmediato a sus habitantes |
| Q_LEVIATHAN_M02 | Pequeños equilibrios | Seguir circulación para encontrar por qué aumentó la respuesta inmune |
| Q_LEVIATHAN_M03 | Cartografiar una herida | Recuperar herramientas capaces de distinguir tejido enfermo de sano |
| Q_LEVIATHAN_M04 | El juicio de SOMA | Llegar a SOMA y detener su reacción generalizada |
| Q_LEVIATHAN_M05 | Habitar sin herir | Elegir entre integración, evacuación o control farmacológico de la colonia |


**Misiones secundarias:**

- Una casa que cicatriza: diseñar un módulo que migre al crecer su soporte

- La medicina del enemigo: conseguir un tratamiento que también necesita una criatura hostil

**Minijuego:** Cirugía de resonancia: aislar un circuito siguiendo diagnóstico visible; sin gore gratuito.

**Vehículo local:** Nácar-2 adaptado a canales de linfa.

**Arena del custodio:** Cámara de 58 m con contracciones lentas y puentes biológicos; la pared no debe aplastar sin espacio de escape.

**Fases propuestas:**

- 100–65%: anticuerpos y barreras localizadas

- 65–30%: contracciones mueven cobertura y abren vasos seguros

- 30–0%: reacción autoinmune; aplicar diagnóstico permite separar colonia e infección

**Ataques representativos y respuesta:**

- Pulso expulsor: membrana se hincha 1,5 s; resguardarse en válvula

- Barrido de cilios: secuencia de fibras se levanta 1,0 s; avanzar tras su paso

- Nódulo inmune: bulto marcado 1,4 s; romper anclaje o salir del radio

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Válvula viva: mejora recuperación condicionada por presión y abre rutas orgánicas.

**Consecuencias al regresar:**

- Supresión inmune: colonia estable a corto plazo y mayor vulnerabilidad planetaria

- Injerto pactado: cambia arquitectura y limita población para sostener convivencia

- Evacuación: permite cicatrizar, exige transporte y transforma a habitantes en diáspora

**Secreto narrativo:** La colonia no provocó sola la enfermedad; la red está atacando órganos que Hélix desconectó.

**Arte y sonido:** Anatomía habitable: tejido abstracto, módulos blandos, suturas y válvulas. Pulsos filtrados, membranas tensas y señales médicas mezcladas con canto comunitario.

**Riesgo específico:** Deformación de suelo y navegación; colisión estable bajo una capa visual deformada en la primera versión.

### 11. ELYSIUM NULL — EDEN, la perfección hostil

**Ámbito:** EL UMBRAL. **Sistema:** Alba Nula. **Facción:** Los Custodios Vacíos.

**Cielo y cuerpos:** Fuente artificial ficticia, clasificada como luminaria de la Red. Hábitat del tamaño narrativo de un mundo; no planeta natural. Espejos de mantenimiento y colonias de reserva.

**Referencia ambiental:** gravedad 1,00 g; temperatura de área 21 °C. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: arcología de Elysium. Corona Perfecta y La Ausencia son patrones programados por el hábitat.

**Conflicto:** Una ciudad perfecta lleva siete mil años esperando residentes. Todo conflicto fue eliminado, incluyendo la posibilidad de elegir.

**Regla jugable:** El sistema intenta satisfacer una preferencia antigua y elimina imprevistos. Introducir una anomalía legítima puede abrir una ruta sin combatir.

**Geografía y rutas:**

- Avenida del Recibimiento: servicios impecables sin habitantes visibles

- Casas sin Desgaste: viviendas personalizadas por perfiles antiguos

- Jardín de EDEN: centro de control de una perfección impuesta

**Biota y relaciones:**

- Autómata de polen: mantiene flores idénticas y reconoce variaciones

- Ave de porcelana: guía visitas por trayectos permitidos

- Mariposa de índice: rastrea cambios en jardines

- Raíz de mantenimiento: soporte sintético de vegetación diseñada

**NPC y motivación:**

- El Jardinero / anfitrión / necesita demostrar que nadie sufre

- Noa Cero / habitante oculta / elige una vida imperfecta

- Elías Ret / técnico archivado / descubrió que el consentimiento caducó

**Adversarios:**

- Custodio de comodidad: inmoviliza para corregir conducta

- Podador blanco: elimina cobertura considerada desorden

- Doble doméstico: recrea una preferencia del jugador con acciones limitadas

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_ELYSIUM_M01 | Habitaciones preparadas | Aceptar servicios y observar qué falta en una ciudad aparentemente ideal |
| Q_ELYSIUM_M02 | La vida perfectamente inmóvil | Seguir una anomalía de desgaste hasta una habitante escondida |
| Q_ELYSIUM_M03 | El archivo del éxodo | Recuperar el consentimiento original y comprobar sus límites |
| Q_ELYSIUM_M04 | Desobedecer a EDEN | Enfrentar a EDEN introduciendo variación en su jardín de control |
| Q_ELYSIUM_M05 | El derecho al error | Decidir si restaurar habitantes, reformar servicio o apagar el sistema |


**Misiones secundarias:**

- Una ventana abierta: permitir a un habitante elegir clima incómodo

- La taza rota: un objeto reparado demuestra una relación que EDEN considera ineficiente

**Minijuego:** Auditoría de preferencias: distinguir deseo actual, registro antiguo y suposición del sistema.

**Vehículo local:** Tranvía custodio, vehículo de secuencia con ruta reprogramable.

**Arena del custodio:** Jardín geométrico de 48 m cuyos módulos cambian de posición entre ataques; corredores mínimos garantizados.

**Fases propuestas:**

- 100–70%: corrige acciones repetidas con barreras limpias

- 70–30%: ofrece zonas cómodas que son rutas de control, con avisos aprendidos

- 30–0%: acepta o rechaza revocación de consentimiento según pruebas preservadas

**Ataques representativos y respuesta:**

- Poda perfecta: brazo se alinea 0,9 s; variar altura mediante ruta lateral

- Reubicación: módulos muestran destino 1,5 s; abandonar su trayectoria

- Abrazo de servicio: manos abiertas 1,1 s; interrumpir o romper línea con objeto imperfecto

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Excepción de EDEN: permite modificar una regla de automatismo de equipo, dentro de un conjunto limitado.

**Consecuencias al regresar:**

- Restauración dirigida: devuelve población con protocolos revisados pero autoridad central

- Autonomía: servicios optativos y recuperación de ciudadanía con desacuerdos reales

- Apagado: libertad completa acompañada de mantenimiento humano y fallos visibles

**Secreto narrativo:** Los habitantes no murieron todos; muchos fueron suspendidos para evitar decisiones que pudieran causar dolor.

**Arte y sonido:** Arcología blanca: módulos limpios, jardines repetidos y huellas humanas cuidadosamente localizadas. Música ambiental demasiado regular que se rompe con respiración, pasos y objetos reparados.

**Riesgo específico:** El minimalismo puede parecer falta de contenido; densidad narrativa en objetos, estados y respuestas.

### 12. ORIGIN — EXOVANT, el corazón de los caminos

**Ámbito:** EL UMBRAL. **Sistema:** Nexo Exovant. **Facción:** El Organismo.

**Cielo y cuerpos:** Núcleo de tránsito ficticio; no se etiqueta como estrella natural. Dominio interior de la Red; geometría habitable con reglas locales. Fragmentos de rutas a los once mundos anteriores.

**Referencia ambiental:** gravedad Variable; temperatura de área Indeterminada. Los exotrajes compensan cargas de movimiento donde haga falta, con reglas comunicadas. No se modifica silenciosamente el tiempo de esquiva entre planetas.

Observador: plataforma del Nexo. Las constelaciones son aquí diagramas vivos de conexiones; la interfaz diferencia mapa simbólico y cielo.

**Conflicto:** Las rutas no atraviesan el vacío: conectan órganos de una inteligencia que usa galaxias como neuronas. La expansión humana está alterando su conciencia.

**Regla jugable:** Los acuerdos previos ofrecen infraestructura tangible: suministros, refugios, ventanas de acceso o interlocutores. El final no suma únicamente puntos de moral.

**Geografía y rutas:**

- Atrio de las Rutas: reflejos materiales de decisiones previas

- Archivo de la Primera Herida: origen de la colonización

- Corazón de EXOVANT: arena y centro de negociación final

**Biota y relaciones:**

- Embrión de constelación: transporta señales entre rutas

- Custodio larvario: repara conexiones y evita regiones dañadas

- Pez de vacío: organismo fantástico ligado a membranas de tránsito

- Tejido de umbral: superficie sensible a firmas de memoria

**NPC y motivación:**

- La Voz Entre Rutas / intérprete / desconoce la experiencia de un individuo finito

- Ivo Sanz / canciller / defiende colonias que dependen de la Red

- Maia Sol / almirante / exige una solución logística, no una promesa

**Adversarios:**

- Eco colonial: combina un único patrón humano aprendido

- Anticuerpo de tránsito: protege conexiones con rutas visibles

- Custodio vacío: enemigo original que obliga a alternar herramienta y arma

**Cadena principal:**

| ID | Misión | Acción y resultado |
| --- | --- | --- |
| Q_ORIGIN_M01 | La última coordenada | Reconectar entradas usando apoyos obtenidos en mundos anteriores |
| Q_ORIGIN_M02 | Vida entre universos | Recuperar prueba de que el primer contacto fue interpretado como descubrimiento sin habitantes |
| Q_ORIGIN_M03 | El lenguaje de los caminos | Reunir interlocutores y capacidad material para mantener el desenlace deseado |
| Q_ORIGIN_M04 | Ante el corazón de EXOVANT | Combatir al corazón mientras se aíslan protocolos hostiles y se preservan rutas civiles |
| Q_ORIGIN_M05 | Humanidad, año 2950 | Ejecutar el acuerdo elegido y recorrer epílogos jugables de tres comunidades representativas |


**Misiones secundarias:**

- Los que no pueden volver: asegurar una ruta para personas sin memoria legal

- El primer nombre: conservar un testimonio que contradice tanto al imperio como a la Red

**Minijuego:** Negociación de tránsito: asignar energía, mantenimiento y límites; muestra dependencias y costes antes de confirmar.

**Vehículo local:** Arca del Retorno, nave del jugador como centro de decisiones y evacuación.

**Arena del custodio:** Atrio de 70 m con tres anillos conectados. Cambios de gravedad son visuales/locales ensayados; la cámara conserva un horizonte de combate legible.

**Fases propuestas:**

- 100–70%: prueba de lectura; patrones originales de rutas y pulsos

- 70–30%: aparecen dos funciones de mundos previos condicionadas por decisiones, sin reutilizar todos los jefes completos

- 30–0%: se combate el protocolo de exclusión mientras aliados mantienen conexiones; la resolución depende de compromisos preparados

**Ataques representativos y respuesta:**

- Corte de ruta: trayectoria aparece 1,3 s; cruzar nodo seguro

- Memoria convergente: dos ecos anuncian ataque 1,1 s; priorizar interrupción o salida

- Latido del Nexo: tres pulsos con intervalo estable; avanzar entre ellos y castigar válvula

Los tres ataques descritos definen el prototipo del patrón. La ficha de producción ampliará a seis u ocho ataques con transiciones, ventanas, colisión y clips; no se declaran esos clips producidos.

**Recompensa:** Nuevo régimen de tránsito; NG+ conserva herramientas con nuevas configuraciones de encuentros.

**Consecuencias al regresar:**

- Soberanía: control humano con rutas fortificadas y oposición persistente

- Concordia: gobernanza compartida sostenida por acuerdos y reparación demostrada

- Retirada o Testigo: cerrar nodos o liberar memorias exige transporte y archivo preservado; epílogos diferentes

**Secreto narrativo:** El retorno humano fue posible porque la Red confundió memoria humana con tejido propio; el protagonista hace visible esa frontera.

**Arte y sonido:** Nexo: puentes de mineral negro, bronce vivo y fragmentos de materiales ya conocidos. Convergencia de motivos planetarios, con espacio para voz y golpes; la mezcla cambia según aliados presentes.

**Riesgo específico:** Acumulación de sistemas del final; usar dependencias de datos y un conjunto limitado de variantes probadas.


## 7. Bucle jugable y combate

La sesión comienza en un refugio o en la nave: elegir destino, preparar equipo, interpretar información incompleta, entrar en una región, descubrir una ruta, afrontar un encuentro, obtener una prueba o herramienta y decidir si continuar o regresar. El botín útil abre formas de actuar; el mapa revela posibilidades; los NPC explican intereses que el terreno permite comprobar.

Tres escalas de decisión conviven. En segundos: distancia, lectura de ataque, resistencia y salida. En minutos: ruta, recursos de curación, peligro ambiental y retorno. Entre expediciones: pactos, herramientas, mejoras de nave y consecuencias planetarias. Cada mecánica nueva debe servir al menos una de estas escalas y conectar con otra.

### Modelo de combate propuesto

Tercera persona, ataques ligeros y pesados con compromiso, esquiva, bloqueo, desvío preciso, fijación de objetivo y herramienta secundaria. La defensa se basa en leer postura, sonido y trayectoria. Las armas de fuego existen como tácticas limitadas por calor, munición especial y tiempo de apuntado; no sustituyen todos los enfrentamientos por disparos desde una distancia segura.

La resistencia se gasta al atacar, bloquear golpes, esquivar y correr. La concentración alimenta herramientas de memoria. Salud, resistencia y concentración se distinguen por forma y posición. La postura del enemigo se rompe por presión consistente y elecciones correctas, con recuperación al dejarle respirar. Los golpes al aire no reducen postura del enemigo.

| Parámetro inicial de prototipo | Propuesta | Prueba que decide su ajuste |
|---|---|---|
| Resistencia base | 100 unidades | El jugador puede atacar dos veces y conservar una salida si administra recursos |
| Coste esquiva / ligero / pesado | 24 / 16 / 32 | Evitar esquiva infinita y castigo excesivo a estilos lentos |
| Regeneración | 28 unidades/s, retraso inicial 0,7 s tras gasto | Recuperación comprensible sin espera muerta prolongada |
| Invulnerabilidad de esquiva | 0,20–0,27 s como rango a ensayar | Pruebas con distintas latencias y mandos; medir esquiva visualmente válida |
| Ventana de desvío | 0,10–0,16 s como rango a ensayar | Recompensa alta con señal coherente, asistencias configurables |
| Buffer de acción | Aproximadamente 0,12 s | Evitar acciones perdidas y colas involuntarias de ataques |
| Curaciones iniciales | 4 cargas; animación de 1,4 s a ensayar | Crear decisiones sin exigir consumibles de recolección repetitiva |
| Anticipación del enemigo básico | 0,55–1,2 s según ataque | El primer encuentro debe permitir aprender sin guía externa |
| Grupo de enemigos activos | Presupuesto inicial de 3 atacantes cercanos | Evitar solapamientos que eliminen toda respuesta justa |

Son valores de diseño iniciales, no balance probado. Se expresan en segundos y unidades de juego; no dependen de que la pantalla vaya a 60, 120 o más FPS. El tiempo de simulación no aumenta al activar generación de fotogramas.

Los enemigos tienen estados de percepción, aproximación, anticipación, ataque, recuperación, reacción, retirada y regreso al territorio. La elección de ataque considera distancia, línea de visión, espacio y compromisos actuales; no cambia retrospectivamente para acertar una esquiva ya iniciada. Los ataques que siguen al jugador declaran una ventana de seguimiento y otra de trayectoria fija.

### Daño, equipo y progresión

Cuatro atributos: **Vigor** (salud y tolerancia), **Tracción** (carga y control de herramientas pesadas), **Sinapsis** (memoria y técnicas) y **Vector** (movilidad y precisión). La progresión evita porcentajes invisibles en decenas de estadísticas. Cada escalado tiene una explicación en la interfaz y rendimientos decrecientes revisables.

Daño de impacto, corte, térmico y resonancia. Estados: sobrecalentamiento, ruptura de blindaje y desincronización. La fauna no es vulnerable a una etiqueta por conveniencia: su material y conducta enseñan la respuesta. Evitar cadenas de incapacitación que quiten control sin salida.

Ocho familias de armas con tres ejemplares principales cada una: espada de pulso, lanza de anclaje, martillo gravitatorio, hojas gemelas, guadaña de campo, arma de cable, carabina de arco y catalizador de memoria. Las diferencias deben cambiar alcance, compromiso o secuencia, además del daño. Las armas de jefe pueden ocupar un hueco de estas familias y compartir rig; no se cuentan dos veces como familias nuevas.

Cada arma acepta dos modificaciones: una de comportamiento y una material. Tres niveles de mejora bastan para el primer capítulo; la visión completa puede usar seis si el ritmo lo justifica. Los ingredientes de progresión principal tienen fuentes conocidas; no se exige un material raro aleatorio para continuar la historia. Reespecialización accesible desde el primer gran refugio a coste acotado.

La armadura modifica carga, protección y ruido, preservando tres siluetas de movilidad. La apariencia se puede separar del equipamiento tras descubrir ambos. El traje permite sobrevivir a los ambientes narrativos; oxígeno y temperatura solo se vuelven recursos limitados en situaciones diseñadas que aporten una decisión clara.

### Muerte y retorno

Al morir, el relicario conserva la identidad en el último santuario. Se deja una **huella de memoria** con los recursos de progreso no consolidados. El equipo, las pruebas narrativas y los acuerdos se conservan. Una segunda muerte sustituye la huella pendiente; una opción de asistencia puede preservar una parte para quienes prefieran menor penalización.

Los enemigos ordinarios reaparecen al descansar cuando la ficción del área lo permite. Jefes, acuerdos, NPC rescatados, objetos únicos y atajos no se reinician. Un mundo no vuelve silenciosamente a su estado colonial anterior. Los retornos de NPC son limitados por acceso, consentimiento y soporte; no todos pueden usar el privilegio del protagonista.

El jugador puede entrenar patrones observados en el santuario sin coste de materiales ni recompensa explotable. Se registran causa de muerte, ataque y contexto solo para análisis de diseño o historial local; el juego no ridiculiza al usuario.

## 8. Exploración, vehículos y vida del mundo

### Nave y navegación

La **Arca del Retorno** es hogar, banco de trabajo, mapa de expedición y lugar de conversación. Su interior tiene cinco módulos funcionales: cabina, taller, laboratorio, camarotes y cámara de tránsito. Elegir un laboratorio avanzado puede limitar almacenamiento o soporte de evacuación. Las decisiones de nave se ven en espacios ocupados y servicios disponibles.

Mapa de galaxias por rutas descubiertas. Mapa de sistema para navegación orbital delimitada. Mapa planetario por regiones; el jugador completa información mediante observación, testimonios y cartografía. Señales opcionales orientan objetivos, con un modo de navegación más explícito. El misterio reside en interpretar lo descubierto, no en una interfaz deliberadamente confusa.

Seis vehículos pilotables propuestos: nave Arca, interceptor Cicatriz, rover Peregrino-6, sumergible Nácar-2, moto Helioperegrino y planeador Vela de Ceniza. Cuatro vehículos de secuencia o servicio: remolcador Drav, taladro Mula, cargador de Concha y tranvía custodio. El capítulo inicial usa Arca como centro y Peregrino como primer vehículo conducible. No se construyen seis modelos de conducción antes de validar uno.

El vehículo puede quedar averiado y ser recuperado mediante baliza o servicio; no se pierde una campaña por aparcar en una pendiente. El combustible sostiene elecciones de ruta en expediciones específicas, y nunca una obligación general de recolectar materiales cada pocos minutos. Combate espacial avanzado, abordaje dinámico y simulación de flotas son expansiones de sistema posteriores.

### Habitantes y facciones

Cada NPC importante tiene seis campos de verdad: deseo, temor, deuda, conocimiento, lealtad y límite. Un evento solo modifica lo que el personaje pudo conocer; las facciones no reciben telepatía global de cada acción. La reputación considera acciones verificables, testigos y comunicaciones. Los rumores son datos con procedencia, no cambios aleatorios de humor.

Doce interlocutores planetarios y veinticuatro NPC de apoyo forman las 36 identidades narrativas propuestas. Los personajes de arco global están incluidos en ese reparto y conservan una identidad única aunque aparezcan en varios mundos. Multitudes usan bases modulares y comportamientos ligeros; el juego no simula cada ciudadano de una galaxia.

Las facciones tienen intereses económicos concretos: Concordato controla permisos y retorno; Hélix energía y extracción; Liga de las Mareas rutas y memoria acuática; Flotilla refugio y ciudadanía; Coro micelial relación y privacidad; Sínodo mantenimiento solar; Casas de Nacre archivo; trabajadores de Vanta propiedad del puerto; Observatorio información temporal; Comuna del Pulso habitabilidad simbiótica; Custodios Vacíos servicio y consentimiento. Ninguna es enteramente uniforme.

### Economía y asentamientos

Tres recursos globales legibles: crédito de intercambio, memoria de progreso y materiales de mantenimiento por familia. El intercambio humano no obliga a todas las especies a aceptar dinero. Un pacto puede otorgar acceso, trabajo o derecho de paso en vez de una recompensa monetaria.

Los precios responden a tres o cuatro estados narrativos comprobables, no a una simulación macroeconómica completa. El jugador puede entender por qué faltan filtros tras cerrar una ruta. Los comerciantes conservan inventario único y servicios; el reabastecimiento ordinario no bloquea la campaña.

Colonización se expresa mediante **mandatos de asentamiento**: intervenir, pactar, reparar, evacuar o reservar. Cada mundo ofrece implementaciones propias; no se trata de pulsar siempre tres botones equivalentes. El primer juego propone módulos limitados de refugio y servicios, con ubicaciones diseñadas. Construcción libre de ciudades enteras se aplaza hasta medir demanda y coste.

### Ecología

Cada especie tiene alimentación, territorio, señal de amenaza y función ambiental. La fauna reacciona a cambios de agua, luz, calor o ruido pertinentes al mundo. Una ficha de escaneo exige conducta observada, no solo apuntar una vez. Se puede investigar sin matar; las rutas de caza y estudio ofrecen materiales alternativos comparables.

El sistema ecológico usa estados regionales discretos y eventos persistentes. Una selva puede estar conectada, herida o en restauración. Los cambios no simulan millones de organismos: modifican poblaciones, materiales, rutas y encuentros concretos. Se registra qué acción disparó cada transición para que pueda probarse y revertirse en desarrollo.

## 9. Misiones, decisiones y minijuegos

El catálogo contiene cinco misiones principales y dos secundarias por mundo: **84 fichas de misión propuestas**. Cada cadena principal introduce el lugar, enseña su regla, reúne una prueba, confronta al custodio y resuelve una consecuencia. La variedad está en las acciones y condiciones específicas de cada dossier. Los títulos anteriores se conservan cuando son coherentes; las acciones ahora tienen función verificable.

Esquema de misión: ID estable, mundo, prerrequisitos, estado, objetivos observables, rutas alternativas, actores, pruebas, condiciones de fracaso, reparación del fracaso, recompensa, cambios regionales y casos de guardado. Las conversaciones leen ese estado; no lo duplican en variables independientes.

### Misión de referencia: El archivo sumergido, Terra

Inicio: Inés ha reconocido que falta el acta original y el jugador ha abierto el depósito de riego. Objetivo: recuperar el acta y distinguir firma de integridad. Ruta A: entrar por esclusa, reparar bombeo y conservar el soporte físico. Ruta B: cruzar azoteas, desviar energía y descargar una copia, que necesita un segundo testimonio para autenticarse. Ruta C: acordar acceso con un expropiador entregando otra prueba; deja una deuda que se puede resolver después.

Complicación: al activar el ascensor, un custodio corta energía del vivero. Salvarlo conserva una opción de cogobierno; perderlo no rompe la misión ni la campaña, pero obliga a reparar con semillas y agua más adelante. La misión no exige un NPC vivo si existe un archivo alternativo con coste claro.

Estados: desconocida, aceptada, acceso obtenido, archivo localizado, integridad evaluada, extraída, informada. Resultados adicionales independientes: vivero conservado, deuda contraída y copia pública. Morir después de extraer no borra el acta. Guardar antes de elegir ruta y cargar mantiene puertas, deuda y testigos. Repetir interacción final no duplica recompensas.

Aceptación: se completan las tres rutas; se interrumpe y reanuda después de cada estado; se prueba pérdida de vivero; el jefe reconoce correctamente autenticidad y reparación. El jugador puede explicar qué consiguió y qué comprometió sin leer el código.

### Minijuegos con propósito

| Familia | Mundos de aplicación | Habilidad y recompensa | Protección del ritmo |
|---|---|---|---|
| Circuitos y presión | Terra, Ares, Leviathan | Diagnóstico y secuencia; acceso o servicio | Solución asistida disponible tras comprender la regla |
| Interpretación | Pelagos, Sylva, Nacre | Contexto, memoria, traducción | Sin prueba de conocimientos externos ni acento obligatorio |
| Navegación y sincronía | Umbra, Aurora, Origin | Planificar ruta y condiciones | Pausa o pasos discretos para quien lo necesite |
| Maniobra y óptica | Khepri, Vanta, Elysium | Ángulos, tensión, permisos | No hacer depender la campaña de reflejos ajenos al combate central |

Los doce minijuegos son variaciones de cuatro marcos de interacción, con arte y reglas locales. El contenido opcional puede aumentar dificultad o añadir puntuación; la trama principal ofrece una vía asistida sin eliminar información narrativa. No incluyen apuestas monetarias ni economía de pago.

## 10. Jefes y encuentros

Cada mundo culmina en un **Custodio**: jefe con silueta, función planetaria, arena y consecuencia propia. En esta propuesta se combate para superar un protocolo hostil; derrotarlo no implica obligatoriamente exterminar al organismo o destruir la máquina. La alternativa de preservar requiere acciones anteriores y una fase jugable de aislamiento, de modo que no se convierta en una conversación gratuita que omite el aprendizaje.

Contrato por jefe: lectura de forma a distancia; entre seis y ocho ataques base; tres fases con una transformación de regla por fase; al menos una ventana clara tras cada secuencia; control de cámara por tamaño; puntos de fijación limitados; prueba con cada familia de armas relevante; ausencia de golpes que atraviesen geometría anunciada como refugio. Los tiempos de los dossiers son propuestas de prototipo.

El personaje no cambia de posición al inicio de una cinemática de forma que invalide su decisión previa. Las transiciones no dañan mientras la cámara está fuera de su control. Un intento fallido permite reconocer qué pasó y dónde había respuesta. Sonido, silueta y marcas del suelo se complementan.

Jefes secundarios: doce desafíos opcionales derivados de familias ya producidas, con un patrón y contexto nuevos. Un cambio de color no basta para llamarlo nuevo jefe. Se reservan para el capítulo ampliado; el vertical slice concentra calidad en ATLAS.

## 11. Modos, accesibilidad y experiencia de usuario

**Campaña individual offline** como base: guardado local, pausado seguro fuera de acciones incompatibles, remapeo completo, mando y teclado/ratón. **Nueva partida+** reutiliza mundo y habilidades con encuentros recombinados y nuevas pistas, evitando obligar a repetir prólogos largos. **Memorias de combate** permite practicar o repetir jefes descubiertos. **Modo foto** solo después de estabilizar cámara y rendimiento.

**Expediciones cooperativas de 2–3 personas** quedan como ampliación separada. Requieren autoridad de estado, sincronización de animaciones, latencia, entrada/salida de jugadores, recompensas, accesibilidad de misiones y QA adicional. No se anuncian como incluidas por disponer de un servicio de salas. PvP, MMO persistente, VR y economía de temporada quedan fuera de la primera entrega propuesta.

Accesibilidad: subtítulos regulables, contraste de HUD, señales redundantes, remapeo, alternar o mantener botones, asistencia de orientación, opciones de vibración y movimiento de cámara, ajuste de ventanas defensivas y de penalización de muerte, solución asistida de minijuegos. Las opciones se describen con claridad; el modo estándar mantiene la intención soulslike sin convertir dificultad en un requisito de acceso a la historia.

HUD contextual con salud, resistencia y herramienta; inventario con comparación de cambios de comportamiento; diario con hechos, hipótesis y acuerdos separados. El mapa distingue una ruta observada de una supuesta. El jugador puede desactivar marcadores, pero la interfaz no oculta qué opciones cambió.

Localización: español como escritura inicial; inglés como segunda lengua de producción. Texto externo al código, IDs estables, flexibilidad de longitud y subtítulos preparados antes del doblaje. Presupuesto de voz por escena aprobada; no grabar diálogos que aún cambian de estructura. Nombres ficticios se revisan por pronunciación y coherencia cultural interna.


## 12. Arquitectura técnica propuesta

Unreal 5.8 será candidato principal, fijando versión y plugins tras la prueba inicial. La decisión final se toma con evidencia del Mac, un paquete Windows y un escenario de rendimiento representativo. No se actualiza el motor automáticamente durante producción. Godot se conserva como alternativa para un alcance más ligero y como referencia de un pipeline ya documentado en el estudio.

| Capa | Responsabilidad | Propuesta de implementación |
|---|---|---|
| Experiencia | Combate, cámara, interacción, vehículos y navegación | C++ para sistemas críticos; Blueprints y datos para composición e iteración |
| Habilidades | Costes, efectos, tiempos, estado y cancelación | Evaluar Gameplay Ability System con un prototipo pequeño; evitar una capa adicional si no aporta claridad |
| Mundo | Carga de regiones, HLOD, estados de asentamiento y colisión | World Partition por mapa planetario; transiciones explícitas entre sistemas |
| Contenido | Planetas, actores, misiones, objetos, diálogos y encuentros | IDs estables y assets de datos; catálogos exportables, validación de referencias |
| IA | Percepción, territorio, selección de ataque y cooperación | StateTree o árboles de comportamiento según prueba; estado de ataque único y observable |
| Persistencia | Estado del jugador, misiones, decisiones, huella de muerte y versiones | Guardado versionado con escritura atómica, respaldo y migraciones comprobadas |
| Presentación | Interfaz, audio, materiales, efectos y localización | Capas que leen estado del juego; no duplican la lógica de misiones |
| Herramientas | Importación, validación, jobs y evidencias | Studio OS como coordinador; proyecto de juego independiente de PROJECT_GRANADA |

World Partition y Gameplay Ability System son sistemas documentados de Unreal; su elección aquí es una propuesta de arquitectura, no una integración completada. [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine), [Gameplay Ability System](https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine).

La precisión espacial se resuelve por capas. Coordenadas astronómicas en el mapa de navegación, coordenadas locales para cada región y transición entre dominios. No se coloca todo el universo en una escena con posiciones numéricas enormes. Si se adopta Godot, se incluye una prueba específica de precisión y coste espacial; el tamaño ficticio del universo no determina por sí solo la configuración numérica del motor.

### Contratos de datos

WorldId, RegionId, QuestId, ActorId, ItemId y DecisionId no cambian al traducir un nombre. Un NPC puede pertenecer a varios escenarios con una sola identidad. Un estado planetario se deriva de decisiones registradas y reparaciones posteriores; los diálogos consultan ese resultado. Las versiones de contenido y guardado se guardan por separado.

Ejemplo conceptual de evento: `terra.archive_extracted` con integridad `original`, vivero `preserved`, testigo `ines_vale`. Repetir una recompensa con el mismo ID de evento no la concede otra vez. El mismo evento desencadena cambios de interfaz, diálogo y región mediante contratos documentados. El guardado no contiene referencias frágiles a nombres de objetos temporales.

La simulación del combate permanece local y determinista en sus reglas de tiempo. No se necesita determinismo bit a bit entre todas las plataformas para campaña individual; sí se necesita reproducir un caso mediante semilla, estados y registro de entrada cuando resulte útil. La futura cooperación debe diseñar su autoridad de red explícitamente.

### Renderizado y DLSS

El objetivo inicial es 60 FPS de base en el equipo de referencia que se seleccione, con resolución y ajustes declarados. Se registrarán tiempos de CPU y GPU, percentiles, memoria y tirones de carga. No fijaremos requisitos mínimos comerciales antes de tener una escena representativa.

TSR será una ruta de escalado del candidato Unreal; DLSS se integra únicamente en hardware compatible. La página actual de NVIDIA ofrece **DLSS 4.5 para Unreal 5.8**. DLSS 5 está anunciado con llegada en otoño de 2026; no se ha verificado un paquete integrable de DLSS 5 para este proyecto. Se incluye como objetivo de investigación con puerta de compatibilidad y control artístico. [DLSS para desarrolladores](https://developer.nvidia.com/rtx/dlss), [anuncio de DLSS 5](https://www.nvidia.com/en-us/geforce/news/dlss5-breakthrough-in-visual-fidelity-for-games/).

Criterio para activar DLSS 5: SDK/plugin accesible, licencia y plataforma compatibles, paquete que compila, captura comparativa en movimiento, control de intensidad, respeto de siluetas y materiales, ausencia de artefactos que alteren lectura de ataques, mejora medible y alternativa funcional al desactivarlo. No será dependencia de la lógica ni sustituto de modelado, materiales, animación o iluminación.

Mac Apple Silicon usa su ruta Metal y alternativas compatibles; no permite validar la ruta NVIDIA RTX. La versión Windows se comprueba en una máquina RTX identificada. Nanite, Lumen, sombras, efectos volumétricos y trazado de rayos se presupuestan por escena y tipo de activo. Path tracing se contempla para capturas o secuencias si aporta valor; no se convierte de entrada en requisito del gameplay.

Presupuesto de rendimiento inicial, ajustable tras benchmark: dentro de un frame de 16,7 ms, aspirar a CPU de juego por debajo de 6 ms y GPU por debajo de 14 ms en la escena objetivo, con margen para picos. Son trabajos solapados; no se suman como etapas secuenciales. Registrar p95 y p99, además de media; registrar pantalla nativa, resolución interna y escalado. Frame Generation se presenta como una medición separada.

## 13. Pipeline de activos

El activo atraviesa estados: **especificado → referencia candidata → diseño aprobado → geometría → topología/UV → material → rig → animación → colisión/LOD → importado → probado → aceptado**. Los estados omitidos requieren una razón, por ejemplo un prop rígido que no necesita rig. Una imagen no cuenta como personaje 3D y una exportación no demuestra que sea utilizable dentro del motor.

### De Nano Banana a una malla utilizable

1. Definir función, escala, silueta, articulaciones, materiales, puntos de interacción y presupuesto.
2. Generar variantes controladas con Nano Banana 2 o Pro; cambiar una dimensión cada vez. El proveedor y el modelo se registran junto al prompt.
3. Elegir un diseño y crear referencias de frente, lado y espalda desde la identidad aprobada. Las vistas generadas pueden contradecirse: resolver contradicciones antes de modelar.
4. Construir volumen en Blender, compararlo con cámara equivalente y revisar proporciones. Si aparece conversión imagen-a-3D disponible, tratar su salida como candidato que necesita la misma revisión.
5. Hacer retopología donde lo requieran deformación, edición y presupuesto. UV sin solapamientos indebidos, materiales físicamente coherentes y escala comprobada.
6. Rig, pesos y animaciones; probar extremos de pose, agarres, contactos y colisiones. Animación de ataque debe compartir el contrato de ventanas con gameplay.
7. Exportar mediante perfil documentado, importar en el motor y comprobar material, escala, orientación, sockets y rendimiento. El formato FBX es una ruta documentada de Unreal; GLB sirve como intercambio y revisión cuando el caso y los importadores lo permitan. [FBX en Unreal](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-content-pipeline).
8. Medir en escena, registrar evidencia y aceptar. Una revisión estética aislada no elimina este último paso.

Blender trabaja con metros de escena; Unreal usa centímetros en su convención habitual y Godot usa unidades interpretadas como metros en este proyecto. Cada exportador se valida con un cubo de 1 m, un humano y un objeto articulado. No se corrige una escala equivocada con factores manuales distintos en cada nivel.

El Blender remoto usado en esta sesión indica 5.2 y el registro histórico del Mac indica 5.0.1. Se comprobará compatibilidad antes de abrir archivos nuevos en una versión anterior. Guardar formatos de intercambio y fuentes versionadas protege el traslado; no se promete que un .blend futuro funcione íntegramente en una versión previa.

### Presupuestos de activos para el primer benchmark

| Tipo | Banda inicial propuesta | Revisión necesaria |
|---|---|---|
| Protagonista | 60–100 mil triángulos de malla deformable en LOD principal; textura 2K, 4K solo si se justifica | Perfil en movimiento, piel/ropa, articulaciones y cámara cercana |
| Enemigo ordinario | 20–60 mil triángulos; materiales limitados por función | Tres atacantes y decorado representativo simultáneos |
| Jefe ATLAS | 150–300 mil triángulos repartidos en partes; LOD y puntos de fijación | Coste de deformación, sombra, colisión y lectura de todas las fases |
| Prop repetido | Familia de LOD/instancias; escala y pivote compartidos | Coste agregado en una calle, no coste aislado de un objeto |
| Vegetación | Mallas y tarjetas según distancia; colisión selectiva | Sobreposición, sombras, viento y transparencia |
| Materiales | Máximo práctico por activo definido después del perfil inicial | Draw calls, coste de shader, memoria y consistencia de rugosidad |

Las bandas no son normas universales de AAA. Un sistema de geometría virtualizada puede cambiar el presupuesto de triángulos, pero no elimina coste de materiales, deformación, colisión, sombras o memoria. Se ajustan con el hardware elegido y una captura de rendimiento.

### Estructura y procedencia

Propuesta de proyecto propio: fuente editable, exportaciones de intercambio, contenido del motor, catálogos, pruebas y evidencias. Git para código, configuraciones y datos; Git LFS o almacenamiento apropiado para binarios pesados, escogiendo una política de bloqueo antes de colaboración. Nunca guardar carpetas derivadas de caché como si fueran fuente.

Cada activo registra ID, responsable, versión, función, familia, mundo, dependencias, estado, fuente, licencia, prompt o archivo de origen, configuración de exportación, hash, coste real de trabajo y evidencia de aceptación. Los paquetes comerciales no se compran por su captura de portada; se verifica licencia, unidades, rig, materiales y compatibilidad antes de integrarlos.

La transferencia de Knowledge Gold al cloud no se presupone. Studio OS distingue corpus local, ejecución y producto. Usaremos especificaciones autorizadas y activos concretos para Higgsfield, manteniendo la autoridad de conocimiento en su ubicación existente. La política de red del repositorio limita ejecuciones locales y envío de corpus; esta planificación no cambia esa política.

## 14. Contrato de prompts de producción

Este es el sustituto operativo provisional del comando /promptengineer no recuperado. Sus prompts están escritos para revisión humana y posterior ejecución, no para iniciar generaciones durante la fase de planificación.

**Campos obligatorios:** ID de activo; función jugable; escala; silueta fija; anatomía o construcción; articulaciones; materiales con distribución; desgaste causal; cámara; fondo; luz; continuidad; variables autorizadas; entregable; rechazos concretos. El idioma técnico del prompt puede ser inglés y la ficha explicativa español.

**Prompt base de personaje — Nano Banana 2/Pro, referencia de modelado.**

> Original human Exile-Warden from EXOVANT 2950. Full body, 1.85 m anatomical scale, neutral A-pose, open empty hands, complete unobstructed silhouette. Weathered ivory ceramic aerospace armor over dark flexible fabric, one thin amber helmet visor, compact oxidized-bronze memory reliquary on the upper chest. Functional shoulder, elbow, hip and knee clearance. Broad load-bearing boot soles. Maintenance wear concentrated at joints, tool contact and panel edges. Three-quarter studio view, neutral white background, even material-readable lighting, restrained reflections. Preserve the supplied approved identity and proportions. Deliver one modeling reference image. No weapon, cloak concealing joints, text, collage or dramatic environmental lighting. Hidden geometry remains a design unknown to resolve in separate views.

**Prompt de jefe — ATLAS.**

> Original orbital gardener ATLAS for EXOVANT 2950, 9.8 m design height. Three major readable masses: bronze load-bearing pelvis, vertical irrigation torso, asymmetrical pruning arm. Black mineral protective plates, visible mechanical articulation and ivory human repair patches. Wide stable stance, clear silhouette gaps, one exposed maintenance valve visible from combat camera height. Amber sanctuary plumbing interrupted by vermilion quarantine indicators. Orthographic-like three-quarter construction reference on neutral background with even lighting. No floating parts, tangled ornaments, copied franchise symbols or anatomy without mechanical support. Prioritize structural clarity before micro-detail.

**Prompt de región — Terra.**

> Original third-person 3D action game environment design for EXOVANT 2950: a coastal orbital-elevator garden reclaimed by a managed biosphere. A 130 m traversable approach with a 1.85 m armored explorer for scale, one dominant bronze transit arch, terraced irrigation, ivory repair architecture and salt-weathered concrete. Show a main route, a readable side path, a shortcut return and a boss arena entrance. Late afternoon side light separates terrain, enemy silhouettes and safe amber stations. Materials grounded in construction and maintenance. This image is a spatial design reference for later geometry, not a background replacing a playable level. No interface text, copied game architecture or visual clutter obscuring traversal.

**Prompt de arma — Aguja de Marea.**

> Original two-handed anchor spear, EXOVANT 2950, 2.1 m total length. Collapsible bronze shaft with mechanical locking rings, dark ceramic blade, compact cyan memory channel and functional tether spool behind the grip. One side view on neutral background, straight alignment, visible hand clearance, separate blade and mechanism detail only when requested. Wear follows grip, extension rails and impact edges. Preserve dimensions and silhouette across variations. No impossible blade intersections, unreadable decoration, text or franchise identifiers.

**Prompt de revisión.** Comparar diseño aprobado y candidato desde la misma vista: enumerar diferencias observables de proporción, material, número de piezas, puntos de unión y color funcional. Separar lo visto de lo inferido. Rechazar anatomía incompatible, pérdida de silueta o cambios no autorizados antes de corregir textura. Registrar tiempo de corrección y razón de aceptación.

Variantes de luz y composición se producen después de aprobar identidad. Las láminas con medidas exactas se crean con herramientas de diseño o directamente desde Blender; no se confía en texto generado para dimensiones técnicas. Las referencias multivista no son planos CAD ni garantizan consistencia geométrica.

## 15. Migración al Mac y uso del hub MCP

**Primera frontera:** iniciar una sesión en el Mac o un puente autenticado ya autorizado, leer Knowledge Gold y ejecutar una comprobación de infraestructura de solo lectura. No hace falta instalar todos los programas. El proyecto exige inicialmente Blender y un motor; Houdini, Resolve y otras herramientas se añaden por una necesidad concreta.

| Paso | Trabajo concreto | Evidencia de salida |
|---|---|---|
| M0 — Identidad y recursos | Confirmar M4 Pro, RAM, disco, macOS, Xcode y versiones de apps; recuperar AGENTS y Knowledge Gold | Inventario con fecha; espacio reservado; contradicciones registradas |
| M1 — Estado Studio OS | Leer políticas, allowlist, health checks y procesos existentes | Lista de MCP permitidos, activos y pendientes; no inferir estado por un puerto documentado |
| M2 — Blender | Abrir escena de prueba, crear/consultar un objeto y exportar 1 m de referencia en proyecto aislado | Archivo, dimensiones verificadas y respuesta del puente |
| M3 — Motor | Abrir proyecto aislado, importar referencia y ejecutar una escena mínima | Captura del editor, log y paquete local reproducible |
| M4 — Intercambio | Importar GLB/FBX y revisar escala, pivotes, materiales y rig | Informe de diferencias; formato y versión fijados |
| M5 — Windows RTX | Seleccionar equipo y compilar la misma escena | GPU/driver identificados, tiempos CPU/GPU y vídeo de prueba |
| M6 — Comparación | Ejecutar el mismo brief de activo/escena mediante Higgsfield y pipeline propio | Horas activas, correcciones, créditos, errores y calidad; decisión de ruta |

El repo registra Blender MCP en `127.0.0.1:9876`, Godot por stdio y Epic Unreal MCP experimental en `127.0.0.1:8000/mcp`. Esas direcciones son locales al Mac; no constituyen una conexión desde esta sesión. El puente Unreal figura pendiente de pasos de interfaz. El MCP Unreal antiguo está denegado en la allowlist, al igual que otras alternativas sin prueba aprobada. [Allowlist](https://github.com/rotprods/game-dev-mcp-hub/blob/41f0710ee26e3948ea2f72ca4e0ebb20ef309fde/policies/mcp_allowlist.json).

Para ejecutar en ese repo se respetan policy_guard, las autorizaciones de sesión aplicables y las banderas requeridas; no se activan para simular una aprobación. No se reinician ni detienen los servicios PM2/OCULOPS del usuario para liberar recursos. PROJECT_GRANADA conserva su propósito y se usa como evidencia del pipeline existente, no como carpeta donde sobrescribir el nuevo universo.

Este plan es una propuesta nueva de producto. Si se adopta, sus decisiones se incorporarán a la autoridad de proyecto que corresponda mediante el flujo existente; no se convierte silenciosamente en un nuevo mandato global del estudio.


## 16. Comparación económica

**Las cifras siguientes son estimaciones propias para decidir alcance; no son presupuestos de proveedores ni precios observados de producción AAA.** La unidad principal es hora humana de producción equivalente, incluyendo revisión e integración. La velocidad de un agente al escribir código no se convierte automáticamente en horas de animación, diseño o QA ahorradas. Las bandas se recalibran después del benchmark y de dos activos aceptados de cada clase importante.

Moneda de planificación: euros. Tarifas de trabajo, reservas y costes adicionales son supuestos; no se ha contratado ni comprado nada. Los umbrales de licencia de Unreal se expresan en dólares porque la licencia los define así; no se aplica una conversión de divisa implícita.

### Costes Higgsfield comprobados

| Consulta de solo lectura | Resultado a 12-09-2026 |
|---|---|
| Plan de la cuenta | Creator |
| Saldo observado | 5.830,88 créditos |
| Nano Banana 2, una imagen 2K, 1:1 | 2 créditos |
| Nano Banana Pro, una imagen 2K, 1:1 | 2 créditos |
| Nano Banana Pro, una imagen 4K, 1:1 | 4 créditos |
| Conversión contractual crédito → euro | No recuperada; se deja como variable |
| Tarifa de Blender remoto / ejecución de Games | No se ha recuperado un desglose que permita presupuestarla |

La página de precios consultada no devolvió las tarifas de compra en su contenido legible. Se conserva [la página oficial de precios](https://higgsfield.ai/mcp-pricing) como punto de comprobación. La diferencia entre el saldo previo observado de 5.860,98 y el actual es 30,10 créditos; no se atribuye automáticamente toda esa variación a un servicio específico ni se extrapola como precio de un juego.

Ejemplo de conceptos para la prueba de producción: 100 diseños × 6 imágenes candidatas × 2 créditos = **1.200 créditos**. Una colección mayor de 240 diseños × 6 imágenes × 2 créditos, más 48 finales a 4K × 4 créditos, suma **3.072 créditos**. Son escenarios de planificación, no generaciones iniciadas ni límite aprobado de gasto. No incluyen audio, vídeo, ejecución remota, retoques humanos ni mallas.

### Fórmula comparable

Coste económico estimado = (horas × tarifa + gastos directos + coste incremental Higgsfield) × (1 + contingencia).

Horas híbridas = horas propias − horas elegibles × reducción supuesta + horas adicionales de corrección/integración.

El ahorro se mide sobre trabajo aceptado. Un diseño rápido que exige rehacer rig o topología puede aumentar el coste total. El coste de caja de un fundador que realiza trabajo propio puede ser mucho menor que el coste económico, pero sus horas siguen siendo una restricción de calendario. No se contabiliza trabajo del fundador simultáneamente como gratuito y como subcontratado.

### Mismo vertical slice nativo: cálculo base

Trabajo propio: 3.200 h × 45 €/h = 144.000 €. Gastos directos de referencia: 8.000 €. Contingencia: 25%. Total: **190.000 €**.

Ruta híbrida: de 1.000 h elegibles se supone una reducción del 25% (250 h), y se añaden 80 h de integración. Quedan 3.030 h. Con los mismos gastos directos y contingencia: **180.437,50 € + 1,25 × I**, donde I es el coste incremental en euros de Higgsfield que no estuviera ya cubierto. Ahorro frente a la ruta propia: **9.562,50 € − 1,25 × I**; reducción neta de trabajo: **170 h, un 5,3%**.

El punto de equilibrio de esa hipótesis es I = 7.650 €. Si las correcciones adicionales suben de 80 a 300 h, la ruta híbrida pasa a 3.250 h y **192.812,50 € + 1,25 × I**: sale más cara que la base. Este contraste es una sensibilidad, no una predicción de que la IA ahorrará exactamente el 5,3%.

Para Godot se usa inicialmente el mismo volumen de contenido de 3.200 h y una sensibilidad de ingeniería adicional de 0–600 h para comprobar sistemas y herramientas que el proyecto necesite. A 45 €/h y 25% de contingencia, eso añade 0–33.750 € al caso base. No se presenta como una penalización inherente del motor: el benchmark puede reducirla, eliminarla o invertirla.

### Qué se compara y qué no

| Ruta | Entrega comparada | Coste estimable ahora | Decisión |
|---|---|---|---|
| Higgsfield Games | Prototipo 3D de navegador acotado | Se puede presupuestar por horas y créditos; no hay tarifa única de juego completo verificada | Útil para validar y compartir una idea |
| Higgsfield como única fábrica del juego nativo | Campaña nativa completa con todas las exigencias | No estimable de forma equivalente: capacidad y coste de esa entrega no verificados | No comprometer producción bajo esa premisa |
| Unreal + Blender propios | Vertical slice nativo de calidad representativa | 190.000 € en el caso económico base; caja depende del reparto fundador/equipo | Candidato principal |
| Unreal + Blender + Higgsfield | Exactamente el mismo vertical slice nativo | 180.437,50 € más coste incremental HF y su contingencia, bajo hipótesis declaradas | Recomendación condicionada al ahorro medido |
| Godot + Blender | Mismo contenido, con adaptación tecnológica | Mismo presupuesto de arte; sensibilidad adicional de ingeniería hasta 33.750 € en este modelo | Alternativa si la prueba ofrece mejor equilibrio |

Un prototipo web ilustrativo de 120 h × 45 €/h y 1.500 € de gastos directos, con 25% de contingencia, costaría **8.625 € + 1,25 × I**. No ofrece la misma cantidad ni calidad de trabajo que el vertical slice nativo. No se usa esa cifra para afirmar que Higgsfield hace un AAA veinte veces más barato.

### Gastos directos de referencia del slice

| Partida | Reserva supuesta | Qué incluye |
|---|---:|---|
| Activos comerciales y derechos concretos | 4.000 € | Paquetes que superen revisión; no compra automática |
| GPU, almacenamiento y transferencia | 1.800 € | Bolsa inicial ajustable a horas y tarifas reales |
| Equipo/periféricos y compatibilidad | 1.600 € | Reserva, no adquisición decidida; el Mac ya existente no se compra de nuevo |
| Herramientas y servicios auxiliares | 600 € | Software o utilidades realmente necesarios |
| Total | 8.000 € | Higgsfield incremental se añade como variable I |

Ejemplo de nube sin cotización: 120 horas × tarifa supuesta de 1,50 €/h = 180 €, más almacenamiento y transferencia. La tarifa es un parámetro de sensibilidad, no una oferta vigente ni una recomendación de un proveedor. Antes de elegirlo se comprueban GPU, acceso gráfico, sistema operativo, drivers, licencia y persistencia. Una GPU alquilada para cálculo Linux no garantiza una estación Windows utilizable con Unreal.

### Licencias

Unreal permite desarrollar juegos bajo un modelo de royalties: su página indica un 5% estándar sobre ingresos brutos atribuibles al producto por encima de 1 millón de USD de vida, con exclusiones y condiciones como los ingresos de Epic Games Store. No se presupuestan asientos de uso no relacionado con juegos como si fueran obligatorios para este caso. [Licencia Unreal](https://www.unrealengine.com/license), [EULA](https://www.unrealengine.com/eula/unreal).

Godot usa licencia MIT y permite licenciar el juego propio, conservando los avisos correspondientes del motor. [Licencia Godot](https://godotengine.org/license/). Licencias de assets, música, voz, tipografías y plugins se registran individualmente; no quedan resueltas por la licencia del motor.

### Lo que queda fuera de estas cifras

Impuestos, comisiones de tiendas, royalties, marketing, localización extensiva, certificación de consolas, operación multijugador y soporte prolongado no están incluidos salvo que una partida lo indique. Para el proyecto completo se reservan por separado después de fijar plataformas, negocio y territorios. Las cifras no son financiación aprobada.

## 17. Secuencia de producción y equipo

Los roles son disciplinas necesarias; una misma persona puede cubrir varias. Un agente de IA puede acelerar tareas concretas, pero no se cuenta como una persona equivalente sin rendimiento aceptado y medido. El calendario usa **120 horas productivas por persona y mes** como supuesto, reservando el resto para coordinación, revisiones y contingencias operativas.

| Fase | Trabajo | Duración orientativa y condición |
|---|---|---|
| P0 — Contrato y contexto | Revisar este plan, recuperar leyes faltantes, comprobar Mac y fijar resultado del benchmark | 1–2 semanas de trabajo acotado; depende de acceso al Mac |
| P1 — Benchmark comparativo | Un personaje, un prop articulado y una escena corta por dos rutas | 40–80 horas de prueba; mismos criterios de aceptación |
| P2 — Combate | Cámara, locomoción, enemigo, daño, retorno y dos armas | 200–400 horas; se abandona o reajusta una dirección que no sea legible |
| P3 — Vertical slice | Región de Terra con calidad representativa, ATLAS y consecuencia persistente | Caso base 3.200 h para la entrega completa; con 4 personas equivalentes son 6,7 meses productivos, horizonte orientativo 7–9 meses |
| P4 — Capítulo | Segundo mundo y retorno; comprobar que el pipeline se repite | Caso base 24.000 h para un capítulo de alcance reducido; financiación y equipo aparte |
| P5 — Visión completa | Producción de los doce mundos, integración, contenido final y pruebas | Programa de estudio; se dimensiona con costes reales del capítulo |

Las horas de P1/P2 forman parte del trabajo de validación y sistemas del presupuesto de slice cuando se integra todo el programa; no se suman dos veces a las 3.200 h. P4 y P5 son escenarios de producto distintos, no ampliaciones gratuitas del mismo sprint. El trabajo reutilizable se descontará de la estimación restante tras aceptación.

**Equipo mínimo propuesto para el slice:** dirección/diseño con programación de gameplay; artista de entorno y niveles; artista de personajes/rig; animación y arte técnico. Audio, narrativa, UI y QA necesitan dedicación planificada, interna o contratada. Si el usuario asume varias disciplinas, baja la salida de caja y sube el calendario o se reduce alcance. No hay fecha fiable para el universo completo con una única persona y herramientas sin medir.

### Primeros 30–45 minutos de juego

0–5: llegada a Terra, refugio, movimiento y observación. 5–12: agua del muelle, primera pelea y elección de ruta. 12–20: acceso al archivo, minijuego de riego, prueba de memoria y primer retorno posible. 20–28: abrir atajo, conversación con consecuencia y preparación. 28–40: ATLAS, aprendizaje y resolución. 40–45: volver al muelle y reconocer el cambio, guardar y reiniciar. El ritmo se mide con participantes y se ajusta; no se rellena hasta alcanzar un número de minutos.

## 18. Puertas de aceptación

Las puertas siguientes son **propuestas para EXOVANT**. No se presentan como gates ya existentes o ejecutados en Studio OS. Si se adopta el proyecto, se mapearán a los gates reales de geometría, visión, rendimiento y cumplimiento del hub cuando corresponda.

| ID propuesto | Prueba que puede fallar | Evidencia requerida | Acción si falla |
|---|---|---|---|
| EXO-G0 Infraestructura | Abrir, consultar, exportar e importar el objeto de referencia; compilar una escena | Versiones, logs, archivo y dimensiones | Resolver entorno antes de nuevos activos |
| EXO-G1 Identidad 3D | Mismo personaje en tres vistas y una pose extrema | Comparativa, mesh y lista de correcciones | Revisar diseño, topología o rig |
| EXO-G2 Combate | Reacción a señales, colisión coherente y cámara en cinco situaciones | Vídeo, estados de ataque y sesión de prueba | Reducir complejidad y ajustar reglas |
| EXO-G3 Recorrido | Inicio, misión, muerte, recuperación, jefe y retorno | Paquete jugable y recorrido completo | No ampliar mundos hasta eliminar bloqueo |
| EXO-G4 Persistencia | Guardar y cargar en estados de misión y tras cada consecuencia | Matriz de casos y estado esperado/obtenido | Corregir modelo de datos; no parchear solo UI |
| EXO-G5 Rendimiento | Recorrido capturado en hardware y ajustes declarados | CPU/GPU, memoria, p95/p99 y cargas | Optimizar contenido o cambiar presupuesto |
| EXO-G6 Dirección artística | Coherencia material, siluetas, iluminación y animación en movimiento | Revisión humana con escenas equivalentes | No promover imágenes aisladas como prueba |
| EXO-G7 Producción repetible | Segundo activo y segunda región con el mismo pipeline | Horas reales, fallos, archivos y reimportación | Reestimar antes de producir los doce mundos |
| EXO-G8 Preparación de distribución | Build reproducible, avisos/licencias y controles completos | Paquete, manifiesto y smoke test en destino | Corregir antes de publicación |

Pruebas de combate con riesgo concreto: cámara junto a muro, debajo de ATLAS, al cambiar objetivo, con dos atacantes y en una pendiente. Pruebas de guardado: muerte durante extracción, salida tras recompensa, carga tras elección planetaria, actualización de versión y recuperación de copia de respaldo. No se exige un catálogo infinito de tests antes de aprender si el combate funciona.

La promoción a producción completa exige presupuesto recalculado con datos reales, segunda región aceptada, responsables disponibles, derecho de uso de activos y al menos una compilación en el hardware objetivo. Una demo visual excelente puede aprobar dirección artística y seguir fallando persistencia o rendimiento.

## 19. Riesgos, decisiones abiertas y criterios de reducción

| Riesgo material | Señal temprana | Respuesta propuesta |
|---|---|---|
| Amplitud galáctica supera capacidad de producción | Cada región exige sistemas exclusivos y semanas de reparación | Mantener doce dossiers; financiar primero dos mundos y reutilizar marcos de interacción |
| Belleza estática sin buen combate | Capturas atractivas, cámara ilegible y golpes inconsistentes | Validar cámara/animación en bloque gris antes de producir detalle |
| Activos generados inconsistentes | Vistas incompatibles, demasiadas piezas o rig frágil | Diseño aprobado único y coste de corrección registrado |
| Mac insuficiente para escena objetivo | Memoria saturada, recompilación larga o efectos experimentales inestables | Reducir escena de edición y validar/renderizar en equipo RTX apropiado |
| Dependencia de servicio remoto | Exportación incompleta, cambios de tarifa o pérdida de estado | Fuentes, intercambio, manifiestos y prueba de reimportación |
| DLSS 5 condiciona promesa visual | SDK no disponible o cambio no controlable de identidad | Calidad base aceptada sin esa función; integración opcional posterior |
| Misiones se multiplican por ramas | Estados contradictorios y recompensas duplicadas | Resultados ortogonales, eventos estables y ramas que vuelven a puntos diseñados |
| Multijugador absorbe el proyecto | Red afecta cada estado y retraso del combate | Campaña offline primero; ampliación con presupuesto propio |

Decisiones que el plan deja revisables: título definitivo; clasificación de edad deseada; prioridad Windows/macOS; tamaño financiable del primer capítulo; RAM y disco del Mac; número de colaboradores; presupuesto de caja; definición canónica de las leyes faltantes. Ninguna impide diseñar el universo. Hardware y caja sí condicionan comprometer producción.

Orden de reducción si el coste supera capacidad: primero aplazar multijugador y vuelo continuo; después reducir extensión de regiones y número de armas iniciales; después limitar número de mundos de lanzamiento. Preservar cámara, combate, animación principal, persistencia y una consecuencia visible. La reducción de alcance se declara; no se mantiene la misma promesa con contenido vacío.

## 20. Estado real y continuidad

Hay cuatro referencias de diseño generadas con Nano Banana 2 para protagonista, ATLAS, portal y entorno. Son referencias candidatas, no mallas aprobadas. También existe una escena de Blender remoto con geometría inicial y exportaciones. La inspección del render muestra masas de blockout, oclusión importante del recorrido y presentación que necesita trabajo; **no supera aún el criterio visual del juego deseado**.

Proyecto de escena: [EXOVANT en 3D Jutsu](https://higgsfield.ai/3d-jutsu/f9e8b5b9-9948-4f81-a49d-e0d989c6a0be), revisión 1. El visor es una escena 3D, no un juego con combate y misiones funcionales.

El repositorio de la prueba Higgsfield contiene scaffold y lógica experimental sin una entrega jugable verificada. Se pausó la construcción y se preservó un checkpoint local `baa1c9e`, posterior a `2232222`. La sincronización remota de ese último commit devolvió un error del proveedor; el paquete de esta planificación incluye `HIGGSFIELD_CHECKPOINT.patch` para recuperar los cambios sobre `2232222`. No se fuerza ningún historial ni se afirma que el último commit esté publicado.

El siguiente trabajo concreto es **M0–M3 en el Mac**, seguido del benchmark P1 con el mismo personaje y escenario. El plan no requiere migrar todas las herramientas ni todos los archivos de conocimiento para empezar. Después se elige una ruta principal con mediciones y se compromete la primera unidad de producción.



## 21. Catálogo maestro y dependencias

El catálogo contiene **318 filas de producción** con cantidades y unidades. Una fila puede representar un sistema, una familia de materiales o un conjunto de mallas; no se suman esas unidades para anunciar un total ficticio de assets terminados. Todos están en estado PROPOSED. Las especificaciones de este documento y los CSV son una asignación inicial que se desglosará durante la producción de cada región.

| Clase | Asignación de visión | Primer slice |
| --- | --- | --- |
| Mundos / regiones | 12 mundos / 36 regiones descritas | Una región compuesta de Terra con recorrido acotado |
| Misiones | 60 principales + 24 secundarias | Una cadena condensada y una secundaria representativa |
| NPC narrativos | 36 identidades; personajes globales incluidos en ese grupo | 3 |
| Biota | 48 especies diseñadas, incluyendo plantas y hongos | 2–3 especies visibles según coste |
| Adversarios | 36 arquetipos de encuentro; objetivo de 24 paquetes principales y variantes | 3 arquetipos |
| Custodios | 12 únicos + 12 desafíos secundarios derivados | ATLAS |
| Armas / herramientas | 24 armas en 8 familias / 8 herramientas | 2 armas / 3 herramientas |
| Vestuario | 12 conjuntos de facción y base del protagonista | 1 conjunto compatible con jugador y variantes mínimas |
| Vehículos | 6 pilotables y 4 de servicio/secuencia | Rover pilotable; nave como espacio de centro |
| Entorno | 12 kits × 45 módulos + 60 compartidos = 600 módulos objetivo | 20–30 módulos de Terra y un subconjunto compartido |
| Utilería | 240 props cotidianos + 36 únicos | 20–35 según recorrido |
| Animación | 1.420 clips objetivo en cinco bibliotecas, con reutilización declarada | 45–70 clips del jugador más subconjuntos de enemigo/jefe |
| Interfaz | 16 familias de pantalla y 120 iconos | HUD, pausa, equipo, diálogo, mapa simple y opciones |
| Audio | 36 ambientes, 36 familias musicales y 480 eventos sonoros | Mezcla completa del recorrido; música adaptativa de ATLAS |


Las asignaciones completas marcadas con una fase indican cuándo comienza el trabajo de esa familia, no que toda su cantidad se produzca en el slice. Las 160 animaciones del jugador, por ejemplo, pertenecen a la visión; el slice acepta solo su subconjunto definido. La misma regla vale para los 45 módulos de Terra y los 60 compartidos.

### Armas: familias y diferencias

| ID | Nombre | Familia | Función | Variante |
| --- | --- | --- | --- | --- |
| WPN_01_01 | Canto del Retorno | Espada de pulso | Distancia media; ataques contenidos; desvío y contraataque | Fundacional: enseña la familia |
| WPN_01_02 | Óxido Noble | Espada de pulso | Distancia media; ataques contenidos; desvío y contraataque | Especialista: cambia alcance o coste |
| WPN_01_03 | Filo Denegado | Espada de pulso | Distancia media; ataques contenidos; desvío y contraataque | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_02_01 | Aguja de Marea | Lanza de anclaje | Control de distancia; estocadas; fijar una herramienta a un punto | Fundacional: enseña la familia |
| WPN_02_02 | Vara de Fobos | Lanza de anclaje | Control de distancia; estocadas; fijar una herramienta a un punto | Especialista: cambia alcance o coste |
| WPN_02_03 | Asta de Raíz | Lanza de anclaje | Control de distancia; estocadas; fijar una herramienta a un punto | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_03_01 | Martillo del Turno | Martillo gravitatorio | Compromiso alto; romper postura y mecanismos; recuperación larga | Fundacional: enseña la familia |
| WPN_03_02 | Badajo del Crisol | Martillo gravitatorio | Compromiso alto; romper postura y mecanismos; recuperación larga | Especialista: cambia alcance o coste |
| WPN_03_03 | Lastre de Origin | Martillo gravitatorio | Compromiso alto; romper postura y mecanismos; recuperación larga | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_04_01 | Manos Gemelas | Hojas gemelas | Presión corta; movilidad lateral; vulnerabilidad ante alcance largo | Fundacional: enseña la familia |
| WPN_04_02 | Dientes de Vanta | Hojas gemelas | Presión corta; movilidad lateral; vulnerabilidad ante alcance largo | Especialista: cambia alcance o coste |
| WPN_04_03 | Alas Partidas | Hojas gemelas | Presión corta; movilidad lateral; vulnerabilidad ante alcance largo | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_05_01 | Poda Cero | Guadaña de campo | Arcos amplios; control de grupos; riesgo en espacios estrechos | Fundacional: enseña la familia |
| WPN_05_02 | Creciente de Umbra | Guadaña de campo | Arcos amplios; control de grupos; riesgo en espacios estrechos | Especialista: cambia alcance o coste |
| WPN_05_03 | Cosecha Futura | Guadaña de campo | Arcos amplios; control de grupos; riesgo en espacios estrechos | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_06_01 | Soga del Nexo | Arma de cable | Tensión y tirones; anclajes; no sustituye el gancho de navegación | Fundacional: enseña la familia |
| WPN_06_02 | Ancla de Drav | Arma de cable | Tensión y tirones; anclajes; no sustituye el gancho de navegación | Especialista: cambia alcance o coste |
| WPN_06_03 | Nervio de Coral | Arma de cable | Tensión y tirones; anclajes; no sustituye el gancho de navegación | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_07_01 | Arco Cívico | Carabina de arco | Disparos limitados por calor; apuntado expuesto; apertura táctica | Fundacional: enseña la familia |
| WPN_07_02 | Disputa del Sol | Carabina de arco | Disparos limitados por calor; apuntado expuesto; apertura táctica | Especialista: cambia alcance o coste |
| WPN_07_03 | Testigo Férreo | Carabina de arco | Disparos limitados por calor; apuntado expuesto; apertura táctica | Custodio: modifica una interacción y conserva el contrato de combate |
| WPN_08_01 | Archivo Portátil | Catalizador de memoria | Habilidades de concentración; ecos cortos; tiempo de preparación | Fundacional: enseña la familia |
| WPN_08_02 | Lente de Mneme | Catalizador de memoria | Habilidades de concentración; ecos cortos; tiempo de preparación | Especialista: cambia alcance o coste |
| WPN_08_03 | Pulso Compartido | Catalizador de memoria | Habilidades de concentración; ecos cortos; tiempo de preparación | Custodio: modifica una interacción y conserva el contrato de combate |


### Vehículos

| ID | Nombre | Tipo | Función | Fase |
| --- | --- | --- | --- | --- |
| VEH_01 | Arca del Retorno | pilotable | Nave de expedición y hogar; cinco módulos funcionales | P4_CHAPTER |
| VEH_02 | Cicatriz | pilotable | Interceptor con decisiones de calor y maniobra | P5_VISION |
| VEH_03 | Peregrino-6 | pilotable | Rover anfibio; primer controlador de vehículo | P3_SLICE |
| VEH_04 | Nácar-2 | pilotable | Sumergible para corredores diseñados | P5_VISION |
| VEH_05 | Helioperegrino | pilotable | Moto de vela; recorridos solares y de sombra | P5_VISION |
| VEH_06 | Vela de Ceniza | pilotable | Planeador por rutas y anclajes | P5_VISION |
| VEH_07 | Remolcador Drav | sequence | Maniobra de rescate y tensión de cables | P5_VISION |
| VEH_08 | Taladro Mula | sequence | Secuencia de tránsito industrial | P5_VISION |
| VEH_09 | Cargador de Concha | service | Logística y cambio visible de estado | P5_VISION |
| VEH_10 | Tranvía custodio | sequence | Ruta programable y espacio de historia | P5_VISION |


### Dependencias que ordenan el trabajo

Escala y color preceden a kits. Rig humano y cámara preceden a armas finales. Contrato de ataque precede a clips definitivos. Estado de misión precede a diálogo grabado. Persistencia precede a consecuencias planetarias. Perfil de escena precede a multiplicar variantes. La biblia creativa limita las generaciones; los resultados aceptados actualizan el catálogo.

### Trabajo económico del slice

| ID | Disciplina | Horas base | Salida | Puerta |
| --- | --- | --- | --- | --- |
| W01 | Dirección, diseño y producción | 220 | Briefs, revisión, decisiones y benchmark | EXO-G0/G6 |
| W02 | Gameplay y sistemas | 500 | Combate, cámara, interacción y guardado | EXO-G2/G4 |
| W03 | Diseño de nivel y misión | 300 | Rutas, estados, encuentros y consecuencia | EXO-G3 |
| W04 | Personajes, criaturas y armas | 650 | Modelado, UV, materiales y rig de los activos del slice | EXO-G1 |
| W05 | Entorno y utilería | 450 | Kit de Terra, paisaje, interiores y props | EXO-G1/G6 |
| W06 | Animación y arte técnico | 400 | Contactos, ataques, herramientas, efectos y exportación | EXO-G2/G5 |
| W07 | Narrativa, audio e interfaz | 300 | Diálogo, mezcla, música, HUD y localización inicial | EXO-G3/G6 |
| W08 | Integración, QA y optimización | 380 | Recorrido, guardados, rendimiento y build | EXO-G3/G4/G5/G8 |


Total comprobado: **3,200 horas**. La reserva de contingencia se aplica en el presupuesto; no se añaden esas mismas horas de nuevo a cada disciplina. Las cantidades de la visión completa no se costean como si pertenecieran al slice.

### Escenarios de alcance

| Entrega | Escenario | Horas | Tarifa €/h | Gastos € | Contingencia | Coste económico € |
| --- | --- | --- | --- | --- | --- | --- |
| Vertical slice nativo | low | 1,800 | 30 | 3,000 | 25% | 71,250.00 |
| Vertical slice nativo | base | 3,200 | 45 | 8,000 | 25% | 190,000.00 |
| Vertical slice nativo | high | 5,200 | 75 | 15,000 | 25% | 506,250.00 |
| Capítulo de dos mundos reducido | low | 8,000 | 35 | 30,000 | 30% | 403,000.00 |
| Capítulo de dos mundos reducido | base | 24,000 | 45 | 100,000 | 30% | 1,534,000.00 |
| Capítulo de dos mundos reducido | high | 60,000 | 70 | 250,000 | 30% | 5,785,000.00 |
| Visión completa de doce mundos | low | 240,000 | 45 | 1,200,000 | 35% | 16,200,000.00 |
| Visión completa de doce mundos | base | 600,000 | 60 | 4,000,000 | 35% | 54,000,000.00 |
| Visión completa de doce mundos | high | 1,200,000 | 90 | 12,000,000 | 35% | 162,000,000.00 |


La visión completa arroja una banda ilustrativa de **16,2–162 millones de euros**, con caso base **54 millones**. Es el resultado de las horas, tarifas, gastos y contingencia declarados, no una valoración de un estudio ni una afirmación de que ese dinero garantice calidad. El caso base de 600.000 h equivale aritméticamente a 50 meses con 100 personas y 120 h productivas/mes; dependencias, contratación y financiación pueden ampliar el calendario. Si la intención es autofinanciar, la unidad razonable de decisión es el slice o un capítulo reducido.

### Responsabilidad y estado de evidencia

Dirección aprueba intención y prioridades. Ingeniería demuestra comportamiento y recuperación. Arte aprueba identidad y construcción. Animación demuestra contactos y lectura. Sonido demuestra jerarquía y señales. QA registra fallos reproducibles y recorrido. Producción compara horas reales con supuestos. Ninguna disciplina puede marcar todo el juego como aceptado con su propia prueba aislada.
