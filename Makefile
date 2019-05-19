
upload:
	twine upload dist/*

version:
	bumpversion minor

wheel:
	python setup.py bdist_wheel

ci:
	pytest --pep8 --flakes ipymarkup --nbval --cov ipymarkup --cov-report xml -v test.ipynb

test:
	pytest --pep8 --flakes ipymarkup --nbval --cov-report term-missing --cov ipymarkup -v test.ipynb

clean:
	find ipymarkup -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info coverage.xml
