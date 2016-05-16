'''Extracts Twitter handle of top 100 the most following people.

'''


import urllib
from bs4 import BeautifulSoup

URL = 'http://twittercounter.com/pages/100'


def get_handles():
    html = urllib.urlopen(URL).read()
    bs = BeautifulSoup(html, 'html.parser')
    links = bs.find_all('a', {'class': 'uname'})
    handles = [link.text for link in links]
    return handles

if __name__ == '__main__':
    hendles = get_handles()
    with open('hendles.txt', 'w') as f:
        for hendle in hendles:
            f.write(hendle[1:] + '\n')
