# ссылка на созданный мной ТГ-бот: t.me/HWphonebookbot

import telebot
import json
from telebot import types

#from command_script import add_contact, show_all, edit_contact
from dir_script import load, save, autoload, autosave, phonebook

#phonebook = autoload()

bot = telebot.TeleBot('6315653937:AAHTlQ2NYEqBOLjoGOt0Up56cqV4DT7-nDc')


contact_name = None


@bot.message_handler(commands=['start'])
def main_start(message):
    bot.send_message(message.chat.id, f'''Привет {message.from_user.first_name}! Это Телефонная-книга бот.\n 
                      Я храню список твоих контактов, могу добавлять,
                      удалять, искать и изменять контакты. Список команд:
                     <b>add</b> - добавить контакт;\n  <b>del</b> - удалить контакт;\n  <b>find</b> - поиск контакта;\n 
                      <b>all</b> - показать все контакты;\n  <b>edit</b> - изменить контакт''', parse_mode='html')



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

def add_contact2(phonebook, name, phones, email, birthday):
    contact = {"phones": phones, "email": email, "birthday": birthday}
    phonebook[name] = contact
    save()
    autosave()


############################################
@bot.message_handler(commands=['all'])
def show_all_tgbot(message):
    bot.send_message(message.chat.id, 'Список контактов: ')
    for name, contact_info in phonebook.items():
        murkup_inline = types.InlineKeyboardMarkup()
        item_info = types.InlineKeyboardButton(text='Инфо', callback_data=name)
        murkup_inline.add(item_info)
        bot.send_message(message.chat.id, f'Имя: {name}', reply_markup=murkup_inline)


#Функция выполнения логики кнопки "инфо" - вывод информации по выбранному контакту
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
        response += 'Чтобы изменить контакт выбирите необходимый параметр'
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


# @bot.callback_query_handler(func=lambda call: call.data.startswith('edit'))
# def edit_contact_info(call):
#     global contact_name
#     contact_name = call.data
#     bot.send_message(call.message.chat.id, f'Выбран контакт {contact_name}. Выберите, что нужно изменить:', reply_markup=get_edit_keyboard())




############################################
# @bot.callback_query_handler(func=lambda call: True)
# def show_info_tgbot(call):
#     if call.data in phonebook:
#         contact_info = phonebook[call.data]
#         info_message = f'Информация по контакту {call.data}: \n'
#         info_message += contact_phone_count(contact_info)
#         info_message += f'Почта: {contact_info["email"]} \n'
#         info_message += f'Дата рождения: {contact_info["birthday"]}'

#         keyboard = types.InlineKeyboardMarkup()
#         edit_button = types.InlineKeyboardButton(text='Изменить', callback_data=f'edit_{call.data}')
#         keyboard.add(edit_button)

#         bot.send_message(call.message.chat.id, info_message, reply_markup=keyboard)

############################################
'''Версия команды edit до объединения с all'''
############################################
# @bot.message_handler(commands=['edit'])
# def edit_contact_tg(message):
#     bot.send_message(message.chat.id, 'Выберите контакт для изменения из списка: ')
#     for name2, contact_info in phonebook.items():
#         markup2 = types.InlineKeyboardMarkup()
#         item_edit = types.InlineKeyboardButton(text='Изменить', callback_data= name2)
#         markup2.add(item_edit)
#         bot.send_message(message.chat.id, f'Имя: {name2}', reply_markup=markup2)


# @bot.callback_query_handler(func=lambda call: call.data.startswith('edit')) # call.data.startswith('all')
# def edit_contact_info(call):
    
#     if call.data == 'edit_name':
#         bot.send_message(call.message.chat.id, "Введите новое имя контакта:")
#         bot.register_next_step_handler(call.message, process_new_name)
#     elif call.data == 'edit_phone':
#         bot.send_message(call.message.chat.id, "Введите новый телефон контакта:")
#         bot.register_next_step_handler(call.message, process_new_phone)
#     elif call.data == 'edit_email':
#         bot.send_message(call.message.chat.id, "Введите новую почту контакта:")
#         bot.register_next_step_handler(call.message, process_new_email)
#     elif call.data == 'edit_birthday':
#         bot.send_message(call.message.chat.id, "Введите новую дату рождения контакта (в формате ДД.ММ.ГГГГ):")
#         bot.register_next_step_handler(call.message, process_new_birthday)


# @bot.callback_query_handler(func=lambda call: call.data.startswith('edit_'))
# def callback_query(call):
#     global contact_name
#     contact_name = call.data.split('_')[1]
#     bot.send_message(call.message.chat.id, f'Выбран контакт {contact_name}. Выберите, что нужно изменить:', reply_markup=get_edit_keyboard())

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
# Обновляем имя выбранного контакта в телефонной книге
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
#         bot.send_message(message.chat.id, "Номер телефона успешно изменен.")

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




