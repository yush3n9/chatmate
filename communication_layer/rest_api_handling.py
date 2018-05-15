import json
import logging

import falcon
from rasa_core import events

logger = logging.getLogger(__name__)


class HelloWorldHandler():
    def on_get(self, req, resp):
        result = dict(hello='World')
        resp.media = result
        resp.context_type = falcon.MEDIA_JSON


class ParseHandler():
    def __init__(self, agent):
        self.agent = agent

    def on_post(self, req, resp):
        message = req.media['query']
        sender_id = req.media['sender_id']
        mandant_id = req.media['mandant']
        arr_result = []
        try:
            result = self.agent.start_message_handling(message, sender_id)
            arr_result.append(result)
            status_code = '200 OK'
            if 'onlinebanking_einrichten' in result['tracker']['latest_message']['intent']['name']:
                logger.info('Set mandant id in slot per direct input with slash manually.')
                mandant = dict(mandant=mandant_id)
                arr_result.append(self.agent.start_message_handling('/mitteilen' + json.dumps(mandant), sender_id))
                status_code = '200 OK'
            logger.debug(arr_result)
        except Exception as e:
            status_code = '500 Internal Server Error'
            arr_result.append({"error": "{}".format(e)})

        resp.status = status_code
        resp.media = arr_result
        resp.context_type = falcon.MEDIA_JSON


class ContinueHandler():
    def __init__(self, agent):
        self.agent = agent

    def on_post(self, req, resp):
        encoded_events = req.media.get('events', [])
        executed_action = req.media.get("executed_action", None)
        print('executed action')
        print(executed_action)
        evts = events.deserialise_events(encoded_events, self.agent.domain)
        sender_id = req.media['sender_id']
        try:
            result = self.agent.continue_message_handling(sender_id,
                                                          executed_action,
                                                          evts)
            status_code = '200 OK'
        except ValueError as e:
            status_code = '400 Bad Request'
            result = {"error": e.message}
        except Exception as e:
            status_code = '500 Internal Server Error'
            result = {"error": "Server failure. Error: {}".format(e)}

        resp.status = status_code
        resp.media = result
        resp.context_type = falcon.MEDIA_JSON
