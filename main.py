# Derived from https://github.com/pyrogram/pyrogram/blob/develop/examples/get_history.py

import time

from pyrogram import Client
from pyrogram.api.errors import FloodWait


""" Config """
targets = [
    "https://t.me/joinchat/abcdefg"
]  # tips for this: chat_id param in https://docs.pyrogram.ml/pyrogram/Client#pyrogram.Client.get_history


# "ANY" if group purge, your username if user purge
your_username = "ANY"
debug = True

delete_before_time = 3 * 24
# int() is to delete decimals
delete_before = int(time.time() - (delete_before_time * 60 * 60))

#print(delete_before)

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
                from_username = "ID {} (username: {})".format(message.from_user.id, message.from_user.username)
            else:
                from_username = "ID {} (no username)".format(message.from_user.id)

            if your_username == "ANY" or message.from_user.username == your_username:
                if(delete_before > message.date):
                    print("Deleting message from {} (sent {})"
                        .format(from_username, str(message.date)))

                    # Delete message
                    if debug is True:
                        print("Simulate deletion of message (debug mode is enabled)")
                    else:
                        app.delete_messages(message.chat.id, [message.message_id])
                else:
                    print("Read message (too new) from {}".format(from_username))
            else:
                print("Read message from {}".format(from_username))

            print("")

    app.stop()

    # Now the "messages" list contains all the messages sorted by date in
    # descending order (from the most recent to the oldest one)
