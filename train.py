#!/usr/bin/env python3

import sys
import random
import argparse
import leo

def main(argv=None):
    parser = argparse.ArgumentParser(description='pronunciation training')
    parser.add_argument('-s', '--sequential', help='sequential order', action='store_true')
    parser.add_argument('file', help='word list')
    args = parser.parse_args(argv)
    
    with open(args.file, 'r') as f:
        words = [line.strip() for line in f.readlines() if line.strip()]
    if not args.sequential: random.shuffle(words)
    
    for word in words:
        print(word, end='')
        input()
        leo.pronounce(word, 'ende')
    
    return 0

if __name__ == '__main__':
    exit = main()
    sys.exit(exit)

