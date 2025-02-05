#! /bin/bash

# Check we have the correct macros in the file
python ~/scripts/fix_bibtex_macros.py me.bib

# Generate the HTML file from the bibtex file
bibtex2html -noabstract -nokeywords -noheader -m aas.tex -s abbrv.bst -d -r me.bib

# Make my name bold
sed -i.bak -e 's/L\.\&nbsp;Conaboy/<b>L\.\&nbsp;Conaboy<\/b>/' me.html

# Finally, format the output nicely
python strip_bib.py me.html

