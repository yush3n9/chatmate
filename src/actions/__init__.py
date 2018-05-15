#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from rasa_core.actions import Action
from rasa_core.events import SlotSet, TopicSet
import logging

logger = logging.getLogger(__name__)

class ActionTransferToAgent(Action):
    def name(self):
        return 'action_transfer_to_agent'

    def run(self, dispatcher, tracker, domain):
        logger.info(tracker.slots)
        dispatcher.utter_message(
            "Ihre Anfrage wurde zur Fachabteilung weitergeleitet, Der MA wird sich in Kürze mit Ihnen in Verbindung setzen.")


# YS: Test of Topic stuff
class ActionSetTopic(Action):
    def name(self):
        return 'action_set_topic'

    def run(self, dispatcher, tracker, domain):
        return [TopicSet(tracker.latest_message.intent['name'])]


# YS: Test of Topic stuff
class ActionTraceTracker(Action):
    def name(self):
        return 'action_trace_tracker'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(
            "Trace all of the information tracked by tracker.")
        logger.info('----- slots ------')
        for s in tracker.slots:
            logger.info(s)
            logger.info('----- topics ------')
        for t in tracker.topics:
            logger.info(t.name)
        logger.info('----- current topic ------')
        logger.info(tracker.topic.name)
