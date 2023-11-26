'''
Задача №49.

Решение в группах
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. 
Фамилия, имя, отчество, номер телефона - данные, которые должны находиться
в файле.

1. Программа должна выводить данные

2. Программа должна сохранять данные в
текстовом файле

3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)

4. Использование функций. Ваша программа
не должна быть линейной
'''

import os
import json
import datetime


save_dir = r"savefiles"
autosave_dir = r"savefiles\autosaves"

# Операции

def get_file_list(dir):

    file_list = os.listdir(dir)
    full_path = ["{0}/{1}".format(dir,x) for x in file_list]

    return (file_list, full_path)

def autoload():

    all_files = get_file_list(autosave_dir)[1] + get_file_list(save_dir)[1] 
    
    oldest_file = max(all_files, key=os.path.getctime)

    print("Загрузка телефонной книги...")

    try:

        with open(oldest_file, "r", encoding="utf-8") as ct:
            
            phonebook = json.load(ct)
            print("Загрузка завершена")

    except:

        print("Ошибка!","Телефонная книга не загружена!",sep="\n",end="\n\n")

        phonebook = dict()

    return phonebook

def autosave():

    file_list, full_path = get_file_list(autosave_dir)[0], get_file_list(autosave_dir)[1]

    if len(file_list) == 10:
        
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

    os.chdir(autosave_dir)
    timestamp = int(datetime.datetime.now().timestamp())
    autosave_name = f"autosave_{timestamp}.json"

    print("Автосохранение телефонной книги...")

    try:

        with open(autosave_name, "w", encoding="utf-8") as ct:
    
            json.dump(phonebook, ct)   
            print("Автосохраниение завершено")

    except:
        print("Ошибка!","Телефонная книга не сохранена",sep="\n",end="\n\n")
    
    return

def save():

    os.chdir(save_dir) if os.getcwd().basename != save_dir else None
    
    save_name = input("Введите имя файла для сохранения: ")

    try:

        with open(save_name, "w", encoding="utf-8") as ct:
    
            json.dump(phonebook, ct)   
            print("Cохраниение завершено")

    except:
        print("Ошибка!","Телефонная книга не сохранена",sep="\n",end="\n\n")

    return

def load():

    return

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

def close_app():

    autosave()

    globals()['app_active'] = False

    print("Приложение закрыто\n")

    return

# Словарь операций

def main_cycle():

    operations_dict = {
                        # 'add': [add_contact, "Добавить контакт"],
                        # 'del': [del_contact, "Удалить контакт"],
                        # 'find': [find_contact,"Найти контакт"],
                        # 'all': [show_all, "Показать все контакты"],
                        'edit': [edit_contact,"Изменить контакт"],
                        'load': [load,"Загрузить телефонную книгу"],
                        'save': [save,"Сохранить телефонную книгу"],
                        'close': [close_app,"Закрыть приложение"],
                        }

    while app_active:

        print(f"В книге {len(phonebook)} контактов",
              "Доступные команды:",
              "\n".join([f"{i} - {operations_dict[i][1]}" for i in operations_dict.keys()]),sep="\n\n",end="\n\n")
               

        
        command = input('Введите комманду: ')
        print()
            
        try: 
            operations_dict[command][0]()
        
        except:
            print('Команда не найдена')

        

# структура контакта
'''
     {"дядя Ваня": {'phones': [1212121,5555555],
                           'email': '777@mail.com', 'birthday': '10.10.1990'},
            }
'''

app_active = True
phonebook = autoload()
print("")
main_cycle()