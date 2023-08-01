
import os
from flask import Flask, request, Response
from telegram import Bot, Update
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    MessageHandler,
    filters,
    ApplicationBuilder, Updater
)
import requests
import asyncio
import os
from dotenv import load_dotenv
from databse import save_api_key, get_api_key, save_main_id, get_main_id, get_cancel_flag, save_cancel_flag

load_dotenv()

TOKEN = os.getenv('TOKEN')
WEBAPP_HOST= os.getenv('URL')

app = Flask(__name__)


STATE_CHOOSING_OPTION, API_KEY_CHOOSE, STATE_CHOOSING_ITEM, STATE_CONFIRMATION, STATE_END = range(5)

main_menu_keyboard = [[InlineKeyboardButton("\U0001F4F2 Get Number", callback_data='get_number'),
                 InlineKeyboardButton("\U0001F4B0 Check Balance", callback_data='check_balance')],
                [InlineKeyboardButton("\U0001F503 Add Balance", callback_data='add_balance'),
                InlineKeyboardButton("\U0001F503 Support Channel", callback_data='support_channel')],
                [InlineKeyboardButton("\U0001F503 Help and Support", callback_data='help_support')]
                ]

async def check_otp_code_availability(context: CallbackContext, chat_id: int, api_key: str, id: str, cancel_flag: asyncio.Event) -> None:
    while not cancel_flag.is_set():
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")
    
        if response.status_code == 200 and "STATUS_OK" in response.text:
            respond = response.text.split(':')[1]
            ret_buttons = [[InlineKeyboardButton("\U0001F4F2 Request New SMS", callback_data='3')],
                 [InlineKeyboardButton("\U0001F4B0 Back to Service List", callback_data='back')],
                ]
    
            reply_markup = InlineKeyboardMarkup(ret_buttons)
            texte= f"""Your requested otp for the number is 

            \U0001F4F6 OTP: {respond}

            📌_To get another otp for the same number\\! Click on Request New Sms_"""
            
            await context.bot.send_message(chat_id=chat_id, text=texte, reply_markup=reply_markup,parse_mode="MarkdownV2")
            break 
        elif response.status_code == 200 and "STATUS_CANCEL" in response.text:
            break
        await asyncio.sleep(2)
    if cancel_flag.is_set():
        del context.user_data['cancel_flag']

async def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    first_name = update.effective_user.first_name
    api_buttons = [[InlineKeyboardButton("\U0001F4F2 Get API KEY", callback_data='get_api')],
                 [InlineKeyboardButton("\U0001F4B0 Generate Access Key", callback_data='get_access')],
                ]
    
    reply_markup = InlineKeyboardMarkup(api_buttons)
    await context.bot.send_message(chat_id=chat_id, text=f"\U0001F510 Hello {first_name}, Please enter your API key.", reply_markup=reply_markup)
    return STATE_CHOOSING_OPTION
async def generate_access_key(update: Update, context: CallbackContext) -> None:
    callback_query = update.callback_query
    chat_id_effective = update.effective_chat.id
    if callback_query is None:
        api_key = update.message.text.strip()

        save_api_key(chat_id_effective, api_key)
        url = f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getBalance"
        response = requests.get(url)
        if response.status_code == 200 and "ACCESS_BALANCE" in response.text:
            message = "Welcome to the main menu. Please select a service:"
            reply_markup = InlineKeyboardMarkup(main_menu_keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, reply_markup=reply_markup)
            return API_KEY_CHOOSE
        else:
            message = "Invalid API key\n\U0001F517 Please create an access key and generate api key from otpindia.com"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, disable_web_page_preview=True)
            return STATE_CHOOSING_OPTION
        
    chat_id = callback_query.message.chat_id
    query_data = callback_query.data
    if query_data == 'get_api':
        await context.bot.send_message(chat_id=chat_id, text="*Dear user*,\n If you don’t have the api key\\! Then you can simply generate it by your access key\n\n*Step1*: Go to otpindia\\.com\n*Step2*: Login with your access key\n*Step3*: Click on the profile icon on the right top\n*Step4*: Click on Generate api key option to generate\n*Step5*: Copy the api key and paste it on the bot to use\n\n*To get tutorial with images\\! Visit*:\nhttps://telegra\\.ph/how\\-to\\-get\\-api\\-key\\-05\\-31\n\nIf you don’t have access key\\! Then click on “💰_Generate Access key_” option to get the link", parse_mode="MarkdownV2",disable_web_page_preview=True)
        return STATE_CHOOSING_OPTION    
    elif query_data == 'get_access':
        await context.bot.send_message(chat_id=chat_id, text="*Dear user*,\n If you don’t have access key\\! Then you can use this link to generate a new access key for you\n\n[Generate Access Key](https://otpindia.com/?c=get_access&acc=1)\n\n*Step 1*: Go to this link\n*Step 2*: Solve the Google Captcha\n*Step 3*: Click on the Generate Access key button to create an access key", parse_mode="MarkdownV2", disable_web_page_preview=True)
    return STATE_CHOOSING_OPTION

