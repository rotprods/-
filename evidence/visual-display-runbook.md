# Visual display qualified — VISUAL-005

Source 97fb4747. Existing tests/capture_visual.py works with portable Xvfb after resolving its absolute /usr/bin/xkbcomp dependency. Keep authentication; do not disable X access controls.

1. Recover qualified Godot with tools/bootstrap_godot.py.
2. Install Xvfb and xkbcomp through normal package manager on a compatible host; when package-manager privilege switching is unavailable, unpack official Ubuntu packages locally. Record hashes. Portable libraries need LD_LIBRARY_PATH.
3. Xvfb in this distribution calls /usr/bin/xkbcomp explicitly. If missing, expose the installed compiler at that path; never overwrite an existing executable. The current VM uses a symlink to .tools/display/root/usr/bin/xkbcomp. A new environment must restore this dependency.
4. Run Godot --headless --path . --editor --import before capture on a cold clone.
5. python3 tests/capture_visual.py --godot <qualified binary> --xvfb <portable Xvfb> --xlibs <portable lib directory>
6. Require newly generated PNG, CAPTURE_SAVED, no ERROR or SCRIPT ERROR in visual-run.log, and inspect the image. Exit status alone is insufficient: an initial cold run saved a PNG despite missing imported assets.

Evidence: visual-display-qualified.json; final screenshot and dependency bundle persisted in Drive and issue #7. The scene is the prototype, not the Terra art candidate. capture mode repositions player; no full route claim. llvmpipe is CPU, not a GPU benchmark. No permanent desktop or daemon is claimed.
