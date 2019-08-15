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
import os
import getopt
from gen_train import gen_train_file
from gen_model import gen_model_file
from settings import TRAIN_DB, MODEL_BIN
import tempfile


def main(argv):
    progname = argv[0]
    try:
        opts, _ = getopt.getopt(argv[1:], 'i:o:')
    except Exception as e:
        usage(argv[0])
    db_dir = None
    model_dir = None
    for opt, arg in opts:
        if opt == '-i':
            db_dir = arg
            continue
        if opt == '-o':
            model_dir = arg
            continue
    if not db_dir:
        usage(progname, 'Missing train_dir')
    if not model_dir:
        usage(progname, 'Missing model_dir')
    temp_file = tempfile.NamedTemporaryFile()
    try:
        gen_train_file(os.path.join(db_dir, TRAIN_DB), temp_file.name)
        gen_model_file(temp_file.name, os.path.join(model_dir, MODEL_BIN))
    except Exception as e:
        print(e, file=sys.stderr)
    temp_file.close()


def usage(progname, e=None):
    print('Usage: {} -i train_dir -o model_dir'.format(progname), file=sys.stderr)
    if e:
        print(e, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