async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == 'get_number':
        chat_id = update.effective_chat.id
        api_key = get_api_key(chat_id)
        row = []
        response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
        services = response.json()
        response_prices = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getPrices&country=22')
        prices = response_prices.json()
        service_id_to_name = {key: value for key, value in services.items()}
        service_prices = []

        for service_id, prices_data in prices['22'].items():
            service_name = service_id_to_name[service_id]
            for price, _ in prices_data.items():
                service_price = {'service': service_name, 'price': price, 'service_ID':service_id}
                service_prices.append(service_price)
        buttons = []
        for index, service in enumerate(service_prices):            
            serviceme= service['service']+'  '+service['price']+'₹'
            
            if index==0 or index==1:
                row.append(InlineKeyboardButton(serviceme, callback_data=service['service_ID']))                
            else:
                if len(row) == 2:
                    buttons.append(row)
                    row = []
                row.append(InlineKeyboardButton(serviceme, callback_data=service['service_ID']))
        if len(row) == 2:
            buttons.append(row)
        else:
            buttons.append(row + [InlineKeyboardButton("", callback_data="None")] * (3 - len(row)))
        reply_markup = InlineKeyboardMarkup(buttons)
        await context.bot.send_message(chat_id=chat_id, text="Choose a service:", reply_markup=reply_markup)
        return STATE_CHOOSING_ITEM   

    elif query.data == "check_balance":
        chat_id = update.effective_chat.id
        api_key = get_api_key(chat_id)
       
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getBalance")
        balance_str = response.text.split(":")[1]
        message = f'₹{float(balance_str):.2f}'
        await context.bot.send_message(chat_id=chat_id, text=message)

    elif query.data == "add_balance":
        chat_id = update.callback_query.message.chat_id
        api_buttons = [[InlineKeyboardButton("\U0001F4F2 Add Balance", callback_data='add1_balance'),
                    InlineKeyboardButton("\U0001F4B0 How to Add Balance", callback_data='to_add')],
                    ]
        reply_markup = InlineKeyboardMarkup(api_buttons)
        await context.bot.send_message(chat_id=chat_id, text="Add Balance", reply_markup=reply_markup)
        return STATE_CHOOSING_ITEM
    
    elif query.data == "support_channel":
        chat_id = update.callback_query.message.chat_id
        await context.bot.send_message(chat_id=chat_id, text="*Dear user*,\n\nTo get all the *notifications*, *offers* and *updates* about otpindia please join our official Telegram channel\n\n*Channel Link*: @otpindiaofficial\n\n\n_This is our only one official channel, please check the official username before joining any channel_", parse_mode="MarkdownV2")

    elif query.data == "help_support":
        chat_id = update.callback_query.message.chat_id
        await context.bot.send_message(chat_id=chat_id, text="*Dear user*,\n\nIf you face any issues regarding otpindia\\! You can simply contact us on our official support at @tempotpowner\n\n*Username*: @Tempotpowner\n\n__Please remember__:\n_Our office time is 11:00am to 7:00pm \\( Monday\\- Saturday \\)\n\nYou will get replies on the office hours only_", parse_mode="MarkdownV2")

