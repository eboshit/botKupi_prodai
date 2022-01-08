import telebot
import json
from telebot import types
from Keyboard import main_keyboard, menu, string_keyboard, wallet_keyboard, payment_keyboard, main_admin
from parsing_for_users import Btc, Usdt, Ltc, check
import os
import xml.etree.ElementTree as ET
import pandas as pd
import time
from flask import Flask, request

bot = telebot.TeleBot('5057727711:AAHefpx6lTiOcgPfG0n6z-oXdSu__R81GwE')
#bot.remove_webhook()
time.sleep(1)
bot.set_webhook(url="https://109.234.37.30'")
app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def webhook():

    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    """bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )"""
    return "ok", 200

def save_data(data, file_name="bd.json"):
    with open(file_name, "w+", encoding="UTF-8") as f:
        json.dump(data, f)


def load_data(file_name="bd.json"):
    with open(file_name, "r+", encoding="UTF-8") as f:
        data = json.load(f)
    return data


users_bd = load_data()


def new_user(user_id, message_id):
    global users_bd

    users_bd[user_id] = {
        "balance": 0,
        "flag": 0,
        "current_payment_method": "",
        "current_payment_amount": 0,
        "current_wallet": "",
        "current_element": 0,
        "current_element_in_file": 0,
        "message_id": message_id,
        "url": "",
        "cur_file_names": [],
        'bot_messageId': 0,
        "current_file": '',
        "xml": []

    }


def keyboard_init(user_id):
    global users_bd
    if users_bd[user_id]["flag"] == 3:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        i = users_bd[user_id]["current_element"]
        b = len(users_bd[user_id]["cur_file_names"]) - 1
        k = 0
        while b - i >= 0 and k < 5:
            button = types.InlineKeyboardButton(text=users_bd[user_id]["cur_file_names"][i],
                                                callback_data=users_bd[user_id]["cur_file_names"][i])
            keyboard.add(button)
            i += 1
            k += 1
        if users_bd[user_id]["current_element"] > 4:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data="<"))
        if b - users_bd[user_id]["current_element"] >= 5:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=">"))
        keyboard.add(types.InlineKeyboardButton(text="МЕНЮ", callback_data="menu"))

    if users_bd[user_id]["flag"] == 7:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        b = len(users_bd[user_id]["xml"]) - 1
        if users_bd[user_id]["current_element_in_file"] > 4:
            keyboard.add(types.InlineKeyboardButton(text="<", callback_data="<"))
        if b - users_bd[user_id]["current_element_in_file"] >= 5:
            keyboard.add(types.InlineKeyboardButton(text=">", callback_data=">"))
        keyboard.add(types.InlineKeyboardButton(text="МЕНЮ", callback_data="menu"))

    return keyboard


def changing_flag(user_id, val):
    global users_bd
    users_bd[user_id]['flag'] = val


def save_xml(user_id):
    global users_bd
    excel_data_df = pd.read_excel('STROKI/' + user_id + "/" + users_bd[user_id]["current_file"])
    a = []
    for i in range(len(excel_data_df["Название"].tolist())):
        b = []
        b.append(excel_data_df["Ссылка"].tolist()[i])
        b.append(excel_data_df["Название"].tolist()[i])
        b.append(excel_data_df["Цена"].tolist()[i])
        b.append(excel_data_df["Номер"].tolist()[i])
        a.append(b)
    users_bd[user_id]["xml"] = a


def response(user_id):
    global users_bd
    resp = ''
    i = users_bd[user_id]["current_element_in_file"]
    b = len(users_bd[user_id]["xml"]) - 1
    k = 0
    while b - i >= 0 and k < 5:
        resp += f'{str(i + 1)}. [Написать](wa.me/{users_bd[user_id]["xml"][i][3]})\nНазвание товара: {users_bd[user_id]["xml"][i][1]}\nЦена товара: {users_bd[user_id]["xml"][i][2]}\n[Ссылка на объявление]({users_bd[user_id]["xml"][i][0]})\n'
        i += 1
        k += 1
        if k < 5:
            resp += '❈ ═══════💎═══════ ❈\n'
    return resp


admin = "2098607188"


