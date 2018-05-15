import logging
import os
import falcon
from rasa_core.agent import Agent
from rasa_core.interpreter import RasaNLUInterpreter

from communication_layer.rest_api_handling import HelloWorldHandler, ParseHandler, ContinueHandler

# Load config first
logging.basicConfig(level=logging.INFO)

api = falcon.API()

api.add_route('/api/hello', HelloWorldHandler())

interpreter = RasaNLUInterpreter('models/nlu/ner-de/spacy_regex_mb',
                                 'configs/spacy_regex_mb_nlu_model_config.json')
agent = Agent.load('models/dialogue', interpreter=interpreter)

api.add_route('/api/parse', ParseHandler(agent))

# route("/conversations/<sender_id>/continue"
api.add_route('/api/continue', ContinueHandler(agent))

# Serve static source, only for develop purpose!
# For production use nginx or apache
api.add_static_route('/ui', os.path.join(os.getcwd(), 'chat_mockup_gui'))
