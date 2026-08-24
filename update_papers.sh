#! /bin/bash

# Updates the bib pages by scraping my ADS library and committing the
# changes to bibtab.html, which rebuilds the static copy of the site
#
# . update_papers.sh

python ads_to_bibtab.py
git add bibtab.html
git commit -m "Updated bib"
git push
