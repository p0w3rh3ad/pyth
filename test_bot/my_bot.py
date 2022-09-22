from asyncore import dispatcher
import logging
# from time import sleep
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import keyboards as kb
import random
import apscheduler

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

preamble = [
    'Привет!',
    'Доброго времени суток :-)',
    'И вам не хворать!',
    'Здрав будь, боярин...'
]
epilogue = [
    'Пеши исчо',
    'Отправьте мне какой-нибудь текст',
    'Мне нравятся ФЫВА и ОЛДЖ...',
    'Поговорим?'
]

def analize(msg):
    word_count = len(msg.split(' '))
    char_count = len(''.join(msg.split(' ')))
    word_len = round(char_count/word_count,2)    
    return f'Во введенном тексте:\n'\
        f'слов - {word_count}\n'\
        f'символов - {char_count}\n'\
        f'средняя длина слова - {word_len}'

@dp.callback_query_handler()
async def process_callback_kb(callback_query: types.CallbackQuery):
    code = callback_query.data

    # позволяет не зависать чату, во время "поиска ответа" ботом
    # например, пока выполняется 10-секундный слип, пользователь
    # может отправить текст боту и получить ответ от функции analize
    # 
    await bot.answer_callback_query(callback_query.id)
    
    #sleep(10)
    await bot.send_message(callback_query.from_user.id,\
        f'Нажата кнопка {code}')

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # await message.reply('Привет!')
    random.shuffle(preamble)
    random.shuffle(epilogue)
    await message.answer(f'{preamble[0]}\n{epilogue[0]}')
    await message.answer('Тест кнопок', reply_markup=kb.inline_kb)    

@dp.message_handler(content_types=types.ContentType.ANY)
async def answ(message: types.Message):
    if message.content_type == 'text':
        await message.answer(analize(message.text))
    else:
        random.shuffle(epilogue)
        await message.reply(f'Люблю, когда со мной разговаривают ;-)\n'\
            f'{epilogue[0]}')
        
# # @dp.message_handler(content_types=['sticker', 'audio',\
# #    'photo', 'document'])
# @dp.message_handler(content_types=types.ContentType.ANY)
# async def answ_stick(message: types.Message):
#     random.shuffle(epilogue)
#     await message.reply(f'Люблю, когда со мной разговаривают ;-)\n'\
#         f'{epilogue[0]}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)