#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import difflib
import argparse
import requests
from bs4 import BeautifulSoup


COUNTRY_CODES = {
    'en',
    'de',
    'fr',
    'es',
}
LANGUAGES = {
    'en': 'English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
}

URL = "http://dict.leo.org/dictQuery/m-vocab/{0}/query.xml" \
      "?tolerMode=nof&lp={0}&lang=de&rmWords=off&rmSearch=on" \
      "&search={1}&searchLoc=0&resultOrder=basic" \
      "&multiwordShowSingle=on"
URL_PRONOUNCE = 'http://dict.leo.org/media/audio/{0}.mp3'


def similarity(s1, s2):
    return difflib.SequenceMatcher(a=s1.lower(), b=s2.lower()).ratio()


def fetch(phrase, lang):
    url = URL.format(lang, phrase)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    return soup.find_all('entry')


def pronounce(phrase, lang):
    entries = fetch(phrase, lang)
    if not entries:
        return None
    result = []
    for entry in entries:
        for side in entry.find_all('side', lang='en'):
            word = side.find('word').get_text()
            if not side.find('pron'):
                continue
            url = side.find('pron')['url']
            result.append((word, url))
    if not result:
        return False
    result = [x for x in result if phrase in x[0]]
    result.sort(key=lambda x: similarity(x[0], phrase), reverse=True)
    pid = result[0][1]
    url = URL_PRONOUNCE.format(pid)
    play(url)
    return True


def translate(phrase, lang):
    entries = fetch(phrase, lang)
    if not entries:
        return None

    return [tuple([side.find('word').get_text()
                  for side in entry.find_all('side')])
            for entry in entries]


def play(url):
    try:
        import vlc
        player = vlc.MediaPlayer(url)
        player.play()
        while player.get_state() not in (
                vlc.State.Stopped,
                vlc.State.Ended,
                vlc.State.Error,
        ):
            time.sleep(0.1)
        player.stop()
    except ImportError:
        print("Python library vlc not found", file=sys.stderr)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='leo dict cli',
    )
    parser.add_argument(
        '-l',
        '--language',
        help='destination language (default is "%(default)s")',
        default='en',
    )
    parser.add_argument(
        '-p',
        '--pronounce',
        help='pronounce phrase',
        action='store_true',
    )
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
    rcode = main()
    sys.exit(rcode)


# vim: set ft=python sw=4 ts=4 et wrap tw=76:
