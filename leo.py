#!/usr/bin/env python3

import sys
import time
import difflib
import argparse
import requests
from bs4 import BeautifulSoup

COUNTRY_CODES = {'de', 'en', 'fr', 'es'}
LANGUAGES = {'fr': 'French', 'de': 'German', 'es': 'Spanish', 'en': 'English'}

URL = """http://dict.leo.org/dictQuery/m-vocab/%(lang)s/query.xml?tolerMode=nof&lp=%(lang)s&lang=de&rmWords=off&rmSearch=on&search=%(word)s&searchLoc=0&resultOrder=basic&multiwordShowSingle=on"""
URL_PRONOUNCE = 'http://dict.leo.org/media/audio/%(id)s.mp3'

def similarity(s1, s2):
    return difflib.SequenceMatcher(a=s1.lower(), b=s2.lower()).ratio()

def fetch(phrase, lang):
    url = URL % {'lang': lang, 'word': phrase}
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    return soup.find_all('entry')

def pronounce(phrase, lang):
    entries = fetch(phrase, lang)
    if not entries: return None
    result = []
    for entry in entries:
        for side in entry.find_all('side', lang='en'):
            word = side.find('word').get_text()
            if not side.find('pron'): continue
            url = side.find('pron')['url']
            result.append((word, url))
    if not result: return False
    result.sort(key=lambda x: similarity(x[0], phrase), reverse=True)
    pid = result[0][1]
    url = URL_PRONOUNCE % {'id': pid}
    play(url)
    return True

def translate(phrase, lang):
    entries = fetch(phrase, lang)
    if not entries: return None
    
    return [tuple([side.find('word').get_text()
                  for side in entry.find_all('side')])
            for entry in entries]

def play(url):
    import vlc
    player = vlc.MediaPlayer(url)
    player.play()
    while player.get_state() not in (vlc.State.Stopped, vlc.State.Ended, vlc.State.Error):
        time.sleep(0.1)

def main(argv=None):
    parser = argparse.ArgumentParser(description='leo dict cli')
    parser.add_argument('-l', '--language', help='destination language (default is "%(default)s")', default='en')
    parser.add_argument('-p', '--pronounce', help='pronounce phrase', action='store_true')
    parser.add_argument('phrase', help='phrase to translate')
    args = parser.parse_args(argv)
    
    phrase, lang = args.phrase, args.language + 'de'
    
    if args.pronounce:
        result = pronounce(phrase, lang)
        return 0 if result else 1
    
    translations = translate(phrase, lang)
    if not translations:
        print('no translation found')
        return 1
    
    for trans in translations:
        print('%s\t\t%s' % trans)
    
    return 0

if __name__ == '__main__':
    exit = main()
    sys.exit(exit)

