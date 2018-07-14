from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import getLogger
from mycroft.skills.context import adds_context, removes_context
from mycroft.util import play_mp3

import random

_author__ = 'PCWii'
# Release - 20180714

LOGGER = getLogger(__name__)


class GrootTalkSkill(MycroftSkill):
    def __init__(self):
        super(GrootTalkSkill, self).__init__(name="GrootTalkSkill")
        self.groot_talk = False

    def initialize(self):
        self.load_data_files(dirname(__file__))

    def speak_groot(self):
        groot_file_Number = random.randint(1, 4)
        play_groot_file = str(groot_file_Number) + ".mp3"
        play_mp3(join(dirname(__file__), "soundclips", play_groot_file))

    @intent_handler(IntentBuilder('GrootTalkIntent').require("TalkKeyword").require('LikeKeyword').
                    require('GrootKeyword').build())
    @adds_context('GrootChat')
    def handle_groot_talk_intent(self, message):
        groot_file_number = random.randint(1, 4)
        play_groot_file = str(groot_file_number) + ".mp3"
        if not self.groot_talk:
            self.groot_talk = True
            play_mp3(join(dirname(__file__), "soundclips", play_groot_file))
            self.speak_dialog('context', data={"result": ""}, expect_response=True)

    @intent_handler(IntentBuilder('GrootChatIntent').require('GrootChat').build())
    @adds_context('GrootChat')
    def handle_groot_chat_intent(self, message):
        groot_file_number = random.randint(1, 4)
        play_groot_file = str(groot_file_number) + ".mp3"
        if self.groot_talk:
            self.speak_dialog('context', data={"result": ""}, expect_response=True)
            play_mp3(join(dirname(__file__), "soundclips", play_groot_file))

    @intent_handler(IntentBuilder('GrootStopIntent').require('GrootChat').require('IamKeyword').
                    require('GrootKeyword').build())
    @removes_context('GrootChat')
    def handle_stop_groot_intent(self, message):
        groot_file_number = random.randint(1, 4)
        play_groot_file = str(groot_file_number) + ".mp3"
        if self.groot_talk:
            play_mp3(join(dirname(__file__), "soundclips", play_groot_file))
            self.speak_dialog('context', data={"result": "canceled"}, expect_response=False)
        self.groot_talk = True

    def stop(self):
        pass


def create_skill():
    return GrootTalkSkill()