@bot.message_handler(commands=['admin', 'stats', 'dist', 'add', 'ban', 'unban', 'qiwi', 'usdt', 'btc', 'ltc'])
def message_2(message):
    global users_bd
    users_bd = load_data()
    chat_id = message.chat.id
    user_id = str(message.from_user.id)
    if user_id in users_bd:
        if str(message.from_user.id) == admin and (
                users_bd[user_id]['flag'] == 17 or (users_bd[user_id]['flag'] > 7 and users_bd[user_id]['flag'] < 16)):
            if message.text == '/admin':
                bot.send_message(chat_id=chat_id,
                                 text='/admin – перечисление всех команд модератора с описанием \n/stats – статистика по '
                                      'боту, количество юзеров, общая сумма пополнений \n/dist – рассылка сообщений '
                                      'пользователям, к сообщениям в рассылке прикреплять кнопку – скрыть уведомление. '
                                      '\n/add – добавить баланс пользователю по его ID\n/ban – ограничить использование '
                                      'ботом пользователю по id \n/qiwi , /usdt , /btc , /ltc – вставка кошелька, '
                                      'должны заменять кошелек который пишется при оплате.\n/unban – разбанить '
                                      'пользователя по id ')
            if message.text == '/stats':
                all_deposits = users_bd["cash"]["all_deposits"]
                m = str(all_deposits).split('.')
                if len(m[1]) > 4:
                    all_deposits = str(m[0]) + '.' + str(m[1][:4])
                bot.send_message(chat_id=chat_id,
                                 text=f'Общее количество пользователей: {len(users_bd) - 1}\nОбщая сумма пополнений: {all_deposits}')
            if message.text == '/dist':
                bot.send_message(chat_id=chat_id,
                                 text="Введите сообщение, которое будет отправлено всем пользователям бота")
                users_bd[user_id]["flag"] = 8
            if message.text == '/add':
                bot.send_message(chat_id=chat_id,
                                 text="Введите id пользователя и сумму для пополнения баланса в формате:\n 'id' 'сумма'\n999999 999999")
                users_bd[user_id]["flag"] = 10
            if message.text == '/ban':
                bot.send_message(chat_id=chat_id, text="Введите id пользователя, которого хотите забанить")
                users_bd[user_id]["flag"] = 9
            if message.text == '/unban':
                bot.send_message(chat_id=chat_id, text="Введите id пользователя, которого хотите забанить")
                users_bd[user_id]["flag"] = 11
            if message.text == '/qiwi':
                bot.send_message(chat_id=chat_id, text="Введите qiwi-кошелёк")
                users_bd[user_id]["flag"] = 12
            if message.text == '/usdt':
                bot.send_message(chat_id=chat_id, text="Введите usdt-кошелёк")
                users_bd[user_id]["flag"] = 13
            if message.text == '/btc':
                bot.send_message(chat_id=chat_id, text="Введите btc-кошелёк")
                users_bd[user_id]["flag"] = 14
            if message.text == '/ltc':
                bot.send_message(chat_id=chat_id, text="Введите ltc-кошелёк")
                users_bd[user_id]["flag"] = 15
    save_data(users_bd)


