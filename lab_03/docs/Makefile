.PHONY: rep clean

FILE = report

rep:
	pdflatex $(FILE).tex

	bibtex $(FILE).aux

	pdflatex $(FILE).tex
	pdflatex $(FILE).tex
	
	xdg-open $(FILE).pdf

	rm *.aux


prog:
	python3 ../src/main.py

clean:
	echo "Coming soon..."
