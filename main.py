from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import urllib.parse
import requests
import re
import ssl


from libraries import utils


def find_internal_urls(request, root):

    soup = BeautifulSoup(request, 'html.parser')

    links = soup.findAll('a')
    internal_urls = []

    for link in links:
        if utils.extract_domain(link.get('href')) == root:
            href = link.get('href')

            # Accents in url...
            href_parts = href.split('://')

            sub_url = href_parts[0] + '://' + urllib.parse.quote(href_parts[1])

            internal_urls.append(sub_url)

    return internal_urls


def parse_zip_code(request):
    zips = []
    # Regex can be optimized
    matches = re.findall("\d{2}[ ]?\d{3}", utils.text_from_html(request))

    for code in matches:
        zips.append(code)

    return zips


def find_zip_code(url):
    zips = []

    root = utils.extract_domain(url)

    context = ssl._create_unverified_context()
    try:
        print('INF % Processing ' + url)
        request = urllib.request.urlopen(url, context=context).read()

        # Parse starting page
        zips.extend(parse_zip_code(request))

        internal_urls = find_internal_urls(request, root)

        # Parse second level pages
        for sub_url in internal_urls:
            print('INF % Processing ' + sub_url)
            try:
                request = urllib.request.urlopen(sub_url, context=context).read()
                zips.extend(parse_zip_code(request))
            except:
                print('ERR % Can not request page')

        return utils.most_frequent(zips)
    except:
        print('Error % Can not request page')


urls = ["https://www.aquafamily.fr/"]

for url in urls:
    print(find_zip_code(url))