# Chatmate
A chatbot which understands user input by applying intent classification and NER, and generates a suggestion of possible response based on neural network. Current version has only been trained and tested in german language.

## Chatbot Setup Instructions:
* virtualenv venv -p /usr/bin/python3
* source venv/bin/activate
* pip install -r requirements.txt
* python -m spacy download de
* python -m rasa_nlu.train -c configs/spacy_regex_mb_nlu_model_config.json
* python -m rasa_core.train -s data/usecases_basic.md -d data/domain.yml -o models/dialogue --epochs 300
* gunicorn communication_layer.application:api -c gunicorn.cfg
* curl -i -H 'Content-type:application/json; charset=UTF-8' -XPOST localhost:8000/api/parse -d '{"query":"Ich bin Tom Hanks", "sender_id":"12345"}'
* Demo UI is available under localhost:8000/ui/chat.html.

## NLU Training Data Tool:
Read https://github.com/RasaHQ/rasa-nlu-trainer for details about setup, usage.
rasa-nlu-trainer

## Cross validate of nlu model:
python -m rasa_nlu.evaluate -d data/nlu_traindata.json -c configs/spacy_regex_mb_nlu_model_config.json --mode crossvalidation
```
INFO:__main__:CV evaluation (n=10)
INFO:__main__:F1-score: 0.837 (0.052)
INFO:__main__:Precision: 0.914 (0.000)
INFO:__main__:Accuracy: 0.849 (0.044)
INFO:__main__:Finished evaluation
```

## Start nlu as server
python -m rasa_nlu.server  -c configs/spacy_regex_mb_nlu_model_config.json

## Visulaization of dialogue training data:
python -m rasa_core.visualize -d data/domain.yml -s data/usecases_basic.md -o usecases_basic.png

## Run Chatbot in console
python -m rasa_core.run -d models/dialogue -u models/nlu/ner-de/spacy_regex_mb/

## Run Chatbot as Server
python -m rasa_core.server -d models/dialogue -u models/nlu/ner-de/spacy_regex_mb/ --cors http://localhost:63342

## Start Chatbot with falcon
gunicorn communication_layer.application:api -c gunicorn.cfg
Visit localhost:8000/ui/chat.html
