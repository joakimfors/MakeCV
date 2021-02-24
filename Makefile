LETTERS_SRC := $(wildcard *brev*.md)
LETTERS_TEX := $(LETTERS_SRC:.md=.tex)
LETTERS_PDF := $(LETTERS_SRC:.md=.pdf)

all: CV.pdf ${LETTERS_PDF}

CV.tex: CV.yml template.tex
	python3 build.py -y CV.yml -t template.tex -o $@

%.tex: %.md CV.yml template.tex
	python3 build.py -y CV.yml -t template.tex -i $< -o $@

%.pdf: %.tex
	xelatex $<
	xelatex $<

.PHONY: clean
clean:
	rm -vf CV.tex *.aux *.out *.log


.PHONY: list
list:
	echo ${LETTERS_SRC} ${LETTERS_PDF}
