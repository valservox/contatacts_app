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
    
    oldest_file = min(all_files, key=os.path.getctime)

    print("Загрузка телефонной книги...")

    try:

        with open(oldest_file, "r", encoding="utf-8") as ct:
            
            phonebook = json.load(ct)
            print("Загрузка завершена")

    except:

        print("Ошибка!","Телефонная книга не загружена!",sep="\n")

        phonebook = dict()

    return phonebook

def autosave():

    os.chdir(autosave_dir) if os.getcwd().basename != autosave_dir else None

    func_res = get_file_list(autosave_dir)
    file_list, full_path = func_res[0], func_res[1]

    if len(file_list) == 25:
        
        oldest_file = min(full_path, key=os.path.getctime)
        os.remove(oldest_file)

    timestamp = datetime.datetime.now().timestamp()
    autosave_name = f"autosave_{timestamp}.json"

    print("Автосохранение телефонной книги...")

    try:

        with open(autosave_name, "w", encoding="utf-8") as ct:
    
            json.dump(phonebook, ct)   
            print("Автосохраниение завершено")

    except:
        print("Ошибка!","Телефонная книга не сохранена",sep="\n")
    
    return

def save():

    os.chdir(save_dir) if os.getcwd().basename != save_dir else None
    
    save_name = input("Введите имя файла для сохранения: ")

    try:

        with open(save_name, "w", encoding="utf-8") as ct:
    
            json.dump(phonebook, ct)   
            print("Cохраниение завершено")

    except:
        print("Ошибка!","Телефонная книга не сохранена",sep="\n")

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
        print("Ошибка!","Контакт или параметр контакта не найдены",sep="\n")

    autosave()

    return

def close_app():

    autosave()

    globals()['app_active'] = False

    return

# Словарь операций

def main_cycle():

    operations_dict = {
                #    'add': add_contact, 
                #    'del': del_contact, 
                #    'find': find_contact,
                #    'all': show_all, 
                   'edit': edit_contact,
                #    'import': import_contacts,
                #    'export': export_contacts,
                    'close': close_app,
                   }

    while app_active:

        print(f"""В книге  

Доступные команды:
               
add - добавить контакт 
del - удалить контакт
find - поиск контакта
all - показать все контакты
close - закрыть приложение
edit - изменить контакт
""")
        
        command = input('Введите комманду: ')
            
        try: 
            operations_dict[command]()
        
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
main_cycle()