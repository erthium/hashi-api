REQUIREMENTS_FILE := 'requirements.txt'

.PHONY: init freeze dev start

init:
	pip install -r $(REQUIREMENTS_FILE)


freeze:
	pip freeze > $(REQUIREMENTS_FILE)

dev:
	uvicorn app.main:app --reload --port 4040

start:
	python3 -m app.main
