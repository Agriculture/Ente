all:
	python -O src/main.py

clean:
	rm src/*.pyo
	rm src/*.py~

test: 
	ls
	ls -lia
