.PHONY: test
test:
	python3 -m unittest discover -s plugins/codex-model-advisor/tests -v
