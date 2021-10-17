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


check:
	find . -name "*.tex" -exec aspell --lang=ru --mode=tex check "{}" \;

clean:
	echo "Coming soon..."


# Hanspell check 
# find . -name "*.tex" -exec hunspell -t -i utf-8 '{}' \; 

# Aspell check
#find . -name "*.tex" -exec aspell --lang=en --mode=tex check "{}" \; 

# find . -name "*.tex" -exec aspell --lang=ru --mode=tex check "{}" \; 