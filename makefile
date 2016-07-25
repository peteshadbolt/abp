DOC_DIR = doc

.PHONY: doc

doc:
	$(MAKE) -C $(DOC_DIR) html 

sdist:
	python setup.py build sdist

deploy: sdist doc
	$(MAKE) -C $(DOC_DIR) deploy
	python setup.py sdist register upload
