import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, MessageIdInvalid
from shortzy import Shortzy

from bot import Bot
from config import *
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
    website_link = f"{WEBSITE_URL}?codexbot={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Shorten the bot link if enabled
    shortzy = Shortzy(api_key=SHORTLINK_API_KEY, base_site=SHORTLINK_API_URL)
    short_bot_link = bot_link
    if USE_SHORTLINK:
        short_bot_link = await shortzy.convert(bot_link)

    # Create inline keyboard
    buttons = []
    if WEBSITE_URL_MODE:
        buttons.append([InlineKeyboardButton("🔗 Website Link", url=website_link)])
    buttons.append([InlineKeyboardButton("🔁 Bot Link (Original)", url=bot_link)])
    if USE_SHORTLINK:
        buttons.append([InlineKeyboardButton("⚡️ Shortened Bot Link", url=short_bot_link)])

    reply_markup = InlineKeyboardMarkup(buttons)

    # Edit reply with all links
    message_text = "<b>Here are your links:</b>\n\n"
    if WEBSITE_URL_MODE:
        message_text += f"<b>Website:</b> {website_link}\n"
    message_text += f"<b>Bot (Original):</b> {bot_link}\n"
    if USE_SHORTLINK:
        message_text += f"<b>Bot (Shortened):</b> {short_bot_link}"

    await reply_text.edit(message_text, reply_markup=reply_markup, disable_web_page_preview=True)

    # Optionally update the post's reply markup
    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)


@Bot.on_message(filters.channel & filters.incoming & filters.chat(CHANNEL_ID))
async def new_post(client: Client, message: Message):
    print(f"New post in channel: {message.id}")
    if DISABLE_CHANNEL_BUTTON:
        return

    # Generate encoded ID and links
    converted_id = message.id * abs(client.db_channel.id)
    base64_string = await encode(f"get-{converted_id}")
    website_link = f"{WEBSITE_URL}?codexbot={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Shorten link using Shortzy
    short_bot_link = bot_link
    try:
        shortzy = Shortzy(api_key=SHORTLINK_API_KEY, base_site=SHORTLINK_API_URL)
        if USE_SHORTLINK:
            short_bot_link = await shortzy.convert(bot_link)
    except Exception as e:
        print(f"Shortzy API Error: {e}")

    # Create buttons
    buttons = []
    if WEBSITE_URL_MODE:
        buttons.append([InlineKeyboardButton("🔗 Website Link", url=website_link)])
    buttons.append([InlineKeyboardButton("🔁 Bot Link (Original)", url=bot_link)])
    if USE_SHORTLINK:
        buttons.append([InlineKeyboardButton("⚡️ Shortened Bot Link", url=short_bot_link)])

    reply_markup = InlineKeyboardMarkup(buttons)

    try:
        # Attempt to edit the reply markup of the message
        await message.edit_reply_markup(reply_markup)
    except pyrogram.errors.MessageIdInvalid:
        print(f"Invalid Message ID for edit: {message.id}. Sending new message instead.")
        # Send a new message with the reply markup
        await client.send_message(
            chat_id=message.chat.id,
            text="Here are the updated links:",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Error editing reply markup: {e}")