#!/usr/bin/env python3

"""
file: test_generatefixtures.py
description: an alternative version of generatefixtures.py for testing purposes
"""
import os
import csv
import random
import hashlib
import os.path as path


dir = path.abspath(path.dirname(__file__))
files = {
    'accessories.csv': ('Watches', 'Wallets', 'Purses', 'Satchels',),
    'clothing.csv': ('Blouses', 'Shirts', 'Tanks', 'Cardigans', 'Pants', 'Capris', '"Gingham" Shorts',),
    'household_cleaners.csv': ('Kitchen Cleaner', 'Bathroom Cleaner',),
}


def write_file(writer, length, categories):
    writer.writerow(['email_hash', 'category'])
    for i in range(0, length):
        writer.writerow([
            hashlib.sha256('tech+test{}@pmg.com'.format(i).encode('utf-8')).hexdigest(),
            random.choice(categories),
        ])


def main():
    if not os.path.exists('./test_fixtures'):
        os.makedirs('test_fixtures')
    else:
        for file_name, categories in files.items():
            with open(path.join(dir, 'test_fixtures', file_name), 'w+', encoding='utf-8') as fh:
                write_file(
                    csv.writer(fh, doublequote=False, escapechar='\\', quoting=csv.QUOTE_ALL),
                    random.randint(7, 7),
                    categories
                )
        with open(path.join(dir, 'test_fixtures', 'empty_file.csv'), 'w', encoding='utf-8') as fh:
            pass

if __name__ == '__main__':
    main()
