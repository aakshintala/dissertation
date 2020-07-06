#! /usr/bin/make

# YOU PROBABLY DON'T NEED TO RUN THIS.

# This generates pdf files included in the text. Since this requires
# inkscape, the pdfs are committed to the repo despite being
# intermediate files.

all: design_high_level.pdf design.pdf memory_hierarchy.pdf work_flow.pdf communication.pdf silo.pdf design_highest_level.pdf

%.tex %-tex.pdf: %.svg
	inkscape -C -z --file=$< --export-pdf=$*-tex.pdf --export-latex
	mv $*-tex.pdf_tex $*.tex

%.pdf: %.svg
	inkscape -C -z --file=$< --export-pdf=$*.pdf
