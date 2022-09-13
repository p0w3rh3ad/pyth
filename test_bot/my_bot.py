from asyncore import dispatcher
import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN
import random

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def pMyProc(msg):
    word_count = len(msg.split(' '))
    char_count = len(''.join(msg.split(' ')))
    word_len = round(char_count/word_count,2)    
    return f'Во введенном тексте:\nслов - {word_count}\nсимволов - {char_count}\nсредняя длина слова - {word_len}'

@dp.message_handler(commands=['start'])
async def pWelcome(message: types.Message):
    # await message.reply('Привет!')
    await message.answer(list({
        'Привет!',
        'Доброго времени суток :-)',
        'И вам не хворать!',
        'Здрав будь, боярин...'})[0])
    await message.answer(list({
        'Пеши исчо',
        'Отправьте мне какой-нибудь текст',
        'Мне нравятся ФЫВА и ОЛДЖ...',
        'Поговорим?'})[0])

@dp.message_handler()
async def echo(message: types.Message):    
    await message.answer(pMyProc(message.text))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)