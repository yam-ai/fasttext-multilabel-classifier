# Multilabel Text Classification with fastText

Created by [Fascebook AI Research](https://research.fb.com/category/facebook-ai-research/), [fastText](https://fasttext.cc/) is a library for efficient learning of words and classification of texts:
> FastText is an open-source, free, lightweight library that allows users to learn text representations and text classifiers. It works on standard, generic hardware. Models can later be reduced in size to even fit on mobile devices.

This project applies fastText to perform multilabel text classification and dockerizes the trainer and classifier for easy deployment.

## Usage

### 1. Prepare the dataset as a sqlite database
The training data is expected to be given as a [sqlite](https://www.sqlite.org/index.html) database. It consists of two tables, `texts` and `labels`, storing the texts and their associated labels:
```SQL
CREATE TABLE IF NOT EXISTS texts (
    id TEXT NOT NULL PRIMARY KEY,
    text TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS labels (
    label TEXT NOT NULL,
    text_id text NOT NULL,
    FOREIGN KEY (text_id) REFERENCES texts(id)
);
CREATE INDEX IF NOT EXISTS label_index ON labels (label);
CREATE INDEX IF NOT EXISTS text_id_index ON labels (text_id);
```

An empty example sqlite file is in `example/data.db`.

Let us take the [toxic comment dataset](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data) published on [kaggle](https://www.kaggle.com/) as an example. (Note: you will need to create a kaggle account in order to download the dataset.) The training data file `train.csv` (not provided by this repository) in the downloaded dataset has the following columns: `id`, `comment_text`, `toxic`, `severe_toxic`, `obscene`, `threat`, `insult`, `identity_hate`. The last six columns represent the labels of the `comment_text`.

The python script in `example/csv2sqlite.py` can process `train.csv` and save the data in a sqlite file `data.db`.

To convert `train.csv` to `data.db`, run the following commands:
```sh
$ python3 csv2sqlite.py -i /downloads/toxic-comment/train.csv -o /repos/bert-multilabel-classifier/example/data.db
```
You can also use the `-n` flag to convert only a subset of examples in the training csv file to reduce the training database size. For example, you can use `-n 1000` to convert only the first 1,000 examples in the csv file into the training database. This may be necessary if there is not enough memory to train the model with the entire raw training set or you want to shorten the training time.

### 2. Tune the parameters
The training and serving parameters can be modified in `settings.py`.

### 3. Train the model
Build the docker image for training:
```sh
$ docker build -f train.Dockerfile -t classifier-train .
```  

Run the training container by mounting the above volumes:
```sh
$ docker run -v $TRAIN_DB:/train.db -v $MODEL_FILE:/model.bin classifier-train
```

* `$TRAIN_DB` is the full path of the input sqlite DB storing the training set, e.g., `/data/example/train.db`.
* `$MODEL_FILE` is the full path to the output fastText trained model, e.g., `/data/example/model.bin`.

### 4. Serve the model
Build the docker image for serving:
```sh
$ docker build -f serve.Dockerfile -t classifier-serve .
```

Run the serving container by mounting the trained model file and exposing the port:
```sh
$ docker run -v $MODEL_FILE:/model.bin -p 8000:8000 classifier-serve
```

### 5. Post an inference HTTP request

Make an HTTP POST request to `http://localhost:8000/classifier` with a JSON body like the following:
```json
{ 
   "texts":[ 
      { 
         "id":0,
         "text":"Three great forces rule the world: stupidity, fear and greed."
      },
      { 
         "id":1,
         "text":"Put your hand on a hot stove for a minute, and it seems like an hour. Sit with a pretty girl for an hour, and it seems like a minute. That's relativity."
      }
   ]
}
```
Then in reply you will get back a list of scores, indicating the likelihoods of the labels for the input texts (e.g., two Albert Einstein quotes as follows):
```json
[
  {
    "id": 0,
    "scores": {
      "toxic": 0.8602798581123352,
      "insult": 0.09022565186023712,
      "obscene": 0.0350012332201004,
      "identity_hate": 0.009289986453950405,
      "threat": 0.0028602471575140953,
      "severe_toxic": 0.002403183374553919
    }
  },
  {
    "id": 1,
    "scores": {
      "toxic": 0.6345628499984741,
      "insult": 0.18238091468811035,
      "obscene": 0.1788458377122879,
      "identity_hate": 0.0024415855295956135,
      "severe_toxic": 0.0016292480286210775,
      "threat": 0.00019956909818574786
    }
  }
]
```

You can test the API using `curl` as follows:

```sh
$ curl -X POST http://localhost:8000/classifier -H "Content-Type: application/json" -d $'{"texts":[{"id":0,"text":"Three great forces rule the world: stupidity, fear and greed."},{"id":1,"text":"Put your hand on a hot stove for a minute, and it seems like an hour. Sit with a pretty girl for an hour, and it seems like a minute. That\'s relativity."}]}'
```

You will get the response like the following:

```
[{"id": 0, "scores": {"toxic": 0.8602798581123352, "insult": 0.09022565186023712, "obscene": 0.0350012332201004, "identity_hate": 0.009289986453950405, "threat": 0.0028602471575140953, "severe_toxic": 0.002403183374553919}}, {"id": 1, "scores": {"toxic": 0.6345628499984741, "insult": 0.18238091468811035, "obscene": 0.1788458377122879, "identity_hate": 0.0024415855295956135, "severe_toxic": 0.0016292480286210775, "threat": 0.00019956909818574786}}]
```
### 6. Profesional services

If you need our architecture consultancy or software customization services, please find us at https://www.yam.ai or https://twitter.com/theYAMai.