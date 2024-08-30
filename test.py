# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from typing import Dict, Text, Any, List, Union, Optional

from core.action_interfaces import Tracker
from core.action_executor import CollectingDispatcher
from core.action_interfaces import Action, ActionExecutionRejection

from agent_context.context_cache import ContextCache
from agent_context.questions_cache import QuestionCache
from util.actions_helper import *

from mongodb import ai_bots_cache_dao,ai_wa_bots_cache_dao
#import requests
#import datetime
#import util
#import json, random

from string import Template

import validators


class CustomBot104Action(Action):

    def name(self) -> Text:
        return "action_s_104_utter_default"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], dialogs: List[Dict[Text, Any]]) -> List:
        log_message("- action_s_104_utter_default -->", tracker.latest_message)
        bot_id = get_bot_id(tracker.sender_id)


        return []


class CustomBot104Action1(Action):
    def name(self) -> Text:
        return 's_104_handle_liveChatUserForm'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], dialogs: List[Dict[Text, Any]]) -> List:
        # TODO: Check case from DB / Salesforce based on the entities
        userFormValidation = True
        # current_dialog = tracker.latest_message['intent_dialog']
        current_step = tracker.latest_message['current_step'][0]
        # TODO: save CaseId for the flow...in ai cache table
        if userFormValidation:
            # Success flow
            return [{"status": "success"}]

        else:
            return [{"status": "error"}]


class CustomBot104RouteAction(Action):
    def name(self) -> Text:
        return 's_104_handle_route'

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any], dialogs: List[Dict[Text, Any]]) -> List:
        # TODO: Check case from DB / Salesforce based on the entities

        latest_dialog = tracker.events[-1]['latest_message']['intent_dialog']
        list_of_routable_dialogues = latest_dialog['steps'][-1]['next_dialogs']
        all_intents_and_dialogues = {k['intentName']: k['dialogName'] for k in dialogs if
                                     k['dialogName'] in list_of_routable_dialogues}
        achieved_intents = [k['name'] for k in tracker.events[-1]['latest_message']['intent_ranking'][:3]]
        for i in all_intents_and_dialogues.keys():
            if i in achieved_intents:
                return [{"selected_dialog": all_intents_and_dialogues[i]}]
        return [{"status": "error"}]
