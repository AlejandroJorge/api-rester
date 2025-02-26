test:
	@echo Sending request\:
	@cat request.json
	@echo Processing\:
	@python3 api-rester.py
	@echo Got response\:
	@head -n 30 response.json
