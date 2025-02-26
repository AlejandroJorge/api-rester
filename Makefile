ifneq (,$(wildcard ./.env))
    include .env
    export
endif

upload: build
	python -m twine upload --repository pypi dist/* --verbose --non-interactive

build: clean
	python3 -m pip install --upgrade build
	python3 -m build

clean:
	rm -rf dist/ src/api-rester.egg-info/
