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
# структура контакта
'''
     {"дядя Ваня": {'phones': [1212121,5555555],
                           'email': '777@mail.com', 'birthday': '10.10.1990'},
            }
'''

from command_script import add_contact, show_all, edit_contact, del_contact, find_contact
from dir_script import load, save, autoload, autosave, phonebook

# Операция завершения программы 
def close_app():
    save()

    autosave()

    globals()['app_active'] = False

    print("Приложение закрыто\n")

    return False

# Словарь операций

def main_cycle():

    operations_dict = {
                        'add': [add_contact, "Добавить контакт"],
                        'del': [del_contact, "Удалить контакт"],
                        'find': [find_contact,"Найти контакт"],
                        'all': [show_all, "Показать все контакты"],
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

app_active = True

print("")
main_cycle()