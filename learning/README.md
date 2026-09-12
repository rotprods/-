# Aprendizaje persistente de EXOVANT

Autoridad de los eventos de este proyecto: `learning/hub`. El runtime y esquema proceden del sistema del usuario, con procedencia en docs/PROTOCOLS.md. rot.knowledge tendrá un índice/ruta hacia estos eventos, no una copia editable que pueda divergir. Mem, Drive y Linear apuntan a esta autoridad.

Cada evento registra síntoma, mecanismo, familia, frontera de generalización, evidencia, relación con conocimiento previo, promoción y verificaciones. Se comienza en L2-persisted: haber reejecutado un test del juego no verifica automáticamente el aprendizaje ni su adopción por futuros agentes. Las comprobaciones de recuperación de esta ola se registran por separado; futuras revalidaciones crean eventos nuevos con REVALIDATES. No se declara L4 en todo el sistema ni L5 por previsión.

```
python3 tools/aprende_runtime.py audit learning/hub
python3 tools/aprende_runtime.py retrieve learning/hub COLLISION
```

Search EXOVANT en rot.knowledge y Mem no produjo eventos previos al crear este hub. Eso sustenta NEW en este ámbito, no que la idea jamás existiera en otro lugar. Las 12 observaciones seleccionadas se reconstruyen de fuentes y resultados disponibles; no son un conteo exhaustivo de interacciones pasadas.

`instincts.json` contiene una proyección para recuperación trigger → acción → learning_id. No instala agentes ni cambia parámetros de un modelo. El cambio de comportamiento se obtiene leyendo AGENTS, ejecutando controles y consultando los eventos en el próximo run.
