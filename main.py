import telebot, buttons, db

from geopy import Nominatim

#Поддлючение к боту
bot = telebot.TeleBot('6312010807:AAFTKVrMkdYgsXic7TydMkLF90mr4mPO2qY')

#Работа с локацией
geolocator = Nominatim(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                  ' Chrome/114.0.0.0 Safari/537.36')

#Временные данные
users = {}

#Прописываем обработку команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    global user_id
    user_id = message.from_user.id
    check_user = db.checker(user_id)

    #Проверка на наличие пользователя в базе данных
    if check_user:
        products = db.get_pr_name_id()
        bot.send_message(user_id, 'Добро пожаловать!', reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.send_message(user_id, 'Выберите меню:', reply_markup=buttons.main_menu_buttons(products))
        print(products)

    

    else:
        bot.send_message(user_id, 'Hello, type your name!')
        #Перевести на этап получение имени
        bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_name = message.text
    bot.send_message(user_id, 'Great, now send your number!',
                     reply_markup=buttons.num_button())

    #Перевести на этап получение номера
    bot.register_next_step_handler(message, get_number, user_name)

@bot.message_handler(commands=['admin'])
def admin_message(message):
    global user_id
    user_id = message.from_user.id
    if user_id == 88444281:
        bot.send_message(user_id, 'Welcome admin', reply_markup=buttons.admin_buttons())
        bot.register_next_step_handler(message, admin_choice_add)
        bot.register_next_step_handler(message, admin_choice_del)

def admin_choice_add(message):
    if message.text == 'Добавить продукты':
        foods_choice = message.text
        bot.send_message(user_id, 'Good, add name of product!')
        bot.register_next_step_handler(message, adm_name_pr, foods_choice)

def adm_name_pr(message, foods_choice):
    foods_name = message.text
    bot.send_message(user_id, 'Good, now add amount!')
    bot.register_next_step_handler(message, adm_amount_pr, foods_name, foods_choice)

def adm_amount_pr(message, foods_name, foods_choice):
    foods_amount = message.text
    bot.send_message(user_id, 'Good, now add prise!')
    bot.register_next_step_handler(message, adm_price_pr, foods_name, foods_amount, foods_choice)

def adm_price_pr(message, foods_name, foods_amount, foods_choice):
    foods_price = message.text
    bot.send_message(user_id, 'Good, now add photo!')
    bot.register_next_step_handler(message, adm_photo_pr, foods_name, foods_amount, foods_price, foods_choice)

def adm_photo_pr(message, foods_name, foods_amount, foods_price, foods_choice):
    foods_photo = message.text
    bot.send_message(user_id, 'Good, now add description!')
    bot.register_next_step_handler(message, adm_des_pr, foods_name, foods_amount, foods_price,
                                   foods_photo, foods_choice)

def adm_des_pr(message, foods_name, foods_amount, foods_price, foods_photo, foods_choice):
    foods_des = message.text
    bot.send_message(user_id, 'Product successfully added!')
    bot.register_next_step_handler(message, foods_name,
                                   foods_amount, foods_price, foods_photo, foods_des, foods_choice, admin_show,
                                   admin_choice_del)
    db.add_product(foods_name, foods_amount, foods_price, foods_des, foods_photo)

def admin_choice_del(message):
    if message.text == 'Удалить продукты':
        db.get_pr_name()
        bot.send_message(user_id, 'Choose product', reply_markup=buttons.all_products_buttons(db.get_pr_name()))
        bot.register_next_step_handler(message, del_product)

def del_product(message):
        del_pro = message.text
        bot.send_message(user_id, 'Product deleted')
        db.del_product(del_pro)
def admin_show(message, foods_name, foods_amount, foods_price, foods_photo, foods_des, foods_choice):
    if message.text == 'show':
        food_show = message.text
        bot.send_message(user_id, 'Show products', reply_markup=buttons.admin_show_pr_bt())
        bot.register_next_step_handler(message, food_show, foods_name,
                                   foods_amount, foods_price, foods_photo, foods_des, foods_choice)
        db.show_info(message)

#Этап получение номера
def get_number(message, user_name):
    #Если пользователь отправил контакт через кнопку
    if message.contact:
        user_number = message.contact.phone_number
        bot.send_message(user_id, 'Now send your location!', reply_markup=buttons.loc_button())
        #Перевести на этап получение локации
        bot.register_next_step_handler(message, get_location, user_name, user_number)

    #Если не через кнопку
    else:
        bot.send_message(user_id, 'Send message through button!')
        bot.register_next_step_handler(message, get_number, user_name)

@bot.callback_query_handler(lambda call: call.data in ['increment', 'decrement', 'to cart', 'back'])
def get_user_count(call):
    chat_id = call.message.chat.id

    if call.data == 'increment':
        actual_count = users[chat_id]['pr_count']

        users[chat_id]['pr_count'] += 1
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count(actual_count, 'increment'))

    elif call.data == 'decrement':
        actual_count = users[chat_id]['pr_count']

        users[chat_id]['pr_count'] -= 1
        bot.edit_message_reply_markup(chat_id=chat_id,
                                      message_id=call.message.message_id,
                                      reply_markup=buttons.choose_product_count(actual_count, 'decrement'))

    elif call.data == 'back':
        products = db.get_pr_name_id()
        bot.edit_message_text('Выберите пункт меню:',
                              chat_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu_buttons(products))

    elif call.data == 'to_cart':
        products = db.get_pr_name_id()
        product_count = users[chat_id]['pr_count']

        user_product = users[chat_id]['pr_name']
        db.add_to_cart(chat_id, user_product, product_count)
        bot.edit_message_text('Продукт успешно добавлен! Хотите что-нибудь еще?',
                              chat_id,
                              call.message.message_id,
                              reply_markup=buttons.main_menu_buttons(products))


