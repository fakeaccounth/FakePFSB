#(©)CodeXBotz

import os
import asyncio
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import *
from helper_func import *
from database.database import *


@Bot.on_message(filters.command('start') & filters.private & subscribed & subscribed2)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    new_user = False

    # Check if user is new and add them to the database
    if not await present_user(id):
        try:
            await add_user(id)
            new_user = True  # Mark as new user for logging
        except:
            pass

    # Log new user to LOG_CHANNEL
    if new_user:
        log_text = f"👤 New User Started Bot\n\n" \
                   f"🆔 ID: `{id}`\n" \
                   f"👤 Name: {message.from_user.mention}\n" \
                   f"👥 Username: {message.from_user.username or 'N/A'}"
        try:
            await client.send_message(LOG_CHANNEL, log_text)
        except:
            print(f"Failed to log new user {id} to LOG_CHANNEL")

    text = message.text
    if len(text) > 7:
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")

        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))

        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return

        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        track_msgs = []

        for msg in messages:
            caption = (CUSTOM_CAPTION.format(previouscaption=msg.caption.html if msg.caption else "",
                                             filename=msg.document.file_name)
                       if CUSTOM_CAPTION and msg.document else
                       (msg.caption.html if msg.caption else ""))

            reply_markup = None if DISABLE_CHANNEL_BUTTON else msg.reply_markup

            try:
                copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption, parse_mode=ParseMode.HTML,
                                            reply_markup=reply_markup, protect_content=PROTECT_CONTENT)
                if AUTO_DELETE_TIME and copied_msg:
                    track_msgs.append(copied_msg)
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                try:
                    copied_msg = await msg.copy(chat_id=message.from_user.id, caption=caption,
                                                parse_mode=ParseMode.HTML, reply_markup=reply_markup,
                                                protect_content=PROTECT_CONTENT)
                    if AUTO_DELETE_TIME and copied_msg:
                        track_msgs.append(copied_msg)
                except:
                    pass
            except:
                pass

        if track_msgs:
            delete_data = await client.send_message(
                chat_id=message.from_user.id,
                text=AUTO_DELETE_MSG.format(time=AUTO_DELETE_TIME)
            )
            asyncio.create_task(delete_file(track_msgs, client, delete_data))

        return

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("😊 About Me", callback_data="about"),
          InlineKeyboardButton("🔒 Close", callback_data="close")]]
    )

    start_message = START_MSG.format(
        first=message.from_user.first_name,
        last=message.from_user.last_name,
        username=f'@{message.from_user.username}' if message.from_user.username else 'N/A',
        mention=message.from_user.mention,
        id=id
    )

    if START_PIC:
        await message.reply_photo(photo=START_PIC, caption=start_message,
                                  reply_markup=reply_markup, message_effect_id=5104841245755180586)
    else:
        await message.reply_text(text=start_message, reply_markup=reply_markup,
                                 message_effect_id=5104841245755180586)

    try:
        await message.delete()
    except:
        pass
    
#=====================================================================================##

WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

#=====================================================================================##


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton(text="Join Channel", url=client.invitelink),
            InlineKeyboardButton(text="Join Channel", url=client.invitelink2),
        ]
    ]
    try:
        buttons.append(
            [
                InlineKeyboardButton(
                    text = 'Try Again',
                    url = f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text = FORCE_MSG.format(
                first = message.from_user.first_name,
                last = message.from_user.last_name,
                username = None if not message.from_user.username else '@' + message.from_user.username,
                mention = message.from_user.mention,
                id = message.from_user.id
            ),
        reply_markup = InlineKeyboardMarkup(buttons),
        quote = True,
        disable_web_page_preview = True
    )


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

