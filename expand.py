#!/usr/bin/env python3
#  -*- coding: UTF-8 -*-
"""
Expand text with broader and narrower concepts using ARPA.
"""
import argparse
import glob

from arpa_linker.arpa import post

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="Textblock classifier to poems and other text")
    argparser.add_argument("path", help="Path to expand")
    args = argparser.parse_args()

    path = args.path if args.path[-1] != '/' else args.path + '*.*'
    files = glob.glob(path)
    print(path)
    print(len(files))

    url = 'http://demo.seco.tkk.fi/arpa/koko-related'

    for i, file in enumerate(files):
        with open(file, 'r') as f:
            text = f.read()

        data = {'text': text}
        expanded = post(url, data, retries=5)

        narrowers = [match['properties'].get('narrow', '') for match in expanded['results']]
        broaders = [match['properties'].get('broad', '') for match in expanded['results']]

        narrowers = set(item.strip('"') for sublist in narrowers for item in sublist)
        broaders = set(item.strip('"') for sublist in broaders for item in sublist)

        print('Broaders: %s  - Narrowers: %s' % (len(broaders), len(narrowers)))
        # print(sorted(narrowers))
        # print()
        # print(sorted(broaders))
        # quit()
        #
        text += "\n\n"
        text += " ".join(narrowers)
        text += " ".join(broaders)

        with open('expanded_{id}.txt'.format(id=i), 'w') as f:
            f.write(text)

