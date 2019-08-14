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
import falcon
from wsgiref import simple_server
import serve
from fasttext import load_model
import getopt
from logging import getLogger, StreamHandler, Formatter, INFO
from prepro import preprocess
from falcon.media.validators import jsonschema

TOP_LABELS = 10
PORT = 8000

predict_schema = {
    'title': 'Label texts',
    'description': 'Predict labels to be assigned on texts',
    'type': 'object',
    'required': ['texts'],
    'properties': {
        'texts': {
            'type': 'array',
            'description': 'A list of texts for labeling',
            'items': {
                'type': 'object',
                'required': ['id', 'text'],
                'properties': {
                    'id': {
                        'type': 'integer',
                        'description': 'The id of the text'
                    },
                    'text': {
                        'type': 'string',
                        'description': 'A string of text'
                    }
                }
            }
        }
    }
}


class MultiLabelClassifierServer:
    def __init__(self, model_file):
        self.model = load_model(model_file)

    def predict(self, text, k):
        labels, scores = self.model.predict(text, k)
        return list(zip(list(labels), list(scores)))


class ClassifierResource:
    def __init__(self, logger, classifier, k):
        self.classifier = classifier
        self.k = k
        self.logger = logger

    @jsonschema.validate(predict_schema)
    def on_post(self, req, resp):
        items = req.media.get('texts')
        results = []
        for item in items:
            tid = item.get('id')
            text = item.get('text')
            try:
                prediction = self.classifier.predict(preprocess(text), self.k)
            except Exception as e:
                self.logger.error('Error occurred during prediction: {}'.format(
                    e))
                raise e
            scores = {}
            for label, score in prediction:
                scores[label[9:]] = score
            results.append({
                'id': tid,
                'scores': scores
            })
        resp.media = results


def create_app(progname, model_file, port):
    ch = StreamHandler()
    ch.setFormatter(
        Formatter(
            '[%(asctime)s] [%(process)d] [%(levelname)s] %(message)s',
            '%Y-%m-%d %H:%M:%S %z')
    )
    logger = getLogger(__name__)
    logger.addHandler(ch)
    logger.setLevel(INFO)
    try:
        classifier = MultiLabelClassifierServer(model_file)
        app = falcon.API()
        app.add_route(
            '/classifier', ClassifierResource(logger, classifier, TOP_LABELS))
    except Exception as e:
        logger.error('Failed to initialize with model file {}: {}'.format(
            model_file, e))
        sys.exit(1)
    logger.info('Serving classifier on port {}...'.format(port))
    return app


def main(argv):
    progname = argv[0]
    try:
        opts, _ = getopt.getopt(argv[1:], 'm:p:')
    except Exception as e:
        usage(argv[0])
    model_file = None
    port = PORT
    for opt, arg in opts:
        if opt == '-m':
            model_file = arg
            continue
        if opt == '-p':
            try:
                port = int(arg)
            except:
                usage(argv[0], Exception('Invald port {}'.format(arg)))
    app = create_app(progname, model_file, port)
    with simple_server.make_server('', port, app) as httpd:
        httpd.serve_forever()


def usage(progname, e=None):
    print('Usage: {} model_file [port]'.format(sys.argv[0]), file=sys.stderr)
    if e:
        print(e, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    main(sys.argv)