############################################
############################################
############################################

'''Вариант команды all до того момента как я объединил его с edit'''
# @bot.message_handler(commands=['all'])
# def show_all_tgbot(message):
#     bot.send_message(message.chat.id, 'Список контактов: ')
#     for name, contact_info in phonebook.items():
#         murkup_inline = types.InlineKeyboardMarkup()
#         item_info = types.InlineKeyboardButton(text='Инфо', callback_data=name)
#         murkup_inline.add(item_info)
#         bot.send_message(message.chat.id, f'Имя: {name}', reply_markup=murkup_inline)

# #Функция выполнения логики кнопки "инфо" - вывод информации по выбранному контакту
# @bot.callback_query_handler(func=lambda call: True)
# def info_contact(call):
#     contact_name = call.data
#     contact_info = phonebook[contact_name]
#     response = f'Имя: {contact_name}\n'
#     #response += f'Телефоны: {contact_phone_count(contact_info)}'
#     response += contact_phone_count(contact_info)
#     #response += f'Телефоны: {", ".join(str(phone) for phone in contact_info["phones"])}\n'
#     response += f'Email: {contact_info["email"]}\n'
#     response += f'День рождения: {contact_info["birthday"]}\n'
#     bot.send_message(call.message.chat.id, response)

'''Конец команды all до объединения с edit'''



# @bot.callback_query_handler(func=lambda call: True)
# def info_contact(call):
#     contact_name = call.data
#     contact_info = phonebook[contact_name]
#     response = f'Имя: {contact_name}\n'
#     #response += f'Телефоны: {contact_phone_count(contact_info)}'
#     response += contact_phone_count(contact_info)
#     #response += f'Телефоны: {", ".join(str(phone) for phone in contact_info["phones"])}\n'
#     response += f'Email: {contact_info["email"]}\n'
#     response += f'День рождения: {contact_info["birthday"]}\n'
#     bot.send_message(call.message.chat.id, response)

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
        #del_contact(phonebook, name)
        bot.send_message(chat_id, f'Контакт {name} - удален!')
    else:
        bot.send_message(chat_id, 'Неправильный формат ввода. Пример правильного ввода: /del Имя')

# удаление контакта
# def del_contact(phonebook, name):
#     del phonebook[name]
#     save()

''' РАСКОМЕНТИТЬ'''
# @bot.message_handler(commands=['edit'])
# def edit_contact_tg(message):
#     bot.send_message(message.chat.id, 'Выберите контакт для изменения из списка: ')
#     for name, contact_info in phonebook.items():
#         #murkup = types.InlineKeyboardMarkup(resize_keyboard = True)
#         murkup = types.InlineKeyboardMarkup()
#         item_edit = types.InlineKeyboardButton(text='Изменить', callback_data = 'edit')
#         murkup.add(item_edit)
#         bot.send_message(message.chat.id, f'Имя: {name}', reply_markup=murkup)


############################################




############################################
'''РАСКОМЕНТИТЬ'''
# @bot.callback_query_handler(func=lambda call: call.data == 'edit')
# def edit_contact(call):
#     contact_name = call.data
#     contact_info = phonebook[contact_name]
#     murkup_edit = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item_name = types.KeyboardButton('Имя')
#     item_phone = types.KeyboardButton('Телефон')
#     item_email = types.KeyboardButton('Почта')
#     item_birthday = types.KeyboardButton('ДР')
#     murkup_edit.add(item_name, item_phone, item_email, item_birthday)

#     response = f'Выберите, что будем менять?\nИмя: {contact_name}\n'
#     response += contact_phone_count(contact_info)
#     bot.send_message(call.message.chat.id, response, reply_markup=murkup_edit)






# @bot.callback_query_handler(func=lambda call: call.data == 'edit_info')
# def edit_contact(call):
#     contact_name = call.data
#     murkup_edit = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item_name = types.KeyboardButton('Имя')
#     item_phone = types.KeyboardButton('Телефон')
#     item_email = types.KeyboardButton('Почта')
#     item_birthday = types.KeyboardButton('ДР')
#     murkup_edit.add(item_name, item_phone, item_email, item_birthday)

#     if contact_name in phonebook:
#         contact_info = phonebook[contact_name]  
#         response = f'Выберите, что будем менять?\nИмя: {contact_name}\n'
#         response += contact_phone_count(contact_info)
#         # response += f'Email: {contact_info["email"]}\n'
#         # response += f'День рождения: {contact_info["birthday"]}\n'

#         bot.send_message(call.message.chat.id, response, reply_markup=murkup_edit)
#     else:
#         bot.send_message(call.message.chat.id, f'Контакт {contact_name} не найден.')



bot.polling(non_stop=True)
