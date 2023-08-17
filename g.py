

async def check_otp_code_availability(context: CallbackContext, chat_id: int, api_key: str, id: str, cancel_flag: asyncio.Event) -> None:
    while not cancel_flag.is_set():
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")
    
        if response.status_code == 200 and "STATUS_OK" in response.text:
            respond = response.text.split(':')[1]
            await context.bot.send_message(chat_id=chat_id, text=f"CODE: {respond}")
            break 
        elif response.status_code == 200 and "STATUS_CANCEL" in response.text:
            break
        await asyncio.sleep(2)

def service_callback(update, context):
    async def check_otp_code_availability(context, chat_id, api_key, id, cancel_flag):
        while not cancel_flag.is_set():
            response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")
    
            if response.status_code == 200 and "STATUS_OK" in response.text:
                respond = response.text.split(':')[1]       
                await context.bot.send_message(chat_id=chat_id, text=f"CODE: {respond}")
                break 
            elif response.status_code == 200 and "STATUS_CANCEL" in response.text:
                break
            await asyncio.sleep(2)
    
    query = update.callback_query  
   
    chat_id = update.effective_chat.id
    api_key = get_api_key(chat_id)

    service = query.data
    response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={service}&country=22')
    responded = response.text
    if responded == "NO_BALANCE":
        await context.bot.send_message(chat_id=query.message.chat_id, text="Your balance is low, please add money.")
    elif query.data == 'add1_balance':
        await context.bot.send_message(chat_id=query.message.chat_id, text="https://otpindia.xyz")
        return API_KEY_CHOOSE
    elif query.data == 'to_add':
        await context.bot.send_message(chat_id=query.message.chat_id, text="https://telegra.ph/HOW-TO-ADD-BALANCE-05-31")
        return API_KEY_CHOOSE
    else:
        access_number = responded.split(":")[2]
        main_id = responded.split(':')[1]
        save_main_id(chat_id, main_id)
        message_id = query.message.message_id
        context.user_data['message_key'] = message_id
       
        sms_keyboard = [
            [
                InlineKeyboardButton("Cancel Activation", callback_data='8'),
                InlineKeyboardButton("Request New SMS", callback_data='3')
            ],
            [InlineKeyboardButton("Check OTP Code", callback_data="otp_code")]
        ]   
        message = "Cancel Activation or Request another SMS:"
        reply_markup = InlineKeyboardMarkup(sms_keyboard)
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"{message}\n\nNumber: \U0001F4F1 {access_number}\nID:{main_id}", reply_markup=reply_markup)
        cancel_flag = asyncio.Event()
        save_cancel_flag(chat_id, cancel_flag)
    
        asyncio.create_task(check_otp_code_availability(context, query.message.chat_id, api_key, main_id, cancel_flag))
    
    return STATE_CONFIRMATION  

async def cancel_activation(update, context):
    query = update.callback_query
    chat_id = update.effective_chat.id
    api_key = get_api_key(chat_id)
    id = get_main_id(chat_id)
    cancel_flag = get_cancel_flag(chat_id)
    
    button_list = [[KeyboardButton("⬅️ Back"), KeyboardButton("\U0001F3E1 Home")]]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True, one_time_keyboard=True)
    
    if query.data == "otp_code":
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")
        if response.text == "STATUS_WAIT_CODE":
            await context.bot.send_message(chat_id=query.message.chat_id, text="Wait for the code", reply_markup=reply_markup)
        elif response.status_code == 200 and "STATUS_OK" in response.text:
            respond = response.text.split(':')[1]
            
            await context.bot.send_message(chat_id=query.message.chat_id, text=f"CODE:{respond}", reply_markup=reply_markup)
        elif response.text == "STATUS_CANCEL":
            await context.bot.send_message(chat_id=query.message.chat_id, text="The activation was cancelled.", reply_markup=reply_markup)
        return STATE_CONFIRMATION
    elif query.data == '8':    
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status=8")

        if response.status_code == 200 and "ACCESS_CANCEL" in response.text:
            cancel_flag.set()
            # Disable the "Cancel Activation" button
            reply_markup = InlineKeyboardMarkup([])
            query.message.edit_reply_markup(reply_markup=reply_markup)
            await context.bot.send_message(chat_id=query.message.chat_id, text="\U0001F534 Activation Cancelled\n\nPress \U0001F3E1 Home to go to main menu\n         ⬅️ Back to go back to services", reply_markup=reply_markup)   
    elif query.data == '3':
            response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status=3")
            if response.status_code == 200 and 'ACCESS_WAITING' in response.text:
                await context.bot.send_message(chat_id=query.message.chat_id, text="Sending SMS", reply_markup=reply_markup)
                cancel_flag = asyncio.Event()
                save_cancel_flag(chat_id, cancel_flag)
                asyncio.create_task(check_otp_code_availability(context, query.message.chat_id, api_key, id, cancel_flag))











































































































