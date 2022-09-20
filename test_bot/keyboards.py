from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove,\
    InlineKeyboardMarkup, InlineKeyboardButton

inline_kb = InlineKeyboardMarkup(row_width=2)
reply_kb = ReplyKeyboardMarkup()

# inline_btn_1 = InlineKeyboardButton('Button 1', callback_data='btn_1')
# inline_btn_2 = InlineKeyboardButton('Button 2', callback_data='btn_2')
# inline_btn_3 = InlineKeyboardButton('Button 3', callback_data='btn_3')

# list_btn = [inline_btn_1, inline_btn_2, inline_btn_3]

# for btn in list_btn:
#     inline_kb.insert(btn)

for btn in range(1,6):
    inline_kb.insert(InlineKeyboardButton(f'Кнопка {btn}', callback_data=f'11{btn}'))

#change line