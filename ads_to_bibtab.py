import requests
import datetime

LIBRARIES_URL = "https://api.adsabs.harvard.edu/v1/biblib/libraries"
SEARCH_URL = "https://api.adsabs.harvard.edu/v1/search/query"
MAXAUTHORS = 16

def list_libraries(token):
    resp = requests.get(
        LIBRARIES_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("libraries", [])


def fetch_papers(token, library_id, rows=500):
    lib_resp = requests.get(
        f"{LIBRARIES_URL}/{library_id}",
        headers={"Authorization": f"Bearer {token}"},
        params={"start": 0, "rows": rows},
        timeout=25,
    )
    lib_resp.raise_for_status()

    docs = lib_resp.json().get("solr", {}).get("response", {}).get("docs", [])
    bibcodes = [d["bibcode"] for d in docs if d.get("bibcode")]
    if not bibcodes:
        return []

    search_resp = requests.get(
        SEARCH_URL,
        headers={"Authorization": f"Bearer {token}"},
        params={
            "q": " OR ".join(f"bibcode:{bc}" for bc in bibcodes),
            "fl": "title,author,pubdate,year,pub,bibstem,volume,page,doi,doctype,citation_count",
            "rows": len(bibcodes),
        },
        timeout=30,
    )
    search_resp.raise_for_status()
    return search_resp.json().get("response", {}).get("docs", [])


def read_token():
    """Reads ADS token, assuming it is stored in ~/.ads/token

    Returns
    -------
    str
        ADS token

    """
    from os.path import expanduser, isfile

    fn = f'{expanduser("~")}/.ads/token'
    if not isfile(fn):
        raise FileNotFoundError('ADS token must be stored in ~/.ads/token')

    with open(fn, 'r') as f:
        TOKEN = f.readline()

    return TOKEN


def doi_to_url(doi):
    assert len(doi) < 3, 'too many DOIs!'

    url = {}
    url = {'arxiv': None, 'pub': None}
    for doi_ in doi:
        doi_ = doi_.lower()
        if 'arxiv' in doi_:
            url_ = doi_.split('arxiv.', 1)[1]
            url['arxiv'] = f'https://arxiv.org/pdf/{url_:s}.pdf'
        else:
            url['pub'] = f'https://dx.doi.org/{doi_:s}'

    return url


def get_journal_bibitem(p):
    bibitem = p.get('year') + ', '
    if p.get('doctype') == 'article':
        bibitem += p.get('pub') + ', '
        if p.get('volume'):
            # bibitem += ' <b>' + p.get('volume') + '</b>'
            bibitem += p.get('volume')
    elif p.get('doctype') == 'eprint':
        doi = p.get('doi')[0]
        arxiv = 'arXiv.'
        idx = doi.find(arxiv)
        bibitem = 'astro-ph/' + doi[idx+len(arxiv):]
    else:
        return None


    return bibitem

        
def p_to_bibitem(p):
    print(p.get('title'))
    url = doi_to_url(p.get('doi'))

    bibitem = '<tr valign="top">\n'
    bibitem += '<td align="right" class="bibtexnumber">\n'
    if url['pub'] is not None:
        bibitem += '<a href="'+url['pub']+'">pub</a>&nbsp;\n'
    if url['arxiv'] is not None:
        bibitem += '<a href="'+url['arxiv']+'">arXiv</a>&nbsp;\n'
    # bibitem += '</a>\n'
    bibitem += '</td>\n'
    # bibitem += '<td>\n'
    # bibitem += '</td>\n'
    bibitem += '<td class="bibtexitem">\n'

    # Now format authors
    nauthors = 0
    for author in p.get("author"):
        if 'Conaboy' in author:
            if nauthors == MAXAUTHORS: bibitem += '..., '
            bibitem += '<b>'+author+r'</b>' 
            if nauthors == MAXAUTHORS: bibitem += ', ..., '
        else:
            if nauthors < MAXAUTHORS:
                bibitem += author

        if nauthors < MAXAUTHORS:
            bibitem += ', '
            nauthors += 1
 
    bibitem = bibitem
    bibitem += '<i>' + p.get('title')[0].replace('$', '') + '</i>, '
    journal = get_journal_bibitem(p)
    if journal is not None: bibitem += journal + '\n'
    bibitem += '</td>\n'
    bibitem += '</tr>\n'

    return bibitem


def year_to_bibitem(year):
    bibitem = '<tr valign="top"; class="border_bottom">\n'
    bibitem += '<td align="right">\n'
    bibitem += '<b>' + year + '</b>\n'
    # bibitem += '</a>\n'
    bibitem += '</td>\n'
    # bibitem += '<td>\n'
    # bibitem += '</td>\n'
    bibitem += '<td>\n'
    bibitem += '</td>\n'
    bibitem += '</tr>\n'

    return bibitem

def pubdate_to_year(pubdate):
    year = pubdate[0:4]

    return year


if __name__ == "__main__":
    TOKEN = read_token()

    # List all libraries and pick the first one
    libraries = list_libraries(TOKEN)
    for lib in libraries:
        print(f"{lib['id']}  {lib['name']}  ({lib['num_documents']} papers)")

    bibitems = {}
        
    if libraries:
        lib_id = libraries[0]["id"]
        papers = fetch_papers(TOKEN, lib_id)
        print(f"\nFetched {len(papers)} papers from '{libraries[0]['name']}':\n")
        for p in papers:
            k = p.get('pubdate')
            
            if k[-1] == '0':
                k = k[:-1] + '1'  # not sure what's going on but we
                                  # can't have zero days

                # We need to deal with dupilcate pubdates, since we
                # use the pubdate as a key. This is going to be
                # good...
            while k in bibitems:
                k = k[:-1] + str(int(k[-1]) + 1)

            bibitems[k] = p_to_bibitem(p)

            # TODO write new date and add bottom line to the rows

    bibitems = dict(sorted(bibitems.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d'), reverse=True))
    cur_year = 9999
    with open('bibtab.html', 'w') as f:
        f.write('<table border-collapse: collapse>\n')
        for pubdate, bibitem in bibitems.items():
            
            year = pubdate_to_year(pubdate)

            if int(year) < cur_year:
                f.write(year_to_bibitem(year))
                cur_year = int(year)

            f.write(bibitem)
        f.write('</table>\n')
