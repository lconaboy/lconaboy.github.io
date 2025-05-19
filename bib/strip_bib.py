"""
This is the worst piece of code I have ever written.
"""
import os
import re
import sys

inp_fn = sys.argv[1]
out_fn = '../bib.html'

inp = open(inp_fn, 'r')
out = open(out_fn, 'w')

# Write first half of bib html
out.write('<html>\n')
out.write('  <head>\n')
out.write('    <link rel="stylesheet" href="styles.css">\n')
out.write('    <meta name="google-site-verification" content="egpqFBWYXcbmA02K-_elZgx0FR7HUNiZ4mA1jsgvEOs" />\n')
out.write('    <meta name="viewport" content="width=device-width, initial-scale=1">\n')
out.write('    <title>\n')
out.write('      conaboy/home\n')
out.write('    </title>\n')
out.write('  </head>\n')
out.write('  <body>\n')
out.write('    \n')
out.write('    <div class="main">\n')
out.write('      <div class="header">\n')
out.write('	<a href="index.html", style="color:#440154">home</a>\n')
out.write('	<a href="https://raw.githubusercontent.com/lconaboy/cv/main/cv.pdf", style="color:#46327E" >cv</a>\n')
out.write('	<a href="talks.html" style="color:#365C8D">talks</a>\n')
out.write('	<a href="mailto:luke.conaboy@nottingham.ac.uk" style="color:277F8E">email</a>\n')
out.write('	<a href="https://github.com/lconaboy" style="color:#1FA187">github</a>\n')
out.write('	<a href="bib.html" style="color:#4AC16D">publications</a>\n')
out.write('      </div>\n')
out.write('\n')
out.write('      <div class="container">\n')
out.write('	  <div class="papers">\n')
out.write('	    <p style="text-align: center">\n')
out.write('         <a href="index.html" style="color:#0000FF">home</a>/<a href="bib.html" style="color:#0000FF">publications</a>\n')
out.write('	    </p>\n')

out.write('	    <p>\n')
out.write('            Publications are listed below (see also <a href="https://ui.adsabs.harvard.edu/search/q=%20author%3A%22conaboy%2C%20luke%22&sort=date%20desc%2C%20bibcode%20desc&p_=0">ADS</a>).\n')
out.write('	    </p>\n')

out.write('	    <p>\n')

# Now the actual bibliography
write = True
new_entry = False
end_entry = False
author_key = None
bib_entry = {}
old_lini = None

# FIXME bad stuff happens with multi-line author lists if an initial is repeated

if write: out.write('<table>\n')

for l in inp:
    if l[0] in ['<', '[', ']']:
        lini = l[0:5]
    else:
        lini = l
        
    if lini == "</tab":
        print("-- stopping writing")
        write = False
        out.write("</table>\n")
        break
    elif new_entry:
        bib_entry[lini] = l
        if lini == '</tr>':
            new_entry = False
            end_entry = True
    elif lini == '<tr v':
        new_entry = True
        bib_entry[lini] = l
    old_lini = lini

    # We have reached the end of this bibtex entry, so now we can play
    # around with it before writing it out
    if end_entry:
        # Find out the citekey associated with this entry
        # print(bib_entry['[<a n'])
        match = re.search('name="(\w+\d+\w*)"', bib_entry['[<a n'])
        name = match.group(1)
        # print(name)

        # If I have uploaded the pdf, link to it
        pdf_file = f'../pdf/{name:s}.pdf'
        if os.path.isfile(pdf_file):
            pdf = f'<a href="pdf/{name:s}.pdf">pdf</a>&nbsp;|&nbsp;'
        else:
            pdf = ''
            print(pdf_file, 'not found')

        # This key might not have a link to the arXiv/DOI version (somehow)
        try:
            hrefs = bib_entry['[&nbs'] + pdf + bib_entry['<a hr']+'\n'
        except KeyError as e:
            hrefs = bib_entry['[&nbs'][:-1] + pdf + '\n'

        # Remove [] from links
        hrefs_stripped = ''
        for x in hrefs:
            if x not in ['[', ']', '|']:
                hrefs_stripped += x
        hrefs = hrefs_stripped

        # Combine all the links together to be placed in the first cell
        bib_entry['[&nbs'] = ''
        bib_entry['<a hr'] = ''
        bib_entry['[<a n'] = f'<a name={name:s}>{hrefs:s}</a>\n'

        # Finally write out the entire entry
        if write:
            for line_key, bib_line in bib_entry.items():
                out.write(bib_line)
            out.write('</td>\n')  # this tag is not stored, because there is one earlier
            
        bib_entry = {}
        end_entry = False
        # if write: out.write(l)
        

# Finish off the second half
out.write('	    </p>\n')
out.write('\n')
out.write('	  <p style="font-size: 14px">\n')
out.write('	     Bibliography converted from bibtex to HTML using <a href="http://www.lri.fr/~filliatr/bibtex2html/"><tt>bibtex2html</tt></a>, inspired by <a href=https://fleuret.org/francois/publications.html> François Fleuret </a>\n')
out.write('	  </p>\n')

out.write('	  </div>\n')
out.write('	  <div class="footer">\n')
out.write('Updated: Wed 05 Feb 25\n')
out.write('	  </div>\n')
out.write('	</div>\n')
out.write('    </div>\n')
out.write('  </body>\n')
out.write('</html>\n')

inp.close()
out.close()