# import os
# import requests
# import asyncio
# from dotenv import load_dotenv
# from flask import Flask
# from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
# from telegram.ext import (
#     ConversationHandler,
#     CommandHandler,
#     CallbackQueryHandler,
#     CallbackContext,
#     MessageHandler,
#     filters,
#     ApplicationBuilder,
#     Updater,
# )
# from databse import save_api_key, get_api_key, save_main_id, get_main_id, get_cancel_flag, save_cancel_flag

# load_dotenv()

# TOKEN = os.getenv('TOKEN')

# STATE_CHOOSING_OPTION, API_KEY_CHOOSE, STATE_CHOOSING_ITEM, STATE_CONFIRMATION, STATE_END = range(5)

# main_menu_keyboard = [
#     [
#         InlineKeyboardButton("\U0001F4F2 Get Number", callback_data='get_number'),
#         InlineKeyboardButton("\U0001F4B0 Check Balance", callback_data='check_balance')
#     ],
#     [
#         InlineKeyboardButton("\U0001F503 Add Balance", callback_data='add_balance'),
#         InlineKeyboardButton("\U0001F503 Support Channel", callback_data='support_channel')
#     ],
#     [InlineKeyboardButton("\U0001F503 Help and Support", callback_data='help_support')]
# ]

# async def check_otp_code_availability(context: CallbackContext, chat_id: int, api_key: str, id: str, cancel_flag: asyncio.Event) -> None:
#     while not cancel_flag.is_set():
#         response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")

#         if response.status_code == 200 and "STATUS_OK" in response.text:
#             respond = response.text.split(':')[1]
#             await context.bot.send_message(chat_id=chat_id, text=f"DODE: {respond}")
#             break
#         elif response.status_code == 200 and "STATUS_CANCEL" in response.text:
#             break
#         await asyncio.sleep(2)

# async def start(update: Update, context: CallbackContext) -> int:
#     chat_id = update.message.chat_id
#     first_name = update.effective_user.first_name
#     api_buttons = [
#         [InlineKeyboardButton("\U0001F4F2 Get API KEY", callback_data='get_api')],
#         [InlineKeyboardButton("\U0001F4B0 Generate Access Key", callback_data='get_access')]
#     ]
    
#     reply_markup = InlineKeyboardMarkup(api_buttons)
#     await context.bot.send_message(chat_id=chat_id, text=f"\U0001F510 Hello {first_name}, Please enter your API key.", reply_markup=reply_markup)
#     return STATE_CHOOSING_OPTION

# async def generate_access_key(update: Update, context: CallbackContext) -> int:
#     callback_query = update.callback_query
#     chat_id_effective = update.effective_chat.id
    
#     if callback_query is None:
#         api_key = update.message.text.strip()

#         save_api_key(chat_id_effective, api_key)
#         url = f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getBalance"
#         response = requests.get(url)
        
#         if response.status_code == 200 and "ACCESS_BALANCE" in response.text:
#             message = "Welcome to the main menu. Please select a service:"
#             reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
#             await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
#             return API_KEY_CHOOSE
#         else:
#             message = "Invalid API key\n\U0001F510 Please enter your API key again."
#             await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
#             return STATE_CHOOSING_OPTION

#     else:
#         await context.bot.edit_message_text(
#             chat_id=chat_id_effective,
#             message_id=callback_query.message.message_id,
#             text="\U0001F510 Please enter your API key.",
#         )
#         return STATE_CHOOSING_OPTION

# async def button_callback(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     query.answer()
#     query.edit_message_text(text="\U0001F510 Please select a service:")
#     return STATE_CHOOSING_ITEM

# async def service_callback(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     chat_id = query.message.chat_id
#     message_id = query.message.message_id
#     text = query.data

