upload: build
	python -m twine upload --repository pypi dist/* --verbose

build:
	rm -rf dist/ src/api_rester.egg-info/
	python3 -m pip install --upgrade build
	python3 -m build
