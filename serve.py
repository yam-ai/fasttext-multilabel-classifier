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


class MultiLabelClassifierServer:
    pass


class ClassifierResource:
    def __init__(self, classifier):
        self.classifier = classifier

    def on_get(self, req, resp):
        """Handles POST requests"""
        result = {
            'msg': 'to be implemented'
        }
        resp.media = result


def create_app():
    classifier = MultiLabelClassifierServer()
    app = falcon.API()
    app.add_route('/classifier', ClassifierResource(classifier))
    return app


if __name__ == '__main__':
    PORT = 8000
    app = create_app()
    with simple_server.make_server('', PORT, app) as httpd:
        print('Serving HTTP on port {}...'.format(PORT))
        httpd.serve_forever()
