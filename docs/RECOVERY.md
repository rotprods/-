# Recuperación y continuidad sin conversación

Clonar https://github.com/rotprods/-.git. Leer AGENTS, STATE y HANDOFF. Recuperar aprendizajes, comprobar integridad, obtener Godot de la fuente fijada y ejecutar gates. No se requiere el caché .godot ni el historial de chat. El repositorio contiene el portal GLB y su .blend original.

## Comandos
```
python3 tools/project_control.py check
python3 tools/aprende_runtime.py audit learning/hub
python3 tools/aprende_runtime.py retrieve learning/hub MESA
python3 tools/bootstrap_godot.py --destination .tools
python3 tests/run_gauntlet.py --godot .tools/Godot_v4.7.2-stable_linux.x86_64
```

Para jugar: abrir project.godot con Godot 4.7.2 o ejecutar el motor con --path apuntando al repositorio. La captura virtual anterior necesita Xvfb, libXfont2, libxkbfile, xkbcomp y reglas XKB. El script tests/capture_visual.py comparte servidor/cliente en una invocación, utiliza cookie temporal y termina procesos al finalizar. Esa receta está cualificada en esta VM; no se promete que se aplique a cualquier sandbox. En escritorio normal utilizar el display existente.

GitHub es canónico. Drive contiene snapshot y dossier con SHA; si se restaura un snapshot antiguo, recuperar primero origin/main. Los antiguos EXOVANT_GAME_CURRENT.zip y EXOVANT_HANDOFF.md previos a esta migración son históricos. No deben reemplazarse automáticamente ni competir con el repositorio.

Si falla una sincronización secundaria: conservar el commit, registrar provider/outcome/pendiente y reconciliar mediante ID antes de repetir la creación. No convertir un timeout en un éxito ni duplicar proyectos o notas. No enviar correos a terceros como parte del guardado.
