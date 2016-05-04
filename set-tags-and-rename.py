#!/usr/bin/python
# coding=utf-8

import os
import time
import re
from subprocess import call
import argparse

VALID_CHARACTERS = '[ō\w0-9\s\,\&\(\)\.\!\'\[\]\#\_]'

parser = argparse.ArgumentParser(description='Scan a list of .mp3-Files and add artist/title id3 information')
parser.add_argument('file', nargs='?', default=None, help='If only one specific file should be processed')
parser.add_argument('--silent', action='store_true')
parser.add_argument('--execute', action='store_true')
args = parser.parse_args()


def process_file(file_name):
    if file_name.endswith('.mp3'):
        match = re.search('({valid_chars}*) \- ({valid_chars}*)\-(.*)'.format(valid_chars=VALID_CHARACTERS), file_name)
        if match is not None:
            artist_candidate = match.group(1)
            title_candidate = match.group(2)
            trash = match.group(3)
            if not args.silent:
                print 'Extracted from "{}"'.format(file_name)
                print 'Artist: \'{}\''.format(artist_candidate)
                print 'Title: \'{}\''.format(title_candidate)
        else:
            match = re.search('({valid_chars}*)\-(.*)'.format(valid_chars=VALID_CHARACTERS), file_name)
            if match is not None:
                artist_candidate = 'MrMoMMusic'
                title_candidate = match.group(1)
                trash = match.group(2)
                if not args.silent:
                    print 'Extracted from "{}"'.format(file_name)
                    print 'Artist: \'{}\''.format(artist_candidate)
                    print 'Title: \'{}\''.format(title_candidate)
            else:
                if not args.silent:
                    print 'No information matched for file "{}"'.format(file_name)
                with open('no_match.txt', 'a') as no_match_log:
                    no_match_log.write(file_name + '\n')
        if artist_candidate and title_candidate:
            print '#####'
            print '{}'.format(file_name)
            print '{} - {}'.format(artist_candidate, title_candidate)
            if args.execute:
                print 'gemächt'
                call(['mp3info', '-a {}'.format(artist_candidate), '-t {}'.format(title_candidate), '-g {}'.format('52'), '{}'.format(os.path.join('downloads', file_name))])


if __name__ == '__main__':
    if args.file is not None:
        process_file(args.file)
    else:
        for file_name in os.listdir('downloads'):
            process_file(file_name)
            #raw_input('Press Enter to continue')
