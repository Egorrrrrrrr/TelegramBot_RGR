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