import bs4
import urllib, re
from pelican import signals

def extract_text(url):
    html = urllib.request.urlopen(url).read()
    soup = bs4.BeautifulSoup(html, 'html.parser')
    texts = soup.findAll(text=True)
    return texts


def register():
    signals.content_object_init.connect(calculate_readtime)


def is_visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif isinstance(element, bs4.element.Comment):
        return False
    elif element.string == "\n":
        return False
    return True


def filter_visible_text(page_texts):
    return filter(is_visible, page_texts)

WPM = 200
WORD_LENGTH = 5

def count_words_in_text(text_list, word_length):
    total_words = 0
    for current_text in text_list:
        total_words += len(current_text)/word_length
    return total_words

def estimate_reading_time(content_object):
    if content_object._content is not None:
        content = content_object._content

        filtered_text = filter_visible_text(content)
        total_words = count_words_in_text(filtered_text, WORD_LENGTH)

        minutes = int(math.ceil(total_words/WPM))
        if minutes == 0:
            minutes =1

        content_object.readtime = {
	    "minutes": minutes,
        }


def register():
    signals.content_object_init.connect(estimate_reading_time)
