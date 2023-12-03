# ссылка на созданный мной ТГ-бот: t.me/HWphonebookbot

import telebot
from telebot import types
from dir_script import  save,  autosave, phonebook


bot = telebot.TeleBot('6315653937:AAHTlQ2NYEqBOLjoGOt0Up56cqV4DT7-nDc')




contact_name = None
@bot.message_handler(commands=['start'])
def main_start(message):
    bot.send_message(message.chat.id, f'''Привет {message.from_user.first_name}! Это Телефонная-книга бот.\n Я храню список твоих контактов, могу добавлять, 
    удалять, выводить и изменять контакты. Список команд: <b>start</b> - приветственное окно чат-бота;\n <b>add</b> - добавить контакт;\n 
    <b>del</b> - удалить контакт;\n <b>find</b> - поиск контакта;\n <b>all</b> - показать все контакты;\n''', parse_mode='html')


# Запуск команды add для добавления контакта
@bot.message_handler(commands=['add'])
def add_contact_handler(message):
    chat_id = message.chat.id
    user_input = message.text.split(' ')
    if len(user_input) == 5:
        command, name, phones, email, birthday = user_input
        phones = list(map(int, phones.split(',')))
        add_contact2(phonebook, name, phones, email, birthday)
        bot.send_message(chat_id, f'Контакт {name} - успешно добавлен!')
    else:
        bot.send_message(chat_id, 'Неправильный формат ввода. Пример правильного ввода: /add Имя Телефон Email День_рождения')

# Функция для внесения в БД
def add_contact2(phonebook, name, phones, email, birthday):
    contact = {"phones": phones, "email": email, "birthday": birthday}
    phonebook[name] = contact
    save()
    autosave()


# Запуск команды all для просмотра контактов и корректировки
@bot.message_handler(commands=['all'])
def show_all_tgbot(message):
    bot.send_message(message.chat.id, 'Список контактов: ')
    for name, contact_info in phonebook.items():
        murkup_inline = types.InlineKeyboardMarkup()
        item_info = types.InlineKeyboardButton(text='Инфо', callback_data=name)
        murkup_inline.add(item_info)
        bot.send_message(message.chat.id, f'Имя: {name}', reply_markup=murkup_inline)


#Функция выполнения логики кнопки "инфо" - вывод информации по выбранному контакту, а также меню для корректировки контакта
@bot.callback_query_handler(func=lambda call: True)
def info_contact(call):
    if call.data in phonebook:
        global contact_name
        contact_name = call.data
        contact_info = phonebook[contact_name]
        response = f'Имя: {contact_name}\n'
        response += contact_phone_count(contact_info)        
        response += f'Email: {contact_info["email"]}\n'
        response += f'День рождения: {contact_info["birthday"]}\n'
        response += '\nЧтобы изменить контакт выбирите необходимый параметр из представленных ниже вариантов:'
        bot.send_message(call.message.chat.id, response, reply_markup=get_edit_keyboard())
        return contact_name
    if call.data == 'edit_name':      
        bot.send_message(call.message.chat.id, "Введите новое имя контакта:")
        bot.register_next_step_handler(call.message, process_new_name)
    elif call.data == 'edit_phone':
        bot.send_message(call.message.chat.id, "Введите новый телефон контакта:")
        bot.register_next_step_handler(call.message, process_new_phone)
    elif call.data == 'edit_email':
        bot.send_message(call.message.chat.id, "Введите новую почту контакта:")
        bot.register_next_step_handler(call.message, process_new_email)
    elif call.data == 'edit_birthday':
        bot.send_message(call.message.chat.id, "Введите новую дату рождения контакта (в формате ДД.ММ.ГГГГ):")
        bot.register_next_step_handler(call.message, process_new_birthday)

# Оформление кнопок для редактирования (клавиатура)
def get_edit_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_name = types.InlineKeyboardButton(text='Имя', callback_data='edit_name')
    btn_phone = types.InlineKeyboardButton(text='Телефон', callback_data='edit_phone')
    btn_email = types.InlineKeyboardButton(text='Почта', callback_data='edit_email')
    btn_birthday = types.InlineKeyboardButton(text='ДР', callback_data='edit_birthday')
    keyboard.add(btn_name, btn_phone, btn_email, btn_birthday)
    return keyboard

#Функции по изменению Имени, Телефона, Имейла, ДР
def process_new_name(message):
    global contact_name
    new_name = message.text
    phonebook[new_name] = phonebook.pop(contact_name)
    contact_name = new_name
    save()
    autosave()
    bot.send_message(message.chat.id, "Имя успешно изменено.")

# def process_new_phone(message):
#     global contact_name
#     new_phone = message.text
#     if contact_name in phonebook:
#         phonebook[contact_name]['phones'].append(new_phone)
#         save()
#         bot.send_message(message.chat.id, "Номер телефона успешно добавлен.")

def process_new_phone(message):
    global contact_name
    new_phone = int(message.text)
    if contact_name in phonebook:
        phonebook[contact_name]['phones'] = [new_phone]
        save()
        autosave()
        bot.send_message(message.chat.id, f"Номер телефона контакта {contact_name} успешно изменен.")

def process_new_email(message):
    global contact_name
    new_email = message.text
    phonebook[contact_name]['email'] = new_email
    save()
    autosave()
    bot.send_message(message.chat.id, f"Адрес электронной контакта {contact_name} почты успешно изменен.")

def process_new_birthday(message):
    global contact_name
    new_birthday = message.text
    phonebook[contact_name]['birthday'] = new_birthday
    save()
    autosave()
    bot.send_message(message.chat.id, f"Дата рождения контакта {contact_name} успешно изменена.")

#Проверка контакта на количество телефонов (проверка пока только для комманды all)
def contact_phone_count(contact_info):
    if len(contact_info["phones"]) >= 1:
        phones_str = ", ".join(str(phone) for phone in contact_info["phones"])
    else:
        phones_str = contact_info["phones"][0]
    #phones_str = contact_info["phones"][0] if len(contact_info["phones"]) >= 1 else ", ".join(contact_info["phones"])
    response = f'Телефоны: {phones_str}\n'
    return response

@bot.message_handler(commands=['del'])
def del_contact_tg(message):
    chat_id = message.chat.id
    user_input = message.text.split(' ')
    if len(user_input) == 2:
        command, name = user_input
        del phonebook[name]
        save()
        bot.send_message(chat_id, f'Контакт {name} - удален!')
    else:
        bot.send_message(chat_id, 'Неправильный формат ввода. Пример правильного ввода: /del Имя')

bot.polling(non_stop=True)
