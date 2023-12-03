
import os
import json
import datetime


save_dir = r"savefiles"
autosave_dir = r"savefiles\autosaves"
load_dir = r"import"

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

    if len(file_list) == 25:
        
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

# def save():

#     os.chdir(save_dir) if os.getcwd().basename != save_dir else None
    
#     save_name = input("Введите имя файла для сохранения: ")

#     try:

#         with open(save_name, "w", encoding="utf-8") as ct:
    
#             json.dump(phonebook, ct)   
#             print("Cохраниение завершено")

#     except:
#         print("Ошибка!","Телефонная книга не сохранена",sep="\n",end="\n\n")

#     return

def save():
    try:
        os.makedirs(save_dir, exist_ok=True) # Создаем папку, если ее нет
        timestamp = int(datetime.datetime.now().timestamp())
        autosave_name = f"autosave_{timestamp}.json" # создание имени по дате
        with open(os.path.join(save_dir, autosave_name), "w", encoding="utf-8") as ct:
            json.dump(phonebook, ct, ensure_ascii=False, indent=4)
        print("Сохранение завершено")
    except Exception as e:
        print(f"Произошла ошибка при сохранении: {e}")

def load():

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



#phonebook = {}
phonebook = autoload()