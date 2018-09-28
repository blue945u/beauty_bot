import os
import time
import json
from slacker import Slacker
from slackclient import SlackClient
from beauty_bot import BeautyBot
from slack_config import SLACK_BOT_TOKEN, BOT_ID

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

slack_client = SlackClient(SLACK_BOT_TOKEN)
slacker = Slacker(SLACK_BOT_TOKEN)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    bb = BeautyBot()
    print(command)
    if isinstance(command, str):
        response, message_attachments = bb.chat(command)
    else:
        response, message_attachments = bb.chat("not string input")

    #response = "Hi! I am alive."
    # slacker.chat.post_message('#beautybot2', 'Hello fellow slackers!')
    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    # slack_client.api_call("chat.postMessage", channel=channel,
    #                       text=response, as_user=True, attachments=message_attachments)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    try:
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output:
                    print(output['text'])
                    if AT_BOT in output['text']:
                        # return text after the @ mention, whitespace removed #
                        out_put_text = output['text'].split(AT_BOT)[1].strip().lower()
                        # print(out_put_text)
                        return out_put_text, output['channel']
        return None, None
    except:
        return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("BeautyBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            # print(command, channel)
            if command and channel:
                print(command)
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
