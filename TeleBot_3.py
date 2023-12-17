import telebot
from telebot import types

bot = telebot.TeleBot('6856240062:AAFv6BSQk-Gn5FHkfvr_HQhNCAkMy0sS3TE')

clients = []  # Список для хранения информации о клиентах [{'chat_id': chat_id, 'name': 'Имя', 'phone': 'Номер телефона'}]

# Список с путями к фотографиям для каждого дашборда
dashboards_photos = {
    "Дашборд 1": r"C:\Users\Admin\Desktop\Работы 2 семестр\Современные программные средства\3 семестр\СПС\РГР_Дашборд_1.JPG",
    "Дашборд 2": r"C:\Users\Admin\Desktop\Работы 2 семестр\Современные программные средства\3 семестр\СПС\РГР_Дашборд_2.JPG",
    "Дашборд 3": r"C:\Users\Admin\Desktop\Работы 2 семестр\Современные программные средства\3 семестр\СПС\РГР_Дашборд_3.JPG",
    "Дашборд 4": r"C:\Users\Admin\Desktop\Работы 2 семестр\Современные программные средства\3 семестр\СПС\РГР_Дашборд_4.JPG",
    "Дашборд 5": r"C:\Users\Admin\Desktop\Работы 2 семестр\Современные программные средства\3 семестр\СПС\РГР_Дашборд_5.JPG",
}

@bot.message_handler(commands=['start'])
def start(message):
    commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'

    # Добавляем кнопку "Дашборды" в основную клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dashboards_button = types.KeyboardButton("Дашборды")
    markup.add(dashboards_button)

    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}\n\n{commands_info}', reply_markup=markup)

# Обработчик для кнопки "Дашборды"
@bot.message_handler(func=lambda message: message.text == "Дашборды")
def dashboards_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    dashboard_buttons = [types.KeyboardButton(dashboard) for dashboard in dashboards_photos.keys()]
    markup.add(*dashboard_buttons)

    bot.send_message(message.chat.id, "Выберите дашборд:", reply_markup=markup)

# Обработчики для каждого дашборда
@bot.message_handler(func=lambda message: message.text in dashboards_photos.keys())
def show_dashboard_photo(message):
    chat_id = message.chat.id
    dashboard_name = message.text
    photo_path = dashboards_photos.get(dashboard_name)

    if photo_path:
        with open(photo_path, 'rb') as photo:
            bot.send_photo(chat_id, photo, caption=f"Фотография для {dashboard_name}")
    else:
        bot.send_message(chat_id, "Фотография не найдена.")

@bot.message_handler(commands=['help'])
def help_message(message):
    commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
    bot.send_message(message.chat.id, commands_info)

@bot.message_handler(commands=['add'])
def add_client(message):
    bot.send_message(message.chat.id, 'Введите ФИО клиента:')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    chat_id = message.chat.id
    name = message.text
    bot.send_message(chat_id, f'ФИО клиента "{name}" сохранено. Введите номер телефона: ')
    bot.register_next_step_handler(message, get_phone, name)

def get_phone(message, name):
    chat_id = message.chat.id
    phone = message.text
    clients.append({'chat_id': chat_id, 'name': name, 'phone': phone})
    bot.send_message(chat_id, f'Номер телефона "{phone}" сохранен.')
    commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
    bot.send_message(message.chat.id, commands_info)

@bot.message_handler(commands=['list'])
def list_clients(message):
    chat_id = message.chat.id
    client_list = [f'{index + 1}. Имя: {client["name"]}, Номер телефона: {client["phone"]}' for index, client in enumerate(clients) if client["chat_id"] == chat_id]
    if client_list:
        bot.send_message(chat_id, 'Список ваших клиентов:\n' + '\n'.join(client_list))
        commands_info = 'Доступные команды:\n' \
                        '/add - Добавить нового клиента\n' \
                        '/list - Список сохраненных клиентов\n' \
                        '/edit - Редактировать клиента\n' \
                        '/clear - Очистить список клиентов\n' \
                        '/help - Помощь'
        bot.send_message(message.chat.id, commands_info)
    else:
        bot.send_message(chat_id, 'Вы еще не добавили клиентов. Используйте /add.')
        commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
        bot.send_message(message.chat.id, commands_info)