async def service_callback(update: Update, context: CallbackContext) -> None:   
    query = update.callback_query
   
    chat_id = update.effective_chat.id
    api_key = get_api_key(chat_id)

    response1 = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
    services = response1.json()
    service_id_to_name = {key: value for key, value in services.items()}

    service = query.data
    service_name = service_id_to_name.get(service) 
    response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getNumber&service={service}&country=22')
    responded = response.text
    if responded == "NO_BALANCE":
        await context.bot.send_message(chat_id=query.message.chat_id, text="Your balance is low, please add money.")
    elif query.data == 'add1_balance':
        await context.bot.send_message(chat_id=query.message.chat_id, text="*Dear user*,\n Currently you can\'t add balance directly in the bot\\. You need to login to otpindia\\.com with your access key to add balance and then you can use that balance on this bot\\.\n\n*For tutorial*: _Click on “💰How to Add Balance”_ Option", parse_mode="MarkdownV2")
        return API_KEY_CHOOSE
    elif query.data == 'to_add':
        await context.bot.send_message(chat_id=query.message.chat_id, text="*Dear user*,\n You need to login to otpindia\\.com with your access key to add balance\\.\n\n*Step1*: go to otpindia\\.com\n*Step2*: Login with your Access Key\n*Step3*: Click on Add Balance Option\n*Step4*: Choose any payment method which is suitable for you and add balance\n\n_The balance will also visible on your access key and bot_\n\n*For extended tutorial, Please visit*:\nhttps://telegra\\.ph/how\\-to\\-add\\-balance\\-05\\-31", parse_mode="MarkdownV2", disable_web_page_preview=True)
        return API_KEY_CHOOSE
    elif "NO_NUMBERS" in responded:
        await context.bot.send_message(chat_id=query.message.chat_id, text="There are no numbers with the specified parameters, try again later, or change the country.")

    elif "ACCESS_NUMBER" in responded:        
        access_number = responded.split(":")[2]
        main_id = responded.split(':')[1]
        save_main_id(chat_id, main_id)
       
        sms_keyboard = [[InlineKeyboardButton("❌ Cancel Activation", callback_data='8')],
                [InlineKeyboardButton("✅ Check OTP Code", callback_data="otp_code")]
                ]   
        message = f"You have successfully Ordered a Number for {service_name}"
        reply_markup = InlineKeyboardMarkup(sms_keyboard)
        await context.bot.send_message(chat_id=query.message.chat_id, text=f"{message}\n\nNumber: \U0001F4F1 {access_number}\nID:{main_id}\n\n\n*📌Note*: Sms will appear automatically when received\n\n__Cancel Activation__: To cancel the order\n__Request New SMS__: To get another otp for the same number *FREE*\n__Check OTP Code__: Show the last received otp", reply_markup=reply_markup, parse_mode="MarkdownV2")
        cancel_flag = asyncio.Event()
        save_cancel_flag(chat_id, cancel_flag)
        asyncio.create_task(check_otp_code_availability(context, query.message.chat_id, api_key, main_id, cancel_flag))
    
    return STATE_CONFIRMATION  

