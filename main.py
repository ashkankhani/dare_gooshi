from telegram.ext import Updater,InlineQueryHandler,CommandHandler,CallbackContext,CallbackQueryHandler
from telegram.update import Update
from telegram import Chat,InlineQueryResultArticle,InputTextMessageContent,InlineKeyboardButton,InlineKeyboardMarkup,User,ParseMode
from uuid import uuid4
import re




BOT_TOKEN = '2038024519:AAFqwDWL0d8IMEoMVsSl_3pew43o-bC0t8w'

updater = Updater(BOT_TOKEN)



def get_mention(update : Update)-> None:
    first_name = update.inline_query.from_user.first_name
    last_name = update.inline_query.from_user.last_name
    id = update.inline_query.from_user.id
    user = User(id = id , first_name=first_name,is_bot=False)
    if(not last_name):
        last_name = ''
    
    name = first_name + ' ' + last_name

    mention = user.mention_markdown_v2(name=name)

    return mention




def send_secret_pm(update:Update , context:CallbackContext)->None:
    #^(.+)\s\@
    
    query = update.inline_query.query

    
    if query == "":
        return

    mention = get_mention(update)

    secret_message = re.findall(r'^(.+)\s\@',string = query,flags=re.S)

    inline_keyboard = [
        [InlineKeyboardButton(text = 'نمایش متن پیام🔏',callback_data=secret_message)]
    ]
    inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard)

    results = [
        InlineQueryResultArticle(
            id = str(uuid4()),
            title = f'متن پیام شما : {secret_message}',
            input_message_content=InputTextMessageContent(f'یک پیام از {mention} داری',parse_mode=ParseMode.MARKDOWN_V2),
            description  = '...\n999',
            reply_markup = inline_keyboard_markup,
            url = 'https://google.com',
            hide_url = True
            )
    ]
    update.inline_query.answer(results)





def recive_secret_pm(update:Update , context : CallbackContext)->None:
    query = update.callback_query
    secret_message = query.data
    print(update)
    print(query)
    
    












def main()->None:
    
    dispatcher = updater.dispatcher

    send_secret_pm_handler = InlineQueryHandler(send_secret_pm , pass_chat_data  = True,chat_types=[Chat.SUPERGROUP]) #bara darje pm
    recive_secret_pm_handler = CallbackQueryHandler(recive_secret_pm)
    

    dispatcher.add_handler(send_secret_pm_handler)
    dispatcher.add_handler(recive_secret_pm_handler)


    updater.start_polling()
    


if(__name__ == '__main__'):
    main()