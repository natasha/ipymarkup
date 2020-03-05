
upload:
	twine upload dist/*

version:
	bumpversion minor

wheel:
	python setup.py sdist bdist_wheel

test:
	pytest \
		--pep8 --flakes ipymarkup \
		--nbval --current-env \
		--cov-report term-missing --cov-report xml --cov ipymarkup \
		-v test.ipynb docs.ipynb

clean:
	find . \
		-name '*.pyc' \
		-o -name '__pycache__' \
		-o -name '.DS_Store*' \
		| xargs rm -rf

	rm -rf dist/ build/ .pytest_cache/ .cache/ \
		*.egg-info coverage.xml .coverage