@bot.callback_query_handler(lambda call: call.data in ['cart', 'clear_cart', 'order', 'back'])
def cart_handle(call):
    user = call.message.chat.id
    message_id = call.message.message_id
    products = db.get_pr_name_id()

    if call.data == 'clear_cart':
        db.del_from_cart(user)
        bot.edit_message_text('Корзина очищена!',
                              user,
                              message_id,
                              reply_markup=buttons.main_menu_buttons(products))

    elif call.data == 'order':
        db.del_from_cart(user)
        bot.send_message(88444281, 'Новый заказ!')
        bot.edit_message_text('Заказ оформлен! Желаете что-то еще?',
                              user,
                              message_id,
                              reply_markup=buttons.main_menu_buttons(products))

    elif call.data == 'back':
        products = db.get_pr_name_id()
        bot.edit_message_text('Выберите пункт меню:',
                              user,
                              call.message.message_id,
                              reply_markup=buttons.main_menu_buttons(products))

    elif call.data == 'cart':
        bot.edit_message_text('Корзина',
                              user,
                              message_id,
                              reply_markup=buttons.cart_buttons())

def get_location(message, user_name, user_number):
    #Если пользователь отправил локацию через кнопку
    if message.location:
        user_location = geolocator.reverse(f"{message.location.longitude},"
                                           f"{message.location.latitude}")

        #Регистрируем пользователя
        db.register(user_id, user_name, user_number, user_location)
        bot.send_message(user_id, 'You have registrate successfuly!')

    #Если не через кнопку
    bot.send_message(user_id, 'Send message through button!')
    bot.register_next_step_handler(message, user_number, user_name, get_location)


#Функция выбора товара
@bot.callback_query_handler(lambda call: call.data in db.get_pr_id())
def get_user_product(call):
    chat_id = call.message.chat.id

    users[chat_id] = {'pr_name': call.data, 'pr_count': 1}

    message_id = call.message.message_id

    bot.edit_message_text('Выберите количество',
                          chat_id=chat_id, message_id=message_id,
                          reply_markup=buttons.choose_product_count())

#Запуск бота
bot.polling()
