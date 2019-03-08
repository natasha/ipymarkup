
test:
	pytest --pep8 --flakes ipymarkup --nbval --cov ipymarkup --cov-report xml -v test.ipynb

clean:
	find ipymarkup -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info coverage.xml
