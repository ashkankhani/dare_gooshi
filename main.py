from telegram.ext import (Updater,InlineQueryHandler,
CommandHandler,CallbackContext,CallbackQueryHandler,
ChosenInlineResultHandler)
from telegram.update import Update
from telegram import (Chat,InlineQueryResultArticle,InputTextMessageContent,
InlineKeyboardButton,InlineKeyboardMarkup,
User,ParseMode, user)
from uuid import uuid4
import re
from sqlite3 import connect,IntegrityError






with connect('database.db') as connection: #===> make database
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE "messages" (
	"id"	INTEGER,
	"message"	TEXT NOT NULL,
	"reciver"	TEXT NOT NULL,
	"user_id"	INTEGER NOT NULL,
	"inline_id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
''')
    cursor.execute('''CREATE TABLE if not exists "users" (
	"id"	INTEGER,
	"user_id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
)
''')
    connection.commit()










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

    res = re.findall(r'^(.+)\s\@(.*)',string = query,flags=re.S) #motabeghe matn kamel
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
                title = f'متن پیامتون: {secret_message}',
                input_message_content=InputTextMessageContent(f'یک پیام از {mention} داری',parse_mode=ParseMode.MARKDOWN_V2),
                description  = f'پیامتو برای ({user_name}@) میفرستم✅\n{len(secret_message)}/200',
                reply_markup = inline_keyboard_markup,
                )
        ]

        #print(id)
    elif(len(query) <= 200):
        results = [
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = f'متن پیامتون: {query}',
                input_message_content=InputTextMessageContent(f'ای بابا آیدی طرفو نزدی که😶',),
                description  = f'⚠️یادت نره که آیدی گیرنده رو بنویسی\n{len(query)}/200',
                )
        ]
    else:
        results = [
            InlineQueryResultArticle(
                id = str(uuid4()),
                title = 'خطا!',
                description = 'متنتون خیلی بلنده چطوره یکم کوتاه کنین؟',
                input_message_content=InputTextMessageContent('اوه اوه متنت خیلی بلند بود که😞'),

            )
        ]

    update.inline_query.answer(results)





def recive_secret_pm(update:Update , context : CallbackContext)->None:
    query = update.callback_query
    inline_id = query.inline_message_id
    user_name = query.from_user.username
    user_id = query.from_user.id
    print(inline_id)
    res = get_message_text(inline_id,user_name,user_id)
    if(res):
        query.answer(f'متن پیام✍️:\n{res[0]}',show_alert=True)
    else:
        query.answer('ای فضول دیدی مچتو گرفتم؟😉')

    



def message_saver(message,reciver,user_id,inline_id):
    with connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'''insert into messages
        (message,reciver,user_id,inline_id)
        values(
            '{message}','{reciver}',{user_id},'{inline_id}'
        )
        ''')
        connection.commit()


def get_message_text(inline_id,user_name,user_id):
    with connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'''select message
        from messages
        where inline_id = '{inline_id}' and (reciver = '{user_name}' or user_id = {user_id})
        ''')
        res = cursor.fetchone()

    return res



def send_secret_pm(update:Update , context:CallbackContext):
    inline = update.chosen_inline_result
    inline_id = inline.inline_message_id
    if(inline_id):
        print(inline.query)
        message , reciver = re.findall(r'^(.+)\s\@(.*)',string = inline.query,flags=re.S)[0]
        user_id = inline.from_user.id
        try:
            message_saver(message,reciver,user_id,inline_id)
        except IntegrityError:
            pass




    #print(update)
    
    












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