import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, WEBSITE_URL, WEBSITE_URL_MODE
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went Wrong..!")
        return

    # Generate base64-encoded ID
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)

    # Generate website and bot links
    website_link = f"{WEBSITE_URL}?rohit_18={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Create inline keyboard with both links
    buttons = [
        [InlineKeyboardButton("🔗 Website Link", url=website_link)] if WEBSITE_URL_MODE else [],
        [InlineKeyboardButton("🔁 Share Bot Link", url=f'https://telegram.me/share/url?url={bot_link}')],
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    # Edit reply with both links
    message_text = "<b>Here are your links:</b>\n\n"
    if WEBSITE_URL_MODE:
        message_text += f"<b>Website:</b> {website_link}\n"
    message_text += f"<b>Bot:</b> {bot_link}"

    await reply_text.edit(message_text, reply_markup=reply_markup, disable_web_page_preview=True)

    # Optionally update the post's reply markup
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)

@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    if DISABLE_CHANNEL_BUTTON:
        return

    # Generate base64-encoded ID
    converted_id = message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)

    # Generate website and bot links
    website_link = f"{WEBSITE_URL}?rohit_18={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Create inline keyboard with both links
    buttons = [
        [InlineKeyboardButton("🔗 Website Link", url=website_link)] if WEBSITE_URL_MODE else [],
        [InlineKeyboardButton("🔁 Share Bot Link", url=f'https://telegram.me/share/url?url={bot_link}')],
    ]

    reply_markup = InlineKeyboardMarkup(buttons)

    # Update the message's reply markup
    try:
        await message.edit_reply_markup(reply_markup)
    except Exception as e:
        print(e)
        pass