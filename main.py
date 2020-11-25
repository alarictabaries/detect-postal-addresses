from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import urllib.parse
import requests
import re
import ssl
import csv


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

            if (".pdf" or ".jpg" or ".png") not in sub_url:
                internal_urls.append(sub_url)

    return internal_urls


def parse_zip_code(request, zip_codes):
    zips = []

    # Regex can be optimized
    matches = re.findall(r'(\w*(?<!BP )\d{2}[ ]?\d{3}\b\s+)', utils.text_from_html(request))

    for code in matches:
        print(code.replace(" ", ""))
        if code.replace(" ", "") in zip_codes:
            zips.append(code.replace(" ", ""))

    print(zips)
    return zips


def find_zip_code(url, zip_codes):
    zips = []

    root = utils.extract_domain(url)

    context = ssl._create_unverified_context()
    try:
        print('INF % Processing ' + url)
        request = urllib.request.urlopen(url, context=context).read()

        # Parse starting page
        zips.extend(parse_zip_code(request, zip_codes))

        internal_urls = find_internal_urls(request, root)

        # Parse second level pages
        for sub_url in internal_urls:
            print('INF % Processing ' + sub_url)
            try:
                request = urllib.request.urlopen(sub_url, context=context).read()
                zips.extend(parse_zip_code(request, zip_codes))
            except:
                print('ERR % Can not request page')

        return utils.most_frequent(zips)
    except:
        print('Error % Can not request page')


zip_codes = []
with open('laposte_hexasmal.csv', 'r') as csv_zip:
    csv_reader = csv.reader(csv_zip, delimiter=';')
    for row in csv_reader:
        zip_codes.append(row[2])

with open('CartoPNPC21.csv', 'r') as csv_input:
    with open('CartoPNPC21_out.csv', 'w', newline='') as csv_output:
        csv_writer = csv.writer(csv_output, delimiter=';')
        csv_reader = csv.reader(csv_input, delimiter=';')

        out = []

        for row in csv_reader:
            refined_url = row[2].split()[0]
            row.append(find_zip_code(refined_url, zip_codes))
            out.append(row)

        csv_writer.writerows(out)