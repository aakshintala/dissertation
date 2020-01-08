
.SUFFIXES: .fig .dvi .ps

VERSION = NoVersionGiven

all: *.tex ref.bib
	rubber -d -o pdf2ps -Wrefs -Wmisc $(name)

osx:
	pdflatex $(name)
	bibtex $(name)
	pdflatex $(name)
	pdflatex $(name)

clean:
	rubber --clean -d -Wrefs -Wmisc $(name)
	rm -f $(name).ps $(name).out $(name).pdf $(name).log $(name).bbl $(name).blg $(name).aux

oclean:
	rm -f $(name).ps $(name).out $(name).pdf $(name).log $(name).bbl $(name).blg $(name).aux


#----------------------------------------------------------------------
# Source files.  Edit these variables for each new paper.
#----------------------------------------------------------------------

name = diss

latex_files = $(name).tex

#----------------------------------------------------------------------
# Shouldn't have to touch anything below here...
#----------------------------------------------------------------------

#----------------------------------------------------------------------
# LaTeX commands.
#----------------------------------------------------------------------

latex_junk = 	$(name).dvi \
		*.aux \
		$(name).log \
		$(name).blg \
		$(name).bbl \
		$(name).toc \
		$(name).synctex.gz \
		$(name).fdb_latexmk \
		psfig.aux

#----------------------------------------------------------------------
# Postscript/PDF generation.
#----------------------------------------------------------------------

pdf: $(name).pdf

$(name).pdf: *.tex ref.bib *.sty
	rubber --pdf -Wrefs -Wmisc $(name)
