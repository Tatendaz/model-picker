.PHONY: test lint
test:
	python3 -m unittest discover -s plugins/codex-model-advisor/tests -v
lint:
	ruff check plugins/ docs/diagrams/
