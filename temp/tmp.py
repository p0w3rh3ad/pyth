import random

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

for i in range(0,10):
    random.shuffle(preamble)
    random.shuffle(epilogue)
    print(preamble[0],epilogue[0])