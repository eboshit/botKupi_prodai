from telebot import types

main_keyboard = types.InlineKeyboardMarkup(row_width =2)
parsing = types.InlineKeyboardButton(text = 'ПАРС',callback_data = 'parsing')
stroki = types.InlineKeyboardButton(text = 'МОИ СТРОКИ', callback_data = 'stroki')
balance = types.InlineKeyboardButton(text = 'ПОПОЛНИТЬ БАЛАНС', callback_data = 'balance')
chavo = types.InlineKeyboardButton(text = 'ЧАВО', callback_data = 'chavo')
main_keyboard.add(parsing,stroki)
main_keyboard.add(balance,chavo)

### кнопка меню
menu = types.InlineKeyboardMarkup(row_width=2)
menu_but = types.InlineKeyboardButton(text='Меню', callback_data='menu')
menu.add(menu_but)

string_keyboard = types.InlineKeyboardMarkup(row_width=1)
s = types.InlineKeyboardButton(text='100', callback_data='100')
d = types.InlineKeyboardButton(text='200', callback_data='200')
t = types.InlineKeyboardButton(text='500', callback_data='500')
string_keyboard.add(s, d, t, menu_but)

stroki_ = types.InlineKeyboardMarkup(row_width=1)
b = types.InlineKeyboardButton(text='Ручной сендер', callback_data='slider')
b1 = types.InlineKeyboardButton(text='Скачать документ', callback_data='download')
b3 = types.InlineKeyboardButton(text='МЕНЮ', callback_data='menu')


wallet_keyboard = types.InlineKeyboardMarkup(row_width=1)
qiwi = types.InlineKeyboardButton(text='QIWI', callback_data='qiwi')
btc = types.InlineKeyboardButton(text='BTC', callback_data='btc')
ltc = types.InlineKeyboardButton(text='LTC', callback_data='ltc')
usdt = types.InlineKeyboardButton(text='USDT', callback_data='usdt')
wallet_keyboard.add(qiwi, btc, ltc, usdt, menu_but)

payment_keyboard = types.InlineKeyboardMarkup(row_width=1)
pay = types.InlineKeyboardButton(text='Оплатил', callback_data='pay')
payment_keyboard.add(pay, menu_but)

main_admin = types.InlineKeyboardMarkup(row_width=2)
main_admin.add(parsing, stroki)
main_admin.add(balance, chavo)
main_admin.add(types.InlineKeyboardButton(text='АДМИНКА', callback_data='admin'))
