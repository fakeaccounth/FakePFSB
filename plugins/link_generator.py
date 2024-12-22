from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, WEBSITE_URL, WEBSITE_URL_MODE, USE_SHORTLINK, SHORTLINK_API_URL, SHORTLINK_API_KEY
from helper_func import encode, get_message_id
from shortzy import Shortzy

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(
                text="Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply(
                "❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel",
                quote=True
            )
            continue

    while True:
        try:
            second_message = await client.ask(
                text="Forward the Last Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply(
                "❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel",
                quote=True
            )
            continue

    # Generate encoded batch link
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)

    # Generate links
    website_link = f"{WEBSITE_URL}?rohit_18={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Shorten the bot link if enabled using Shortzy API
    shortzy = Shortzy(api_key=SHORTLINK_API_KEY, base_site=SHORTLINK_API_URL)
    short_bot_link = bot_link
    if USE_SHORTLINK:
        short_bot_link = await shortzy.convert(bot_link)

    # Inline keyboard with all links
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Open on Website", url=website_link)] if WEBSITE_URL_MODE else [],
        [InlineKeyboardButton("🔗 Bot Link (Shortened)", url=short_bot_link)],
        [InlineKeyboardButton("🔁 Telegram Bot Link", url=bot_link)],
    ])

    await second_message.reply_text(
        f"<b>Here is your link</b>\n\n"
        f"Shortened Bot Link: {short_bot_link}\n"
        f"Bot Link: {bot_link}\n"
        f"{f'Website Link: {website_link}' if WEBSITE_URL_MODE else ''}",
        quote=True,
        reply_markup=reply_markup
    )


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(
                text="Forward Message from the DB Channel (with Quotes)..\n\nor Send the DB Channel Post link",
                chat_id=message.from_user.id,
                filters=(filters.forwarded | (filters.text & ~filters.forwarded)),
                timeout=60
            )
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply(
                "❌ Error\n\nThis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel",
                quote=True
            )
            continue

    # Generate encoded link
    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")

    # Generate links
    website_link = f"{WEBSITE_URL}?rohit_18={base64_string}" if WEBSITE_URL_MODE else None
    bot_link = f"https://t.me/{client.username}?start={base64_string}"

    # Shorten the bot link if enabled using Shortzy API
    shortzy = Shortzy(api_key=SHORTLINK_API_KEY, base_site=SHORTLINK_API_URL)
    short_bot_link = bot_link
    if USE_SHORTLINK:
        short_bot_link = await shortzy.convert(bot_link)

    # Inline keyboard with all links
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Open on Website", url=website_link)] if WEBSITE_URL_MODE else [],
        [InlineKeyboardButton("🔗 Bot Link (Shortened)", url=short_bot_link)],
        [InlineKeyboardButton("🔁 Telegram Bot Link", url=bot_link)],
    ])

    await channel_message.reply_text(
        f"<b>Here is your link</b>\n\n"
        f"Shortened Bot Link: {short_bot_link}\n"
        f"Bot Link: {bot_link}\n"
        f"{f'Website Link: {website_link}' if WEBSITE_URL_MODE else ''}",
        quote=True,
        reply_markup=reply_markup
    )