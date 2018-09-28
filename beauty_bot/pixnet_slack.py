# coding=UTF-8
import sys, os, datetime, time, re
import random
from slackbot import bot

TOKEN_MYBOT = 'xoxb-237810159383-gkbQlEydpkx9bM7OdqJkLJcV'
bot.settings.API_TOKEN = TOKEN_MYBOT

from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to


def algorithm(question_string):
    answer_string = u"我是回答"
    return answer_string


@listen_to(unicode("問題", 'utf-8') + ' (.*)')
def receive_question(message, question_string):
    if message._client.users[message._get_user_id()][u'name'] == "pixbot":
        answer = algorithm(question_string)
        message.send(answer)


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    main()