@bot.message_handler(commands=['start'])
def message_1(message):
    global users_bd
    users_bd = load_data()
    chat_id = message.chat.id
    message_id = message.message_id
    user_id = str(message.from_user.id)
    # r = 0

    if str(message.from_user.id) in users_bd:
        if users_bd[user_id]['flag'] != 5 and user_id != admin:
            try:
                bot.delete_message(chat_id=chat_id, message_id=users_bd[user_id]["message_id"])
            except:
                pass
            try:
                bot.delete_message(chat_id=chat_id, message_id=users_bd[user_id]["bot_messageId"])
            except:
                pass
            r = bot.send_message(chat_id=chat_id,
                                 text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(int(users_bd[user_id]['balance'])), reply_markup=main_keyboard)
            users_bd[user_id]['bot_messageId'] = r.id
            users_bd[user_id]["message_id"] = message_id
            users_bd[user_id]['flag'] = 0

        if user_id == admin:
            m_flag = users_bd[user_id]['flag']
            if m_flag <= 7 and m_flag >= 16:
                try:
                    bot.delete_message(chat_id=chat_id, message_id=users_bd[user_id]["message_id"])
                except:
                    pass
                try:
                    bot.delete_message(chat_id=chat_id, message_id=users_bd[user_id]["bot_messageId"])
                except:
                    pass
            users_bd[user_id]['flag'] = 0
            r = bot.send_message(chat_id=chat_id,
                                 text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                     int(users_bd[user_id]['balance'])), reply_markup=main_admin)
            users_bd[user_id]["message_id"] = message_id
            users_bd[user_id]['bot_messageId'] = r.id

    if str(message.from_user.id) not in users_bd:
        new_user(str(message.from_user.id), message_id)
        if user_id == admin:
            r = bot.send_message(chat_id=chat_id,
                                 text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: 0",
                                 reply_markup=main_admin)
            users_bd[user_id]["message_id"] = message_id
            users_bd[user_id]['bot_messageId'] = r.id
        else:
            r = bot.send_message(chat_id=chat_id,
                                 text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: 0",
                                 reply_markup=main_keyboard)
            users_bd[user_id]["message_id"] = message_id
            users_bd[user_id]['bot_messageId'] = r.id

    save_data(users_bd)


