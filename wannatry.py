#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackContext, CallbackQueryHandler, CommandHandler, ApplicationBuilder

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    keyboard = [
        [
            InlineKeyboardButton("Option A", callback_data="a"),
            InlineKeyboardButton("Option B", callback_data="b"),
        ]
       
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    # await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")
    await query.edit_message_reply_markup(reply_markup=reply_markup)


async def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5912561023:AAH9OaIMM-bXBEoNlAip0-3ZV28Sc5qMevA").build()
    # application = Application.builder().token("TOKEN").build()

    # app_telegram = ApplicationBuilder().token("5912561023:AAH9OaIMM-bXBEoNlAip0-3ZV28Sc5qMevA").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()





















response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
services = response.json()
response_prices = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getPrices&country=22')
prices = response_prices.json()
service_id_to_name = {key: value for key, value in services.items()}
service_prices = []

for service_id, prices_data in prices['22'].items():
    service_name = service_id_to_name.get(service_id)  # Use get() with a default value of None
    if service_name:
        for price, _ in prices_data.items():
            service_price = {'service': service_name, 'price': price, 'service_ID': service_id}
            service_prices.append(service_price)

# Rest of your code...





async def button_callback(update: Update, context: CallbackContext) -> None:
    # Rest of your code...

    chat_id2 = update.effective_chat.id

    print(chat_id, '==', user_id, "SECOND:", chat_id2)
    query = update.callback_query
    if query.data == 'get_number':
        # Rest of your code...
        service_id_to_name = {key: value for key, value in services.items()}

        # Rest of your code...

        for service_id, prices_data in prices['22'].items():
            # Use the get method to get the service name, with a default value of None
            service_name = service_id_to_name.get(service_id)

            if service_name is None:
                # The service ID is not found in the dictionary, handle the error gracefully
                print(f"Service name not found for service ID: {service_id}")
                continue

            for price, _ in prices_data.items():
                # Rest of your code...
                service_price = {'service': service_name, 'price': price, 'service_ID': service_id}
                service_prices.append(service_price)

        # Rest of your code...
        # Send the keyboard with the service options
        reply_markup = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(chat_id=chat_id, text="Choose a service:", reply_markup=reply_markup)
        return STATE_CHOOSING_ITEM
