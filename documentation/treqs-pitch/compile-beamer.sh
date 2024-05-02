#!/bin/bash

DATE_COVER=$(date "+%d %B %Y")

SOURCE_FORMAT="markdown_strict\
+pipe_tables\
+backtick_code_blocks\
+auto_identifiers\
+strikeout\
+yaml_metadata_block\
+implicit_figures\
+all_symbols_escapable\
+link_attributes\
+smart\
+fenced_divs"

# --template pandoc-beamer-template.latex
pandoc --template pandoc-beamer-template.latex --bibliography references.bib  -s --slide-level 2 --toc --listings --columns 50 --pdf-engine lualatex -V classoption:aspectratio=169 -t beamer treqs-presentation.md -o treqs-presentation.pdf
pandoc --template pandoc-beamer-template.latex --bibliography references.bib  -s --slide-level 2 --toc --listings --columns 50 --pdf-engine lualatex -V classoption:aspectratio=169 -t beamer treqs-demonstrator.md -o treqs-demonstrator.pdf
pandoc --template pandoc-beamer-template.latex --bibliography references.bib  -s --slide-level 2 --toc --listings --columns 50 --pdf-engine lualatex -V classoption:aspectratio=169 -t beamer treqs-usage.md -o treqs-usage.pdf
