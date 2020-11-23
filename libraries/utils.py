from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import Counter


def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)


def extract_domain(url, remove_http=True):
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        domain_name = f"{uri.netloc}://{uri.netloc}"
    return domain_name