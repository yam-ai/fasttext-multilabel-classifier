# coding=utf-8

import getopt
from sqlite3 import connect
import re
from common.prepro import normalize_spaces, remove_symbols


def format_label(label):
    return '__label__{}'.format(
        normalize_spaces(
            remove_symbols(label)).lower())


def gen_train_file(dbfile, trainfile):
    try:
        conn = connect(dbfile)
    except Exception as e:
        raise Exception('Failed to read DB {}: {}'.format(
            dbfile, e), file=sys.stderr)

    try:
        outfile = open(trainfile, 'w')
    except Exception as e:
        raise Exception(
            'Failed to open training file {} for writing: {}'.format(
                trainfile, e))

    try:
        cur = conn.cusror()
        cur.execute('SELECT id, text FROM texts;')
        rows = cur.fetchall()
        texts = []
        for row in rows:
            texts.append((row[0], row[1],))
        for (text_id, text,) in texts:
            cur.execute(
                'SELECT label FROM labels WHERE text_id = ?', (text_id,))
            rows = cur.fetchall()
            labels = [format_label(row[0]) for row in rows]
            print('{} {}'.format(' '.join(labels), text), file=trainfile)
    except Exception as e:
        raise Exception('Error writing training file: '.format(trainfile))

    conn.close()


def main(argv):
    dbfile = 'train.db'
    trainfile = 'train.txt'
    try:
        opts, _ = getopt.getopt(argv, 'i:o:')
    except Exception as e:
        print('Error: {}'.format(e), file=sys.stderr)
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-i':
            dbfile = arg
            continue
        if opt == '-o':
            trainfile = arg
            continue
    try:
        gen_train_file(dbfile, trainfile)
    except Exception as e:
        print('Error: {}'.format(e), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