@bot.message_handler(content_types=['text'])
def Flags(message):
    global users_bd
    users_bd = load_data()
    user_id = str(message.from_user.id)
    chat_id = message.chat.id
    users_bd[user_id]["message_id"] = message.message_id
    message_id = users_bd[str(message.from_user.id)]['bot_messageId']
    if user_id in users_bd:
        chat_id = message.chat.id
        support = 2098607188
        if message.from_user.id == support:
            if users_bd[str(support)]['flag'] == 16:
                bot.delete_message(chat_id=support, message_id=users_bd[str(support)]['bot_messageId'])
                bot.delete_message(chat_id=support, message_id=message.message_id)
                bot.send_message(users_bd['cash']['user_id'][0],
                                 text=message.text,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))

                del users_bd['cash']['user_id'][0]

        if users_bd[user_id]['flag'] != 5:
            ###### начало ветви парс ######
            ###прием количества строк
            if users_bd[str(message.from_user.id)]['flag'] == 2:
                ### Нужно сохранять количество элементов для парсинга
                try:
                    count = int(message.text)
                    if count * 4 > float(users_bd[str(message.from_user.id)]['balance']):
                        try:

                            bot.delete_message(chat_id=chat_id,
                                               message_id=message.message_id)
                        except:
                            pass
                        bot.edit_message_text(chat_id=chat_id,
                                              message_id=message_id,
                                              text='Стоимость парсинга превышает ваш остаток на балансе. Введите другое число',
                                              reply_markup=string_keyboard)
                    else:
                        ### Вызывается функция парсиг и баланс изменяется в зависимости от результата парсинга
                        try:
                            bot.delete_message(chat_id=chat_id,
                                               message_id=message.message_id)
                        except:
                            pass
                        bot.edit_message_text(chat_id=chat_id,
                                              message_id=message_id,
                                              text='Фирменный стикер + ожидание')
                        # users_bd[str(message.from_user.id)]['balance'] = users_bd[str(message.from_user.id)]['balance'] - count*4
                        changing_flag(str(message.from_user.id), 0)
                except:
                    try:

                        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
                    except:
                        pass
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Введите ЦЕЛОЕ ЧИСЛО желаемого количество строк',
                                          reply_markup=string_keyboard)
            ###прием ссылки

            if users_bd[str(message.from_user.id)]['flag'] == 1:
                url = message.text
                if 'https://msk.kupiprodai.ru/' not in url or not (check(url)):
                    bot.delete_message(chat_id=chat_id,
                                       message_id=message.message_id)

                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Ссылка указана неверно или же такой ссылки не сушествует. Введите ссылку',
                                          reply_markup=menu)
                if ('https://msk.kupiprodai.ru/' in url) and check(url):
                    users_bd[str(message.from_user.id)]['url'] = url
                    changing_flag(str(message.from_user.id), 2)

                    try:

                        bot.delete_message(chat_id=chat_id,
                                           message_id=message.message_id)
                    except:
                        pass
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Введите желаемое количество строк',
                                          reply_markup=string_keyboard)

            ###### конец ветви парсинга ######
            ###### начало ветви баланс ######
            print(users_bd[str(message.from_user.id)]['flag'])
            if users_bd[str(message.from_user.id)]['flag'] == 6:
                try:
                    bot.delete_message(chat_id=chat_id,
                                       message_id=message.id)
                    if users_bd[str(message.from_user.id)]['current_payment_method'] == 'qiwi':
                        amount = float(message.text)
                        if amount < 500:
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text='Минимальная сумма пополнения 500 рублей',
                                                  reply_markup=menu)
                        else:
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Переведите {amount} на {users_bd[str(message.from_user.id)]["current_wallet"]}\nКак переведёте нажмите кнопку "Оплатил"',
                                                  reply_markup=payment_keyboard)
                            users_bd[str(message.from_user.id)]['current_payment_amount'] = amount
                            users_bd[str(message.from_user.id)]['flag'] = 0
                    if users_bd[str(message.from_user.id)]['current_payment_method'] == 'btc':
                        amount = float(message.text)
                        if amount < 500:
                            print(335)
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Минимальная сумма пополнения 500 рублей',
                                                  reply_markup=menu)

                        else:
                            print(341)
                            btc = Btc()
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Переведите {round(amount / btc, 5)} BTC на {users_bd[str(message.from_user.id)]["current_wallet"]}',
                                                  reply_markup=payment_keyboard)
                            users_bd[str(message.from_user.id)]['current_payment_amount'] = amount
                            users_bd[str(message.from_user.id)]['flag'] = 0
                    if users_bd[str(message.from_user.id)]['current_payment_method'] == 'ltc':
                        amount = float(message.text)
                        if amount < 500:
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Минимальная сумма пополнения 500 рублей',
                                                  reply_markup=menu)
                        else:
                            ltc = Ltc()
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Переведите {round(amount / ltc, 5)} LTC на {users_bd[str(message.from_user.id)]["current_wallet"]}',
                                                  reply_markup=payment_keyboard)
                            users_bd[str(message.from_user.id)]['current_payment_amount'] = amount
                            users_bd[str(message.from_user.id)]['flag'] = 0

                    if users_bd[str(message.from_user.id)]['current_payment_method'] == 'usdt':
                        amount = float(message.text)
                        usdt = Usdt()
                        if amount < 500:
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Минимальная сумма пополнения 500 рублей',
                                                  reply_markup=menu)
                        else:
                            bot.edit_message_text(chat_id=chat_id,
                                                  message_id=message_id,
                                                  text=f'Переведите {round(amount / usdt, 5)} USDT на {users_bd[str(message.from_user.id)]["current_wallet"]}',
                                                  reply_markup=payment_keyboard)
                            users_bd[str(message.from_user.id)]['current_payment_amount'] = amount
                            users_bd[str(message.from_user.id)]['flag'] = 0
                except:
                    bot.delete_message(chat_id=chat_id,
                                       message_id=message.message_id)
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Введите сумму пополнения в нужно формате (Для десятичных чисел используйте точку)',
                                          reply_markup=menu)

            if users_bd[user_id]["flag"] == 8:  # рассылка
                for u_id in users_bd:
                    if u_id != admin and u_id != "cash":
                        bot.send_message(chat_id=int(u_id), text=message.text,
                                         reply_markup=types.InlineKeyboardMarkup().add(
                                             types.InlineKeyboardButton(text='Скрыть уведомление',
                                                                        callback_data='hide')))
                users_bd[user_id]["flag"] = 17

            if users_bd[user_id]["flag"] == 10:  # начисление баланса
                try:
                    a = message.text.split(' ')
                    if len(a) == 2:
                        if int(a[0]) and int(a[1]) and a[0] in users_bd:
                            users_bd[a[0]]["balance"] += int(a[1])
                            users_bd["cash"]["all_deposits"] += int(a[1])
                            users_bd[user_id]["flag"] = 17
                            bot.send_message(chat_id=user_id, text="Готово",
                                             reply_markup=types.InlineKeyboardMarkup().add(
                                                 types.InlineKeyboardButton(text='Скрыть уведомление',
                                                                            callback_data='hide')))
                    else:
                        bot.send_message(chat_id=user_id, text="Что-то пошло не так")
                        users_bd[user_id]["flag"] = 17

                except:
                    bot.send_message(chat_id=user_id, text="Что-то пошло не так")
                    users_bd[user_id]["flag"] = 17

            if users_bd[user_id]["flag"] == 9:  # Бан
                if message.text in users_bd:
                    users_bd[message.text]["flag"] = 5
                    bot.send_message(chat_id=user_id, text="Готово", reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                else:
                    bot.send_message(chat_id=user_id, text="Данного пользователя нет в базе данных")
                users_bd[user_id]["flag"] = 17

            if users_bd[user_id]["flag"] == 11:  # Разбан
                if message.text in users_bd:
                    users_bd[message.text]["flag"] = 17
                    bot.send_message(chat_id=user_id, text="Готово", reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                else:
                    bot.send_message(chat_id=user_id, text="Что-то пошло не так")
                users_bd[user_id]["flag"] = 17
            # qiwi
            if users_bd[user_id]["flag"] == 12:
                users_bd['cash']['qiwi'] = message.text
                bot.send_message(chat_id=user_id, text="Готово. Вы ввели: " + message.text,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                users_bd[user_id]["flag"] = 17
            # bts
            if users_bd[user_id]["flag"] == 13:
                users_bd['cash']['btc'] = message.text
                bot.send_message(chat_id=user_id, text="Готово. Вы ввели: " + message.text,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                users_bd[user_id]["flag"] = 17
            # ltc
            if users_bd[user_id]["flag"] == 14:
                users_bd['cash']['ltc'] = message.text
                bot.send_message(chat_id=user_id, text="Готово. Вы ввели: " + message.text,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                users_bd[user_id]["flag"] = 17
            # usdt
            if users_bd[user_id]["flag"] == 15:
                users_bd['cash']['usdt'] = message.text
                bot.send_message(chat_id=user_id, text="Готово. Вы ввели: " + message.text,
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                users_bd[user_id]["flag"] = 17

    save_data(users_bd)


@bot.callback_query_handler(func=lambda call: True)
def hand(call):
    global users_bd
    user_id = str(call.from_user.id)
    users_bd = load_data()
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    support = 2098607188
    if user_id in users_bd:
        if users_bd[user_id]['flag'] != 5 and users_bd[user_id]['flag'] != 17:

            if call.data == "admin":
                bot.delete_message(chat_id=chat_id, message_id=users_bd[user_id]["bot_messageId"])
                r = bot.send_message(chat_id=chat_id,
                                     text='/admin – перечисление всех команд модератора с описанием \n/stats – статистика по '
                                          'боту, количество юзеров, общая сумма пополнений \n/dist – рассылка сообщений '
                                          'пользователям, к сообщениям в рассылке прикреплять кнопку – скрыть уведомление. '
                                          '\n/add – добавить баланс пользователю по его ID\n/ban – ограничить использование '
                                          'ботом пользователю по id \n/qiwi , /usdt , /btc , /ltc – вставка кошелька, '
                                          'должны заменять кошелек который пишется при оплате.\n/unban – разбанить '
                                          'пользователя по id ')
                users_bd[user_id]['bot_messageId'] = r.id
                users_bd[user_id]['flag'] = 17  # режим админа

            if call.data == 'chavo':
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='ЧАВО',
                                      reply_markup=types.InlineKeyboardMarkup().add(
                                          types.InlineKeyboardButton(text='МЕНЮ', callback_data='menu')))

            if call.data == 'menu':
                users_bd[user_id]['current_element'] = 0
                users_bd[user_id]['current_element_in_file'] = 0
                if user_id != admin:
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text="Привет! Это я, @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                                  int(users_bd[user_id]['balance'])), reply_markup=main_keyboard)
                    users_bd[user_id]['bot_messageId'] = r.id
                else:
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text="Привет! Это я, @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                                  int(users_bd[user_id]['balance'])), reply_markup=main_admin)
                    users_bd[user_id]['bot_messageId'] = r.id
                users_bd[user_id]['flag'] = 0

            if call.data == 'parsing':
                if not (float(users_bd[str(call.from_user.id)]['balance']) >= 4):
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Недостаточно средств на балансе для совершения парсинга',
                                          reply_markup=menu
                                          )
                if float(users_bd[str(call.from_user.id)]['balance']) >= 4:
                    changing_flag(str(call.from_user.id), 1)
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Введите ссылку',
                                          reply_markup=menu
                                          )

            if call.data == '100' or call.data == '200' or call.data == '500':
                if float(users_bd[str(call.from_user.id)]['balance']) < float(call.data) * 4:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Стоимость парсинга превышает ваш остаток на балансе. Введите другое число',
                                          reply_markup=string_keyboard)
                else:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text='Фирменный стикер + ожидание')
                    users_bd[str(call.from_user.id)]['balance'] = float(
                        users_bd[str(call.from_user.id)]['balance']) - int(
                        call.data) * 4
                    changing_flag(str(call.from_user.id), 0)
            ###### конец ветви парсинга ######
            ###### начало ветви баланс ######
            if call.data == 'balance':
                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text='Выберете способ оплаты',
                                      reply_markup=wallet_keyboard)
            if call.data == 'qiwi' or call.data == 'btc' or call.data == 'ltc' or call.data == 'usdt':
                users_bd[str(call.from_user.id)]['current_payment_method'] = call.data
                users_bd[str(call.from_user.id)]['current_wallet'] = users_bd['cash'][call.data]
                r = bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text=f'Введите сумму пополнения. Минимум 500руб.\n\nПисать нужно в рублях(Если не целое число, то пишите через точку)',
                                          reply_markup=menu)
                changing_flag(str(call.from_user.id), 6)
            """if call.data == 'btc':
                course_btc = 500 / Btc()
                users_bd[str(call.from_user.id)]['current_payment_method'] = call.data
                users_bd[str(call.from_user.id)]['current_wallet'] = users_bd['cash']['btc']
                r = bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Введите сумму пополнения. Минимум 500руб/{round(course_btc,5)} BTC.\n\nПисать нужно в рублях(Если не целое число, то пишите через точку)',
                                    reply_markup=menu)
                changing_flag(str(call.from_user.id), 6)
            if call.data == 'ltc':
                users_bd[str(call.from_user.id)]['current_payment_method'] = call.data
                users_bd[str(call.from_user.id)]['current_wallet'] = users_bd['cash']['ltc']
                course_ltc = 500 / Ltc()
                r =bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Введите сумму пополнения. Минимум 500руб/{round(course_ltc,5)} LTC.\n\nПисать нужно в рублях (Если не целое число, то пишите через точку)',
                                    reply_markup=menu)
                changing_flag(str(call.from_user.id), 6)
            if call.data == 'usdt':
                users_bd[str(call.from_user.id)]['current_payment_method'] = call.data
                users_bd[str(call.from_user.id)]['current_wallet'] = users_bd['cash']['usdt']
                course_usdt = 500 / Usdt()
                r = bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=f'Введите сумму пополнения. Минимум 500руб/{round(course_usdt,5)} USDT.\n\nПисать нужно в рублях(Если не целое число, то пишите через точку)',
                                    reply_markup=menu)
                changing_flag(str(call.from_user.id), 6)

            """
            if call.data == 'pay':
                if user_id == admin:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                              int(users_bd[user_id]['balance'])),
                                          reply_markup=main_admin)
                else:
                    bot.edit_message_text(chat_id=chat_id,
                                          message_id=message_id,
                                          text="Привет! Добро пожаловать в @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                              int(users_bd[user_id]['balance'])),
                                          reply_markup=main_keyboard)

                bot.send_message(chat_id=user_id, text="Ожидайте, заявка обрабатывается",
                                 reply_markup=types.InlineKeyboardMarkup().add(
                                     types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                users_bd = load_data()
                print(call.from_user.id)
                users_bd['cash']['user_id'].append(call.from_user.id)
                print(users_bd['cash']['user_id'])
                save_data(users_bd)
                ###### конец ветви баланс ######
                ### отправка сообщения саппорту
                support_keyboard = types.InlineKeyboardMarkup(row_width=1)
                paid = types.InlineKeyboardButton(text='Оплачено',
                                                  callback_data=f'paid {call.from_user.id} {users_bd[str(call.from_user.id)]["current_payment_amount"]}')
                cancel = types.InlineKeyboardButton(text='Отмена', callback_data=f'cancel {call.from_user.id}')
                mes = types.InlineKeyboardButton(text='Сообщение', callback_data=f'message {call.from_user.id}')
                support_keyboard.add(paid, cancel, mes)
                if users_bd[str(call.from_user.id)]["current_payment_method"] == 'qiwi':
                    # round(users_bd[str(call.from_user.id)]["current_wallet"],5)
                    bot.send_message(support,
                                     text=f'Ник: @{call.from_user.username}\nСумма:{users_bd[str(call.from_user.id)]["current_payment_amount"]}руб\nКошелек:{users_bd[str(call.from_user.id)]["current_wallet"]}\nСпособ оплаты:{users_bd[str(call.from_user.id)]["current_payment_method"]}',
                                     reply_markup=support_keyboard)
                if users_bd[str(call.from_user.id)]["current_payment_method"] == 'btc':
                    btc = Btc()
                    bot.send_message(support,
                                     text=f'Ник: @{call.from_user.username}\nСумма:{users_bd[str(call.from_user.id)]["current_payment_amount"]}руб/{round(users_bd[str(call.from_user.id)]["current_payment_amount"] / btc, 5)} BTC\nКошелек:{users_bd[str(call.from_user.id)]["current_wallet"]}\nСпособ оплаты:{users_bd[str(call.from_user.id)]["current_payment_method"]}',
                                     reply_markup=support_keyboard)
                if users_bd[str(call.from_user.id)]["current_payment_method"] == 'ltc':
                    ltc = Ltc()
                    bot.send_message(support,
                                     text=f'Ник: @{call.from_user.username}\nСумма:{users_bd[str(call.from_user.id)]["current_payment_amount"]}руб/{round(users_bd[str(call.from_user.id)]["current_payment_amount"] / ltc, 5)} LTC\nКошелек:{users_bd[str(call.from_user.id)]["current_wallet"]}\nСпособ оплаты:{users_bd[str(call.from_user.id)]["current_payment_method"]}',
                                     reply_markup=support_keyboard)
                if users_bd[str(call.from_user.id)]["current_payment_method"] == 'usdt':
                    usdt = Usdt()
                    bot.send_message(support,
                                     text=f'Ник: @{call.from_user.username}\nСумма:{users_bd[str(call.from_user.id)]["current_payment_amount"]}руб/ {round(users_bd[str(call.from_user.id)]["current_payment_amount"] / usdt, 5)} USDT\nКошелек:{users_bd[str(call.from_user.id)]["current_wallet"]}\nСпособ оплаты:{users_bd[str(call.from_user.id)]["current_payment_method"]}',
                                     reply_markup=support_keyboard)

            if call.from_user.id == support:
                info = call.data.split(' ')
                if len(info) == 3:
                    bot.send_message(info[1],
                                     text='Оплата прошла успешно',
                                     reply_markup=types.InlineKeyboardMarkup().add(
                                         types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                    if users_bd[info[1]]['current_payment_method'] == 'qiwi':
                        users_bd[info[1]]['balance'] += float(info[2])
                        users_bd['cash']['all_deposits'] += float(info[2])
                    if users_bd[info[1]]['current_payment_method'] == 'btc':
                        btc = Btc()
                        users_bd[info[1]]['balance'] += float(info[2])
                        users_bd['cash']['all_deposits'] += float(info[2])
                    if users_bd[info[1]]['current_payment_method'] == 'ltc':
                        ltc = Ltc()
                        users_bd[info[1]]['balance'] += float(info[2])
                        users_bd['cash']['all_deposits'] += float(info[2])
                    if users_bd[info[1]]['current_payment_method'] == 'usdt':
                        usdt = Usdt()
                        users_bd[info[1]]['balance'] += float(info[2])
                        users_bd['cash']['all_deposits'] += float(info[2])
                    ind = users_bd['cash']['user_id'].index(int(info[1]))
                    del users_bd['cash']['user_id'][ind]

                if info[0] == 'cancel':
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                    bot.send_message(info[1],
                                     text='Транзакцию отменили',
                                     reply_markup=types.InlineKeyboardMarkup().add(
                                         types.InlineKeyboardButton(text='Скрыть уведомление', callback_data='hide')))
                    ind = users_bd['cash']['user_id'].index(int(info[1]))
                    del users_bd['cash']['user_id'][ind]

                if info[0] == 'message':
                    r = bot.edit_message_text(chat_id=chat_id,
                                              message_id=message_id,
                                              text='Введите сообщение')
                    users_bd[str(support)]["bot_messageId"] = r.id
                    changing_flag(str(support), 16)

            if call.data == "stroki":
                if user_id in os.listdir("STROKI") and len(os.listdir("STROKI/" + user_id)) != 0:
                    changing_flag(str(call.from_user.id), 3)
                    directory = "STROKI/" + str(call.from_user.id)
                    users_bd[str(call.from_user.id)]["cur_file_names"] = os.listdir(directory)
                    print(users_bd[str(call.from_user.id)]["cur_file_names"])
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Вот, что есть",
                                              reply_markup=keyboard_init(str(call.from_user.id)))
                    users_bd[user_id]['bot_messageId'] = r.id
                else:
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="У Вас нет файлов",
                                              reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                                                  types.InlineKeyboardButton(text='МЕНЮ', callback_data='menu')))
                    users_bd[user_id]['bot_messageId'] = r.id

            if call.data == ">":
                if users_bd[user_id]["flag"] == 3:
                    users_bd[user_id]["current_element"] += 5
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Вот, что есть",
                                              reply_markup=keyboard_init(str(call.from_user.id)))
                    users_bd[user_id]['bot_messageId'] = r.id

                if users_bd[user_id]["flag"] == 7:
                    users_bd[user_id]["current_element_in_file"] += 5
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response(user_id),
                                              reply_markup=keyboard_init(user_id))
                    users_bd[user_id]['bot_messageId'] = r.id

            if call.data == "<":
                if users_bd[user_id]["flag"] == 3:
                    users_bd[user_id]["current_element"] -= 5
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Вот, что есть",
                                              reply_markup=keyboard_init(str(call.from_user.id)))
                    users_bd[user_id]['bot_messageId'] = r.id

                if users_bd[user_id]["flag"] == 7:
                    users_bd[user_id]["current_element_in_file"] -= 5
                    r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response(user_id),
                                              reply_markup=keyboard_init(user_id))
                    users_bd[user_id]['bot_messageId'] = r.id

            if call.data in users_bd[user_id]["cur_file_names"]:
                users_bd[user_id]["current_file"] = call.data
                r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="Способ просмотра",
                                          reply_markup=types.InlineKeyboardMarkup(row_width=1).add(
                                              types.InlineKeyboardButton(text='Ручной сендер',
                                                                         callback_data='slider')).add(
                                              types.InlineKeyboardButton(text='Скачать документ',
                                                                         callback_data='download')).add(
                                              types.InlineKeyboardButton(text='МЕНЮ', callback_data='menu')))
                users_bd[user_id]['bot_messageId'] = r.id

            if call.data == "slider":
                changing_flag(user_id, 7)
                save_xml(user_id)
                r = bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=response(user_id),
                                          parse_mode='Markdown', reply_markup=keyboard_init(user_id))
                users_bd[user_id]['bot_messageId'] = r.id

            if call.data == "download":
                with open('STROKI/' + user_id + '/' + users_bd[user_id]["current_file"], 'rb') as f:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                    bot.send_document(chat_id=chat_id, data=f)
                    if user_id == admin:
                        r = bot.send_message(call.from_user.id,
                                             text="Привет! Это я, @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                                 int(users_bd[user_id]['balance'])), reply_markup=main_admin)
                        users_bd[str(call.from_user.id)]['bot_messageId'] = r.id
                    else:
                        r = bot.send_message(call.from_user.id,
                                             text="Привет! Это я, @\n\nТвой ID: " + user_id + "\n\nТвой баланс: " + str(
                                                 int(users_bd[user_id]['balance'])), reply_markup=main_keyboard)
                        users_bd[str(call.from_user.id)]['bot_messageId'] = r.id

        if call.data == "hide":
            bot.delete_message(chat_id=chat_id, message_id=message_id)
    save_data(users_bd)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=22, debug=True)
    #app.run()