@bot.message_handler(commands=['edit'])
def edit_client(message):
    chat_id = message.chat.id
    client_list = [f'{index + 1}. Имя: {client["name"]}, Номер телефона: {client["phone"]}' for index, client in enumerate(clients) if client["chat_id"] == chat_id]
    if client_list:
        bot.send_message(chat_id, 'Выберите цифру клиента для редактирования:\n' + '\n'.join(client_list))
        bot.register_next_step_handler(message, select_client_to_edit)
    else:
        bot.send_message(chat_id, 'Вы еще не добавили клиентов. Используйте /add.')
        commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
        bot.send_message(message.chat.id, commands_info)

def select_client_to_edit(message):
    chat_id = message.chat.id
    try:
        selected_index = int(message.text) - 1
        selected_client = clients[selected_index]
        # Сохраняем chat_id выбранного клиента в специальном поле для дальнейших операций
        clients[selected_index]['editing_chat_id'] = chat_id
        bot.send_message(chat_id, f'Выбран клиент для редактирования:\n'
                                  f'Имя: {selected_client["name"]}\n'
                                  f'Номер телефона: {selected_client["phone"]}\n\n'
                                  'Что вы хотите изменить:\n'
                                  '/edit_name - Изменить Имя\n'
                                  '/edit_phone - Изменить Номер телефона')
    except (ValueError, IndexError):
        bot.send_message(chat_id, 'Некорректный выбор. Пожалуйста, выберите номер клиента для редактирования.')

@bot.message_handler(commands=['edit_name'])
def edit_name_handler(message):
    chat_id = message.chat.id
    selected_index = get_selected_index(chat_id)
    if selected_index is not None:
        bot.send_message(chat_id, 'Введите новое Имя:')
        bot.register_next_step_handler(message, update_name)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуйте еще раз.')

def update_name(message):
    chat_id = message.chat.id
    new_name = message.text
    selected_index = get_selected_index(chat_id)
    if selected_index is not None:
        clients[selected_index]['name'] = new_name
        bot.send_message(chat_id, f'Имя клиента изменено на "{new_name}".')
        del clients[selected_index]['editing_chat_id']  # Очищаем поле editing_chat_id
        commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
        bot.send_message(message.chat.id, commands_info)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуйте еще раз.')

@bot.message_handler(commands=['edit_phone'])
def edit_phone_handler(message):
    chat_id = message.chat.id
    selected_index = get_selected_index(chat_id)
    if selected_index is not None:
        bot.send_message(chat_id, 'Введите новый номер телефона:')
        bot.register_next_step_handler(message, update_phone)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуйте еще раз.')

def update_phone(message):
    chat_id = message.chat.id
    new_phone = message.text
    selected_index = get_selected_index(chat_id)
    if selected_index is not None:
        clients[selected_index]['phone'] = new_phone
        bot.send_message(chat_id, f'Номер телефона изменен на "{new_phone}".')
        del clients[selected_index]['editing_chat_id']  # Очищаем поле editing_chat_id
        commands_info = 'Доступные команды:\n' \
                    '/add - Добавить нового клиента\n' \
                    '/list - Список сохраненных клиентов\n' \
                    '/edit - Редактировать клиента\n' \
                    '/clear - Очистить список клиентов\n' \
                    '/help - Помощь'
        bot.send_message(message.chat.id, commands_info)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так. Попробуйте еще раз.')

def get_selected_index(chat_id):
    for index, client in enumerate(clients):
        if client['chat_id'] == chat_id:
            return index
    return None

@bot.message_handler(commands=['clear'])
def clear_clients(message):
    chat_id = message.chat.id
    clients.clear()
    bot.send_message(chat_id, 'Список клиентов успешно очищен.')