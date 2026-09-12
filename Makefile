.PHONY: bootstrap test native validate project package
bootstrap:
	python3 tools/bootstrap_godot.py --destination .tools
test:
	python3 -m unittest discover -s tests -p 'test_*.py' -v
native:
	python3 tests/run_gauntlet.py --godot .tools/Godot_v4.7.2-stable_linux.x86_64
validate:
	python3 tools/studio.py validate
project:
	python3 tools/studio.py project
package:
	python3 tools/package_source.py