#     if text == "check_balance":
#         api_key = get_api_key(chat_id)
#         url = f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getBalance"
#         response = requests.get(url)

#         if response.status_code == 200 and "ACCESS_BALANCE" in response.text:
#             balance = response.text.split(":")[1]
#             message = f"Your balance is: {balance}"
#         else:
#             message = "Unable to retrieve balance"

#         await context.bot.send_message(chat_id=chat_id, text=message)
    
#     elif text == "get_number":
#         api_key = get_api_key(chat_id)
#         url = f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=instagram"
#         response = requests.get(url)

#         if response.status_code == 200 and "ACCESS_NUMBER" in response.text:
#             number = response.text.split(":")[1]
#             message = f"Your number is: {number}"
#             save_main_id(chat_id, number)
#             cancel_flag = get_cancel_flag(chat_id)
#             cancel_flag.clear()
#             await check_otp_code_availability(context, chat_id, api_key, number, cancel_flag)
#         else:
#             message = "Unable to retrieve number"
        
#         await context.bot.send_message(chat_id=chat_id, text=message)

#     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\U0001F510 Please select a service:")
#     return STATE_CHOOSING_ITEM

# async def cancel_activation(update: Update, context: CallbackContext) -> int:
#     query = update.callback_query
#     chat_id = query.message.chat_id
#     message_id = query.message.message_id
#     text = query.data

#     if text == "cancel_activation":
#         main_id = get_main_id(chat_id)
#         api_key = get_api_key(chat_id)
#         cancel_flag = get_cancel_flag(chat_id)
#         cancel_flag.set()
#         url = f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&status=8&id={main_id}"
#         response = requests.get(url)

#         if response.status_code == 200 and "ACCESS_CANCEL" in response.text:
#             message = "Activation canceled successfully"
#         else:
#             message = "Unable to cancel activation"

#         await context.bot.send_message(chat_id=chat_id, text=message)
    
#     await context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="\U0001F510 Please select a service:")
#     return STATE_CHOOSING_ITEM

# async def end(update: Update, context: CallbackContext) -> int:
#     chat_id = update.effective_chat.id

#     cancel_flag = get_cancel_flag(chat_id)
#     if cancel_flag.is_set():
#         cancel_flag.clear()

#     await context.bot.send_message(chat_id=chat_id, text="\U0001F44B Thank you for using our service. Have a great day!")
#     return ConversationHandler.END

# async def help_support(update: Update, context: CallbackContext) -> None:
#     chat_id = update.message.chat_id
#     message = "For any support or assistance, please contact us at support@example.com"
#     await context.bot.send_message(chat_id=chat_id, text=message)

# def main() -> None:
#     app_builder = ApplicationBuilder().token("6133650307:AAE01VjwtgusxRcu_HR_uX1fEEiCQqoj97w").build()
#     # STATE_CHOOSING_OPTION: [MessageHandler(filters.TEXT & (~ filters.COMMAND), generate_access_key),
#     #                                     CallbackQueryHandler(generate_access_key)
#     #                                     ],
#     # app_builder.configure_storage('sqlalchemy', name='sqlite:///database.db')
#     app_builder.add_handler(CommandHandler('start', start))
#     app_builder.add_handler(MessageHandler(filters.TEXT & (~ filters.COMMAND), start))
     
#     app_builder.add_handler(CallbackQueryHandler(generate_access_key, pattern="get_api"))
#     app_builder.add_handler(CallbackQueryHandler(generate_access_key, pattern="get_access"))
#     app_builder.add_handler(CallbackQueryHandler(service_callback, pattern="check_balance"))
#     app_builder.add_handler(CallbackQueryHandler(service_callback, pattern="get_number"))
#     app_builder.add_handler(CallbackQueryHandler(cancel_activation, pattern="cancel_activation"))
#     app_builder.add_handler(CallbackQueryHandler(help_support, pattern="help_support"))
#     app_builder.add_handler(CallbackQueryHandler(end, pattern="end"))
#     app_builder.add_handler(STATE_CHOOSING_ITEM, button_callback)
#     app_builder.add_handler(MessageHandler(filters.Text & (~filters.Command), button_callback))
    
#     app_builder.set_default_update_types([])
    
#     app_builder.run_polling()

# if __name__ == "__main__":
#     main()
