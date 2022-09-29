from asyncore import dispatcher
import logging
from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import keyboards as kb
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

# глобальный словарь сессии
GLOBAL_DICT = {'user_id':{'key':'value'}}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

preamble = ['Привет!',
    'Доброго времени суток :-)',
    'И вам не хворать!',
    'Здрав будь, боярин...']
epilogue = ['Пеши исчо',
    'Отправьте мне какой-нибудь текст',
    'Мне нравятся ФЫВА и ОЛДЖ...',
    'Поговорим?']

def analize(msg):
    word_count = len(msg.split(' '))
    char_count = len(''.join(msg.split(' ')))
    word_len = round(char_count/word_count,2)    
    return f'Во введенном тексте:\n'\
        f'слов - {word_count}\n'\
        f'символов - {char_count}\n'\
        f'средняя длина слова - {word_len}'

def user_data_update(id, key, value):
    GLOBAL_DICT.update({str(id):{str(key):str(value)}})

async def send_notif(dp: Dispatcher, user_id):
    await dp.bot.send_message(user_id,'Вы просили маякнуть :-) ')

def sched_job(user_id):
    user_notif = datetime.now() + timedelta(minutes=1)
    user_notif = user_notif.strftime('%Y-%m-%d %H:%M:%S')    
    scheduler.add_job(send_notif, 'date', run_date=user_notif, args=(dp, user_id))
    print(user_notif, scheduler.get_jobs())

@dp.callback_query_handler()
async def process_callback_kb(callback_query: types.CallbackQuery):
    code = callback_query.data

    # позволяет не зависать чату, во время "поиска ответа" ботом
    # например, пока выполняется 10-секундный слип, пользователь
    # может отправить текст боту и получить ответ от функции analize
    # 
    await bot.answer_callback_query(callback_query.id)
    
    #sleep(10)
    if code == 'analize_text':
        await bot.send_message(callback_query.from_user.id,\
            f'Храню в словаре текст: '\
            f'{GLOBAL_DICT[str(callback_query.from_user.id)][code]}')
    elif code == 'scheduler':       
        sched_job(callback_query.from_user.id)
        await bot.send_message(callback_query.from_user.id,\
            f'Внимание! Заказан маячок через 1 минуту')
    else:
        await bot.send_message(callback_query.from_user.id,\
            f'Нажата кнопка {code}')

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # await message.reply('Привет!')
    random.shuffle(preamble)
    random.shuffle(epilogue)
    await message.answer(f'{preamble[0]}\n{epilogue[0]}')
    await message.answer('Тест кнопок', reply_markup=kb.inline_kb)    

@dp.message_handler(commands=['keyb'])
async def keyb(message: types.Message):
    await message.answer('Мои кнопки',reply_markup=kb.inline_kb)

@dp.message_handler(content_types=types.ContentType.ANY)
async def answ(message: types.Message):
    if message.content_type == 'text':
        key = 'analize_text'
        user_data_update(message.from_user.id, key, message.text)
        await message.answer(analize(message.text))        
    else:
        random.shuffle(epilogue)
        await message.reply(f'Люблю, когда со мной разговаривают ;-)\n'\
            f'{epilogue[0]}')

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)