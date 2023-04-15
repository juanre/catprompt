all:

publish:	clean
	python -m build
	twine upload dist/*

clean:
	rm -rf catprompt.egg-info build dist
