from telegram.ext import (Updater,InlineQueryHandler,
CommandHandler,CallbackContext,CallbackQueryHandler,
ChosenInlineResultHandler)
from telegram.update import Update
from telegram import (Chat,InlineQueryResultArticle,InputTextMessageContent,
InlineKeyboardButton,InlineKeyboardMarkup,User,ParseMode)
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




def type_secret_pm(update:Update , context:CallbackContext)->None:
    #^(.+)\s\@
    
    query = update.inline_query.query

    if query == "":
        return

    mention = get_mention(update)

    res = re.findall(r'^(.+)\s\@(.*)',string = query,flags=re.S)
    #print(res)

    if(len(res) and len(res[0][0])<=200): #===> kamel
        secret_message,user_name = res[0]
        inline_keyboard = [
            [InlineKeyboardButton(text = 'نمایش متن پیام🔏',callback_data=f'read')]
        ]
        inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard)
        results = [
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = f'متن پیام شما : {secret_message}',
                input_message_content=InputTextMessageContent(f'یک پیام از {mention} داری',parse_mode=ParseMode.MARKDOWN_V2),
                description  = f'پیام شما به آیدی {user_name}@ ارسال خواهد شد!⚠️',
                reply_markup = inline_keyboard_markup,
                )
        ]
        update.inline_query.answer(results)
        #print(id)
    elif(len(query) <= 200):
        print('faght matn ok')
    else:
        print('matn ziad')





def recive_secret_pm(update:Update , context : CallbackContext)->None:
    # query = update.callback_query
    # #secret_message = query.data
    # #print(update)
    # print(query)
    print(update)


def send_secret_pm(update:Update , context:CallbackContext):
    print(update)
    
    












def main()->None:
    
    dispatcher = updater.dispatcher

    type_secret_pm_handler = InlineQueryHandler(type_secret_pm ,chat_types=[Chat.SUPERGROUP]) #bara darje pm
    send_secret_pm_handler = ChosenInlineResultHandler(send_secret_pm)
    recive_secret_pm_handler = CallbackQueryHandler(recive_secret_pm)
    
    dispatcher.add_handler(send_secret_pm_handler)
    dispatcher.add_handler(type_secret_pm_handler)
    
    dispatcher.add_handler(recive_secret_pm_handler)
    



    updater.start_polling()
    


if(__name__ == '__main__'):
    main()