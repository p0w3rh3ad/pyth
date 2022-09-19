from asyncore import dispatcher
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import keyboards as kb
import random

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
    await bot.answer_callback_query(callback_query.id,\
        f'Нажата кнопка {code}')
    # await bot.send_message(callback_query.from_user.id,\
    #     f'Нажата кнопка {code}')

@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    # await message.reply('Привет!')
    random.shuffle(preamble)
    random.shuffle(epilogue)
    await message.answer(f'{preamble[0]}\n{epilogue[0]}')
    await message.answer('Тест кнопок', reply_markup=kb.inline_kb)

@dp.message_handler()
async def echo(message: types.Message):    
    await message.answer(analize(message.text))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)