# coding=utf-8
import sys
import re
import getopt
from sqlite3 import connect, Error
from prepro import normalize_spaces, remove_symbols, preprocess


def format_label(label):
    return '__label__{}'.format(
        normalize_spaces(
            remove_symbols(label)).lower())


def gen_train_file(dbfile, trainfile):
    print('dbfile = {}, trainfile = {}'.format(dbfile, trainfile))
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
        cur = conn.cursor()
        cur.execute('SELECT id, text FROM texts;')
        rows = cur.fetchall()
        texts = []
        for row in rows:
            texts.append((row[0], preprocess(row[1]),))
        for (text_id, text,) in texts:
            cur.execute(
                'SELECT label FROM labels WHERE text_id = ?', (text_id,))
            rows = cur.fetchall()
            labels = [format_label(row[0]) for row in rows]
            print('{} {}'.format(' '.join(labels), text), file=outfile)
    except Error as e:
        raise Exception(
            'Error reading training DB {}: {}'.format(trainfile, e))
    except IOError as e:
        raise Exception(
            'Error writing training file {}: {}'.format(trainfile, e))

    conn.close()


def main(argv):
    dbfile = 'train.db'
    trainfile = 'train.txt'
    try:
        opts, _ = getopt.getopt(argv[1:], 'i:o:')
    except Exception as e:
        print('Argument error: {}'.format(e), file=sys.stderr)
        sys.exit(1)
    print(argv)
    print(opts)
    for opt, arg in opts:
        print('opt={},arg={}'.format(opt, arg))
        if opt == '-i':
            dbfile = arg
            continue
        if opt == '-o':
            trainfile = arg
            continue
    print('dbfile = {}, trainfile = {}'.format(dbfile, trainfile))
    try:
        gen_train_file(dbfile, trainfile)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
