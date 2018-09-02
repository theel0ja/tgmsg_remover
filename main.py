# Derived from https://github.com/pyrogram/pyrogram/blob/develop/examples/get_history.py

import time

from pyrogram import Client
from pyrogram.api.errors import FloodWait


""" Config """
target = "https://t.me/joinchat/Awg5A0UW-tzOLX7zMoTDog"  # tips for this: chat_id param in https://docs.pyrogram.ml/pyrogram/Client#pyrogram.Client.get_history
your_username = "theel0ja"


app = Client("my_account")
messages = []  # List that will contain all the messages of the target chat
offset_id = 0  # ID of the last message of the chunk

app.start()

while True:
    try:
        m = app.get_history(target, offset_id=offset_id)
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
        if message.from_user.username == your_username:
            app.delete_messages(target, [message.message_id])

app.stop()

# Now the "messages" list contains all the messages sorted by date in
# descending order (from the most recent to the oldest one)