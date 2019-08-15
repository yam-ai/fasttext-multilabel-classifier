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

FROM python:3.7.4-alpine3.10

WORKDIR /srv/
COPY . /srv/

VOLUME [ "/train", "/model" ]

RUN apk add --update \
    build-base \
    && pip install -r /srv/train_requirements.txt

ENV TRAIN_DIR=/train
ENV MODEL_DIR=/model
ENV SRC_DIR=/srv

CMD ["/srv/train.sh"]