async def cancel_activation(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = update.effective_chat.id
    api_key = get_api_key(chat_id)
    id = get_main_id(chat_id)
    cancel_flag = get_cancel_flag(chat_id)
    ret_buttons = [[InlineKeyboardButton("\U0001F4F2 Request New SMS", callback_data='3')],
                 [InlineKeyboardButton("\U0001F4B0 Back to Service List", callback_data='back')],
                ]
    
    reply_markup1 = InlineKeyboardMarkup(ret_buttons)
    button_list = [[KeyboardButton("⬅️ Back"), KeyboardButton("\U0001F3E1 Home")]]
    reply_markup = ReplyKeyboardMarkup(button_list, resize_keyboard=True,one_time_keyboard=True)
    
    if query.data == "otp_code":
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={id}")
        if response.text == "STATUS_WAIT_CODE":
            await context.bot.send_message(chat_id = query.message.chat_id, text="Wait for the code", reply_markup=reply_markup)
        elif response.status_code==200 and "STATUS_OK" in response.text:
            respond = response.text.split(':')[1]  
            texte= f"""Your requested otp for the number is 

            \U0001F4F6 OTP: {respond} 

            📌_To get another otp for the same number\\! Click on Request New Sms_"""          
            await context.bot.send_message(chat_id=query.message.chat_id, text=texte, reply_markup=reply_markup1, parse_mode="MarkdownV2")
            return STATE_CHOOSING_ITEM
        elif response.text == "STATUS_CANCEL":
            await context.bot.send_message(chat_id=query.message.chat_id, text="The activation was cancelled.", reply_markup=reply_markup)

    elif query.data == "back":
        await back(update, context)
        return STATE_CHOOSING_ITEM

    elif query.data == "8":
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status=8")

        if response.status_code == 200 and "ACCESS_CANCEL" in response.text:
            cancel_flag.set()
            await context.bot.send_message(chat_id=query.message.chat_id, text="\U0001F534 Activation Cancelled\n\nPress \U0001F3E1 Home to go to main menu\n         ⬅️ Back to go back to services", reply_markup=reply_markup)   
    elif query.data == "3":
        
        response = requests.get(f"https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=setStatus&id={id}&status=3")
        await context.bot.send_message(chat_id=query.message.chat_id, text="Sending SMS", reply_markup=reply_markup)
        cancel_flag = asyncio.Event()
        context.user_data['cancel_flag'] = cancel_flag
        asyncio.create_task(check_otp_code_availability(context, query.message.chat_id, api_key, id, cancel_flag))

        return STATE_CONFIRMATION

async def back(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    api_key = get_api_key(chat_id)
    
    row = []
    response = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getServices')
    services = response.json()
    response_prices = requests.get(f'https://smstore.su/stubs/handler_api.php?api_key={api_key}&action=getPrices&country=22')
    prices = response_prices.json()
    service_id_to_name = {key: value for key, value in services.items()}
    service_prices = []

    for service_id, prices_data in prices['22'].items():
        service_name = service_id_to_name[service_id]
        for price, _ in prices_data.items():
            service_price = {'service': service_name, 'price': price, 'service_ID':service_id}
            service_prices.append(service_price)
    buttons = []
    for index, service in enumerate(service_prices):            
        serviceme= service['service']+'  '+service['price']+'₹'
        
        if index==0 or index==1:
            row.append(InlineKeyboardButton(serviceme, callback_data=service['service_ID']))                
        else:
            if len(row) == 2:
                buttons.append(row)
                row = []
            row.append(InlineKeyboardButton(serviceme, callback_data=service['service_ID']))
    if len(row) == 2:
        buttons.append(row)
    else:
        buttons.append(row + [InlineKeyboardButton("", callback_data="None")] * (3 - len(row)))
    reply_markup = InlineKeyboardMarkup(buttons)
    await context.bot.send_message(chat_id, text="Choose a service:", reply_markup=reply_markup)
    return STATE_CHOOSING_ITEM

async def home(update: Update, context: CallbackContext) -> None:
    button_list = main_menu_keyboard
    reply_markup = InlineKeyboardMarkup(button_list)
    await update.message.reply_text('Welcome! Choose an option:', reply_markup=reply_markup)    
    return API_KEY_CHOOSE

app_telegram = ApplicationBuilder().token(os.getenv('TOKEN')).read_timeout(30).write_timeout(30).build()

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string, app_telegram.bot)
        app_telegram.process_update(update)
        # Start the webhook
    return 'ok'


@app.route('/', methods=['GET'])
def index():
    return Response('Get ok', status=200)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
        states={
            STATE_CHOOSING_OPTION: [MessageHandler(filters.TEXT & (~ filters.COMMAND), generate_access_key),
                                    CallbackQueryHandler(generate_access_key)
                                    ],
            API_KEY_CHOOSE: [CallbackQueryHandler(button_callback)],
            STATE_CHOOSING_ITEM: [CallbackQueryHandler(service_callback)],
            STATE_CONFIRMATION: [CallbackQueryHandler(cancel_activation)],
            STATE_END: [CommandHandler('start', start)],
        },
        fallbacks=[MessageHandler(filters.Regex('^(⬅️ Back)$'), back), MessageHandler(filters.Regex('^(\U0001F3E1 Home)$'), home)],
        allow_reentry=True
)
app_telegram.add_handler(conv_handler)

webhook_url = f'{WEBAPP_HOST}/webhook'

app_telegram.run_webhook(listen='0.0.0.0', url_path='/webhook', webhook_url=webhook_url)

if __name__ == '__main__':
    app.run()