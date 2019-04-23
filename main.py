# Derived from https://github.com/pyrogram/pyrogram/blob/develop/examples/get_history.py

import time

from pyrogram import Client
from pyrogram.api.errors import FloodWait


""" Config """
targets = [
    "https://t.me/joinchat/abcdefg"
]  # tips for this: chat_id param in https://docs.pyrogram.ml/pyrogram/Client#pyrogram.Client.get_history


your_username = "username"


for target in targets:

    app = Client("my_account")
    messages = []  # List that will contain all the messages of the target chat
    offset_id = 0  # ID of the last message of the chunk

    app.start()

    chat_id = app.get_chat(target).id

    while True:
        try:
            m = app.get_history(chat_id, offset_id=offset_id)
        except FloodWait as e:
            # For very large chats the method call can raise a FloodWait
            print("waiting {}".format(e.x))
            time.sleep(e.x)  # Sleep X seconds before continuing
            continue

        if not m.messages:
            break

        messages += m.messages
        offset_id = m.messages[-1].message_id

        for message in messages:
            if(type(message.from_user.username) is str):
                username = message.from_user.username
                username = " from " + username
            else:
                username = ""

            print("Read message" + username)
            if message.from_user.username == your_username:
                print("Deleting message")
                app.delete_messages(message.chat.id, [message.message_id])

    app.stop()

    # Now the "messages" list contains all the messages sorted by date in
    # descending order (from the most recent to the oldest one)
