#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import random
import argparse
import leo


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='pronunciation training',
    )
    parser.add_argument(
        '-s',
        '--sequential',
        help='sequential order',
        action='store_true',
    )
    parser.add_argument(
        '-p',
        '--pronounce',
        help='pronounce word',
        action='store_true',
    )
    parser.add_argument('file', help='word list')
    args = parser.parse_args(argv)

    lang = 'ende'

    with open(args.file, 'r') as f:
        words = [line.strip() for line in f.readlines() if line.strip()]
    if not args.sequential:
        random.shuffle(words)

    for word in words:
        print(word, end='')
        input()

        subs = [sub.strip() for sub in word.split('/')]
        for sub in subs:
            subs_len = len(subs)
            if subs_len > 1:
                print("%s:" % sub)
            translations = leo.translate(sub, lang)
            if not translations:
                print("\tnot found")
            else:
                for translation in translations:
                    print("\t%s - %s" % translation)
        if args.pronounce:
            leo.pronounce(subs[0], lang)
            for sub in subs[1:]:
                time.sleep(0.3)
                leo.pronounce(sub, lang)

    return 0


if __name__ == '__main__':
    exit = main()
    sys.exit(exit)


# vim: set ft=python sw=4 ts=4 et wrap tw=76:
