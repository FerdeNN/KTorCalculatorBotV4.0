import telebot
from telebot import types
import random as rand
import shelve

bot = telebot.TeleBot('5053457649:AAETjdBGf-2GVS5PKapH3137sOAX0xEPitY')

res = None

menu = telebot.types.ReplyKeyboardMarkup()
menu.row('Калькулятор',
         'Тест'
         )

menu.row('Об авторе',
         'Выход'
         )

test = telebot.types.ReplyKeyboardMarkup()
test.row('Начать',
         'Инструкция')
test.row('Назад')

author = telebot.types.ReplyKeyboardMarkup()
author.row('Вернуться')

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('1',
                                                callback_data='1'),
             telebot.types.InlineKeyboardButton('2',
                                                callback_data='2'),
             telebot.types.InlineKeyboardButton('3',
                                                callback_data='3'),
             telebot.types.InlineKeyboardButton('4',
                                                callback_data='4'),
             telebot.types.InlineKeyboardButton('5',
                                                callback_data='5')
             )

keyboard.row(telebot.types.InlineKeyboardButton('6',
                                                callback_data='6'),
             telebot.types.InlineKeyboardButton('7',
                                                callback_data='7'),
             telebot.types.InlineKeyboardButton('8',
                                                callback_data='8'),
             telebot.types.InlineKeyboardButton('9',
                                                callback_data='9'),
             telebot.types.InlineKeyboardButton('0',
                                                callback_data='0')
             )

keyboard.row(telebot.types.InlineKeyboardButton('+',
                                                callback_data='+'),
             telebot.types.InlineKeyboardButton('-',
                                                callback_data='-'),
             telebot.types.InlineKeyboardButton('*',
                                                callback_data='*'),
             telebot.types.InlineKeyboardButton('/',
                                                callback_data='/')
             )

keyboard.row(telebot.types.InlineKeyboardButton(',',
                                                callback_data=','),
             telebot.types.InlineKeyboardButton('<=',
                                                callback_data='<='),
             telebot.types.InlineKeyboardButton('C',
                                                callback_data='C'),
             telebot.types.InlineKeyboardButton('=',
                                                callback_data='=')
             )

testmode = telebot.types.ReplyKeyboardMarkup()
testmode.row('Сложение')
testmode.row('Вычитание')
testmode.row('Умножение')

summmode = telebot.types.ReplyKeyboardMarkup()
summmode.row('Сложение однозначных чисел')
summmode.row('Сложение двузначных чисел')

subtrmode = telebot.types.ReplyKeyboardMarkup()
subtrmode.row('Вычитание однозначных чисел')
subtrmode.row('Вычитание двузначных чисел')

multmode = telebot.types.ReplyKeyboardMarkup()
multmode.row('Умножение однозначных чисел')
multmode.row('Умножение двузначных чисел')

stoptest = telebot.types.ReplyKeyboardMarkup()
stoptest.row('Завершить')


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id,
                     'Добро пожаловать!',
                     reply_markup=menu)


@bot.message_handler(regexp='Калькулятор')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выберите первое число:',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    h = shelve.open('values')
    flag1 = 'value' in h
    flag2 = 'old_value' in h
    if not flag1:
        h['value'] = ''
    if not flag2:
        h['old_value'] = ''
    data = query.data

    if data == 'no':
        pass

    elif data == 'C':
        h['value'] = ''

    elif data == '<=':
        if h['value'] != '':
            value = h['value']
            h['value'] = value[:len(value) - 1]

    elif data == '=':
        try:
            value = h['value']
            h['value'] = str(eval(value))
        except:
            h['value'] = 'Ошибка!'

    else:
        value = h['value']
        h['value'] = value + data

    if (h['value'] != h['old_value'] and h['value'] != '') or ('0' != h['old_value'] and h['value'] == ''):
        if h['value'] == '':
            bot.edit_message_text(chat_id=query.message.chat.id,
                                  message_id=query.message.message_id,
                                  text='0',
                                  reply_markup=keyboard)
            h['old_value'] = '0'

        else:
            bot.edit_message_text(chat_id=query.message.chat.id,
                                  message_id=query.message.message_id,
                                  text=h['value'],
                                  reply_markup=keyboard)

            h['old_value'] = h['value']

    if h['value'] == 'Ошибка!': h['value'] = ''
    h.close()


@bot.message_handler(regexp='Назад')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выход в меню...',
                     reply_markup=menu)


@bot.message_handler(regexp='Об авторе')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Автор:\n'
                     'Торосян Кирилл Александрович\n'
                     'ББСО-02-19\n'
                     '\n'
                     'О продукте:\n'
                     'Данный бот "KTorCalculatorProMax"\n'
                     'был создан специально для\n'
                     'изучения языка программирования\n'
                     'Python во время обучения\n'
                     'в РТУ МИРЭА.')


