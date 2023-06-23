async def cancel_activation(update: Update, context: CallbackContext):
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
            return STATE_CHOOSING_ITEM
        elif response.text == "STATUS_CANCEL":
            await context.bot.send_message(chat_id=query.message.chat_id, text="The activation was cancelled.", reply_markup=reply_markup)
    else:    
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status={query.data}")

        if response.status_code == 200 and "ACCESS_CANCEL" in response.text:
            await cancel_flag.set()
            await context.bot.send_message(chat_id=query.message.chat_id, text="\U0001F534 Activation Cancelled\n\nPress \U0001F3E1 Home to go to the main menu\n         ⬅️ Back to go back to services", reply_markup=reply_markup)   
        else:
            await context.bot.send_message(chat_id=query.message.chat_id, text="Sending SMS", reply_markup=reply_markup)            
            await cancel_flag.clear()
           
        save_cancel_flag(chat_id, cancel_flag)
           
        await check_otp_code_availability(context, query.message.chat_id, api_key, id, cancel_flag)
    return STATE_CONFIRMATION
