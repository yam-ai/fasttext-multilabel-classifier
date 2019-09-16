# coding=utf-8
# Copyright 2019 YAM AI Machinery Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import re
import getopt
import sqlite3
from prepro import normalize_spaces, remove_symbols, preprocess


def format_label(label):
    return '__label__{}'.format(
        '_'.join(normalize_spaces(
            remove_symbols(label)).lower().split()))


def gen_train_file(dbfile, trainfile):
    try:
        conn = sqlite3.connect(dbfile)
    except Exception as e:
        raise Exception('Failed to read database {}: {}'.format(
            dbfile, e), file=sys.stderr)

    try:
        outfile = open(trainfile, 'w')
    except Exception as e:
        raise Exception(
            'Failed to open training file {} for writing: {}'.format(
                trainfile, e))

    try:
        cur = conn.cursor()
        cur.execute('SELECT id, text FROM texts;')
        rows = cur.fetchall()
        texts = []
        i = 0
        for row in rows:
            i += 1
            texts.append((row[0], preprocess(row[1]),))
            if i % 1000 == 0:
                print('Read {} rows.'.format(i))
        print('Read {} rows.'.format(i))
        print('Writing {} rows to training file {}...'.format(len(rows), trainfile))
        i = 0
        for (text_id, text,) in texts:
            i += 1
            cur.execute(
                'SELECT label FROM labels WHERE text_id = ?', (text_id,))
            rows = cur.fetchall()
            labels = [format_label(row[0]) for row in rows]
            print(' '.join(labels + [text]), file=outfile)
            if i % 1000 == 0:
                print('Written {} rows to training file {}.'.format(i, trainfile))
        print('Written {} rows to training file {}.'.format(i, trainfile))
    except sqlite3.Error as e:
        raise Exception(
            'Error reading training database {}: {}'.format(dbfile, e))
    except IOError as e:
        raise Exception(
            'Error writing training file {}: {}'.format(trainfile, e))
    conn.close()


def main(argv):
    trainfile = None
    dbfile = None
    try:
        opts, _ = getopt.getopt(argv[1:], 'i:o:')
        for opt, arg in opts:
            if opt == '-i':
                dbfile = arg
                continue
            if opt == '-o':
                trainfile = arg
                continue
    except Exception as e:
        usage(argv[0], e)
    if not dbfile:
        usage(argv[0], 'Missing db_file')
    if not trainfile:
        usage(argv[0], 'Missing train_file')

    print('Input DB file: {}'.format(dbfile))
    print('Output training file: {}'.format(trainfile))
    try:
        gen_train_file(dbfile, trainfile)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def usage(progname, e=None):
    print('Usage: {} -i db_file -o train_file'.format(progname),
          file=sys.stderr)
    if e:
        print(e, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