@bot.message_handler(regexp='Выход')
def getMessage(message):
    bot.send_message(message.chat.id,
                     "Выход...",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(regexp='Тест')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Тест запущен!',
                     reply_markup=test)


@bot.message_handler(regexp='Начать')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выберите режим:',
                     reply_markup=testmode)


@bot.message_handler(regexp='Инструкция')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Тест на устный счет.\n'
                     'Вам нужно будет выбрать режим:\n'
                     'сложение, вычитание\n'
                     'или умножение.\n'
                     'Затем вы сможете выбрать режим\n'
                     'однозначных или двузначных чисел.\n'
                     'Будет вестись подсчет правильно\n'
                     'решенных подряд примеров.\n'
                     'В случае ошибки тест будет\n'
                     'остановлен и вы узнаете свой\n'
                     'окончательный результат.\n'
                     'Вы можете закончить тест в\n'
                     'любой момент, нажав кнопку\n'
                     '"Завершить"\n'
                     'Удачи!')


@bot.message_handler(regexp='^Сложение$')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выберите режим для теста на сложение чисел:',
                     reply_markup=summmode)
    file1 = open('score.txt', 'w')
    file1.write('0')
    file1.close()


@bot.message_handler(regexp='^Вычитание$')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выберите режим для теста на вычитание чисел:',
                     reply_markup=subtrmode)
    file1 = open('score.txt', 'w')
    file1.write('0')
    file1.close()


@bot.message_handler(regexp='^Умножение$')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Выберите режим для теста на умножение чисел:',
                     reply_markup=multmode)
    file1 = open('score.txt', 'w')
    file1.write('0')
    file1.close()


@bot.message_handler(regexp='Завершить')
def getMessage(message):
    bot.send_message(message.chat.id,
                     'Тест завершен!\n'
                     'Ваш результат:')
    file1 = open('score.txt')
    for o in file1.readlines():
        bot.send_message(message.chat.id,
                         o,
                         reply_markup=test)
    file1.close()


@bot.message_handler(regexp='^Сложение однозначных чисел$')
def summ1(message):
    a = rand.randrange(1, 10, 1)
    b = rand.randrange(1, 10, 1)
    x = '+'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                summ1(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)
                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


@bot.message_handler(regexp='^Сложение двузначных чисел$')
def summ2(message):
    a = rand.randrange(10, 100, 1)
    b = rand.randrange(10, 100, 1)
    x = '+'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                summ2(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)

                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


@bot.message_handler(regexp='^Вычитание однозначных чисел$')
def subtr1(message):
    a = rand.randrange(1, 10, 1)
    b = rand.randrange(1, 10, 1)
    x = '-'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                subtr1(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)

                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


@bot.message_handler(regexp='^Вычитание двузначных чисел$')
def subtr2(message):
    a = rand.randrange(10, 100, 1)
    b = rand.randrange(10, 100, 1)
    x = '-'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                subtr2(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)

                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


@bot.message_handler(regexp='^Умножение однозначных чисел$')
def mult1(message):
    a = rand.randrange(1, 10, 1)
    b = rand.randrange(1, 10, 1)
    x = '*'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                mult1(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)

                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


@bot.message_handler(regexp='^Умножение двузначных чисел$')
def mult2(message):
    a = rand.randrange(10, 100, 1)
    b = rand.randrange(10, 100, 1)
    x = '*'

    pr = str(a) + x + str(b)
    result = str(eval(str(a) + x + str(b)))
    file = open('calc.txt', 'w')
    file.write(result)
    file.close()
    bot.send_message(message.chat.id,
                     pr + ' = ?',
                     reply_markup=stoptest)

    @bot.message_handler(content_types=['text'])
    def checkanswer(msg):
        file = open('calc.txt')
        for result in file.readlines():
            if msg.text == result:
                o = 0
                file1 = open('score.txt')
                for o in file1.readlines():
                    o = str(eval(o + '+' + '1'))
                file1.close()
                file1 = open('score.txt', 'w')
                file1.write(o)
                file1.close()

                bot.send_message(msg.chat.id,
                                 'Правильно! Следующий пример: ')
                mult2(message)
            else:
                bot.send_message(msg.chat.id,
                                 'К сожалению, вы ошиблись.\n'
                                 'Тест окончен. \n'
                                 'Ваш результат: ',
                                 reply_markup=test)

                file1 = open('score.txt')
                for o in file1.readlines():
                    bot.send_message(msg.chat.id,
                                     o)
                file1.close()

                o = 0


bot.polling(none_stop=True)
