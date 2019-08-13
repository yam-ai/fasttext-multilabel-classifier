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

WORKDIR /src/
COPY . /src/

RUN apk add --update \
    build-base \
    && pip install -r /src/requirements.txt

ENV TRAIN_FILE=/train.db
ENV MODEL_FILE=/model.bin
ENV SRC_DIR=/src

CMD ["/src/train.sh"]


