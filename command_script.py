# Модуль с выведенными коммандами для телефонного справочника и ТГ бота
import os
import json
import datetime
from dir_script import autosave, autoload, phonebook

# save_dir = r"savefiles"
# autosave_dir = r"savefiles\autosaves"
# load_dir = r"import"

#get_file_list(dir)


# Выводит список всех контактов в адресной книге и совершает поиск по букве по контактам
def show_all():
    # for name, contact_info in phonebook.items():
    #     print(f'Имя: {name}')
    #     print(f'Телефоны: {contact_info['phones']}')
    #     # Еще один вариант вывода номера телефона на новой строке (Мне показался первый вариант более компактным)
    #     # print('Телефоны:')
    #     # for phone in contact_info['phones']:
    #     #     print(phone)
    #     print(f'Email: {contact_info["email"]}')
    #     print(f'День рождения: {contact_info["birthday"]}')
    #     print('------------------') 

# Новый вариант 
    print('Список контактов: ')
    for name in phonebook:
        print('')
        print(name)
        print('_____________')

    print('Для выбора контакта и просмотра сведений о нем, введите его полное имя или первую букву имени: ')
    search_letter = input("Введите букву для поиска: ")
    found = False
    for name in phonebook:
        if search_letter.lower() in name.lower():
            contact_info = phonebook[name]
            print('')
            print(f'Имя: {name}')
            print(f'Телефоны: {contact_info["phones"]}')
            print(f'Email: {contact_info["email"]}')
            print(f'День рождения: {contact_info["birthday"]}')
            print('_____________')
            found = True
            if not found:
                print("Контакт с такой буквой в имени не найден.")

# Изменение контакта Номера телефона, Имени, Имейла, ДР
def edit_contact():

    name = (input('Введите имя для редактирования контакта: '))

    def edit_phone():

        n_phone = int(input(f'У контакта {name} Несколько телефонов. Введите порядковый номер для редактирования: ')) if len(phonebook[name]['phones']) > 1 else 1

        new_phone = int(input(f'Введите номер телефона {n_phone} для контакта {name}: '))

        phonebook[name]['phones'][n_phone - 1] = new_phone

        return
    
    def edit_email():
    
        new_email = input(f'Введите новый Email для контакта {name}: ')

        phonebook[name]['email'] = new_email
    
        return
    
    def edit_birthdate():
    
        new_birthdate = input(f'Введите дату рождения для контакта {name}: ')

        phonebook[name]['birthday'] = new_birthdate
    
        return
    
    edit_dict = {
                 'phone': edit_phone,
                 'email':edit_email,
                 'birthdate':edit_birthdate
                 }

    field = input('''
Выберите поле для редактирования:
                  
phone - Телефон (по умолчанию 1й в списке) 
email - Электронная почта
birthdate - Дата рождения
'''
                  )
    
    try:
        edit_dict[field]()

    except:
        print("Ошибка!","Контакт или параметр контакта не найдены",sep="\n",end="\n\n")

    autosave()

    return



def add_contact():
    name= input('Введите имя: ')
    count_phone = int(input(f'Введите сколько номеров у контакта {name} от 1 до 10: '))
    phones = []
    if count_phone == 1:
        phone = int(input('Введите номер телефона: '))
        phones.append(phone)
    elif count_phone > 1 and count_phone <= 10:
        for count in range(count_phone):
            phone = int(input(f'Введите номер телефона {count + 1}: '))
            phones.append(phone)
    else:
        print('Количество телефонов для одного контакта не может быть больше десяти, равно нулю или быть отрицательным значением')
        return
    email = input('Введите email: ')
    birthday = input('Введите день рождения: ')
    contact = {"phones": phones, "email": email, "birthday": birthday}
    phonebook[name] = contact
    return

def del_contact(phonebook):
    name = input('Введите имя контакта чтоб удалить: ')
    del phonebook[name]
    print(f'Контакт с именем {name} удален!')

#phonebook = autoload()
