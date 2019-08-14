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

TOP_LABELS = 10
PORT = 8000


class MultiLabelClassifierServer:
    def __init__(self, model_file):
        self.model = load_model(model_file)

    def predict(self, text, k):
        labels, scores = self.model.predict(text, k)
        return list(zip(list(labels), list(scores)))


class ClassifierResource:
    def __init__(self, classifier, k):
        self.classifier = classifier
        self.k = k

    def on_post(self, req, resp):
        items = req.media.get('texts')
        results = []
        for item in items:
            tid = item['id']
            text = item['text']
            try:
                prediction = self.classifier.predict(text, self.k)
            except Exception as e:
                print('Error occurred during prediction: {}'.format(
                    e), file=sys.stderr)
                raise e
            scores = {}
            for label, score in prediction:
                scores[label[9:]] = score
            results.append({
                'id': tid,
                'scores': scores
            })
        resp.media = results


def create_app(model_file):
    classifier = MultiLabelClassifierServer(model_file)
    app = falcon.API()
    app.add_route('/classifier', ClassifierResource(classifier, TOP_LABELS))
    return app


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Usage: {} model_file'.format(sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    model_file = sys.argv[1]
    try:
        app = create_app(model_file)
    except Exception as e:
        print('Failed to initialize with model file {}: {}'.format(
            model_file, e), file=sys.stderr)
        sys.exit(1)
    with simple_server.make_server('', PORT, app) as httpd:
        print('Serving HTTP on port {}...'.format(PORT))
        httpd.serve_forever()
