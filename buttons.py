from telebot import types

import db


#Кнопка для отправки номера
def num_button():
    #Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    #Создаем сами кнопки
    num = types.KeyboardButton('Поделиться контактом', request_contact=True)

    #Добавляем кнопки в пространство
    kb.add(num)
    return kb

#Конпка для отправки локации
def loc_button():
    # Создаем пространство для кнопок
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    # Создаем сами кнопки
    loc = types.KeyboardButton('Поделиться геопозицией', request_location=True)

    # Добавляем кнопки в пространство
    kb.add(loc)
    return kb

def remove():
    types.ReplyKeyboardRemove()

#Кнопки для выбора товаров
def main_menu_buttons(products_from_db):
    #Создаем пространство для конпок
    kb = types.InlineKeyboardMarkup(row_width=3)

    #Создаем несгораемую кнопку корзины
    cart = types.InlineKeyboardButton(text = 'Корзина', callback_data='cart')
    #создаем кнопки с продуктами
    all_products = [types.InlineKeyboardButton(text = f'{i[1]}',
                    callback_data=i[1])
                    for i in products_from_db]

    #Объеденяем кнопки с пространством
    kb.row(cart)
    kb.add(*all_products)

    #Возвращаем пространство
    return kb

def all_products_buttons(products_from_db):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in products_from_db:
        kb.add(i[0])

    return kb
#Кнопки выбора количества
def choose_product_count(current_amount=1,plus_or_minus = ''):
    #Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=3)

    #Создаем несгораемые кнопкм
    back = types.InlineKeyboardButton(text='Назад', callback_data='back')
    plus = types.InlineKeyboardButton(text='+', callback_data='increment')
    minus = types.InlineKeyboardButton(text='-', callback_data='decrement')
    count = types.InlineKeyboardButton(text=str(current_amount),
                                       callback_data=str(current_amount))
    add_to_cart = types.InlineKeyboardButton(text='Добавить в корзину', callback_data='to cart')


    #отслеживание плюса и минуса
    if plus_or_minus == 'increment':
        new_amount = int(current_amount) + 1

        count = types.InlineKeyboardButton(text=str(new_amount),
                                           callback_data=str(new_amount))

    elif plus_or_minus == 'decrement':
        if int(current_amount) > 1:
            new_amount = int(current_amount) - 1

            count = types.InlineKeyboardButton(text=str(new_amount),
                                               callback_data=str(new_amount))


    #Объеденяем кнопки с пространством
    kb.add(minus, count, plus)
    kb.row(add_to_cart)
    kb.row(back)

    return kb


#Кнопки корзины
def cart_buttons():
    #Создаем пространство
    kb = types.InlineKeyboardMarkup(row_width=1)

    #Создаем кнопки
    clear_cart = types.InlineKeyboardButton(text = 'Очистить корзину',
                                            callback_data='clear_cart')

    order = types.InlineKeyboardButton(text= 'Оформить заказ',
                                       callback_data='order')

    back = types.InlineKeyboardButton(text='Назад',
                                      callback_data='back')

    #Объеденяем с пространством
    kb.add(clear_cart, order, back)
    return kb


#Кнопки админа
def admin_buttons():
    #Создаем пространство
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)


    #Создаем конпки
    add_adm_pr = types.KeyboardButton('Добавить продукты')
    del_adm_pr = types.KeyboardButton('Удалить продукты')

    kb.add(add_adm_pr, del_adm_pr)

    return kb

def admin_show_pr_bt():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

    sh_pr = types.KeyboardButton('Show products')
    kb.add(sh_pr)

    return kb
#
# def admin_buttons_del():
#     #Создаем пространство
#     kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
#
#     #Создаем конпки
#     add_adm_pr = types.KeyboardButton('Удалить продукты')
#
#     kb.add(add_adm_pr)
#
#     return kb
























































