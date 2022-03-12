all : py git pip

py :
	python increaseVersionSetup.py
	rm -rf build dist
	python setup.py sdist bdist_wheel
	python -m twine upload  dist/*

git :
	git commit -am 'new release'
	git push origin master

pip :
	# pip install --upgrade packageName
	echo "You can run: `pip install --upgrade packageName`"
