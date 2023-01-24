
lint:
	flake8 ipymarkup

exec-notebooks:
	python -m nbconvert \
		--ExecutePreprocessor.kernel_name=python3 \
		--ClearMetadataPreprocessor.enabled=True \
		--execute --to notebook --inplace \
		*.ipynb

