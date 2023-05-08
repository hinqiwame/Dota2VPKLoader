import os
import shutil
from datetime import datetime
from colorama import Fore, init
import sys

def check_dota(dir):
    """
    Проверяет наличие и валидность папки Dota 2.
    """
    print("[~] Проверка папки Dota 2...")
    path = os.path.normpath(dir)
    
    if os.path.exists(path):
        print("[+] Папка Dota 2 найдена! Проверка на валидность...")
        ckpath = os.path.join(path, "core")
        
        if os.path.isdir(ckpath):
            pass
        else:
            print("[!] Вы указали папку, в которой нету файлов игры. Пожалуйста, укажите валидную папку.")
            input("[~] Нажмите Enter чтобы закрыть окно.")
            os._exit(0)
    else:
        print("[!] Папка Dota 2 не найдена, проверьте, установлена ли Dota 2 на вашем ПК.")
        input("[~] Нажмите Enter чтобы закрыть окно.")
        os._exit(0)

def check_vpk(wdir):
    """
    Проверяет наличие VPK и gameinfo.gi файлов.
    """
    print("[~] Проверка VPK...")
    wpath_vpk = os.path.join(wdir, "pak01_dir.vpk")
    
    if os.path.exists(wpath_vpk):
        print("[+] VPK найден!")
    else:
        print("[!] VPK не найден. Пожалуйста, убедитесь что VPK мод находится в той же папке что и этот скрипт и перезапустите скрипт.")
        input("[~] Нажмите Enter чтобы закрыть окно.")
        os._exit(0)
        
    wpath_gameinfo = os.path.join(wdir, "gameinfo.gi")
    
    if os.path.exists(wpath_gameinfo):
        print("[+] Gameinfo найден!")
    else:
        print("[!] Gameinfo не найден. Пожалуйста, убедитесь что gameinfo.gi находится в той же папке что и этот скрипт и перезапустите скрипт.")
        input("[~] Нажмите Enter чтобы закрыть окно.")
        os._exit(0)

def work_dirs(dir):
    """
    Работает с папками для мода.
    """
    print("[~] Работаю с папками для мода...")
    path = os.path.normpath(dir)
    
    if os.path.exists(f"{path}\\Dota2SkinChanger"):
        print("[~] Найдена существующая папка Dota2SkinChanger. Выполняю очистку...")
        entries = os.listdir(f"{path}\\Dota2SkinChanger")
        
        for entry in entries:
            entry_path = os.path.join(f"{path}\\Dota2SkinChanger", entry)
            
            if os.path.isfile(entry_path):
                os.remove(entry_path)
                print(f"[+] Удалил {entry_path}")
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                print(f"[+] Удалил {entry_path}")
    else:
        os.makedirs(f"{path}\\Dota2SkinChanger", exist_ok=True)
        print(f"[+] Создал папку Dota2SkinChanger в {path}.")

def copy_files(wdir, dir):
    """
    Копирует файлы мода в соответствующие папки.
    """
    print("[~] Работаю с файлами мода...")
    wpath = os.path.normpath(wdir)
    path = os.path.normpath(dir)
    shutil.move(f"{wpath}\\pak01_dir.vpk", f"{path}\\Dota2SkinChanger")
    print("[+] Установил pak01_dir.vpk")
    shutil.move(f"{wpath}\\gameinfo.gi", f"{path}\\game")
    print("[+] Заменил gameinfo.gi в файлах игры")

def main():
    init()

    os.system('title "Dota2VPKLoader | Created by https://t.me/staticsyscall / https://github.com/meth1337"')

    print(Fore.LIGHTRED_EX + """⣿⣿⣿⣿⣿⣿⣶⣾⣿⣿⣿⣿⣿⣶⣿⣿⣿⣷⣿⣿⣿⣿
⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿
⣿⣿⣧⡀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣏⠁⠀⠀⢙⣿⣿⣿⣿
⣿⣿⣿⣿⣄⠀⠀⠀⠙⠻⢿⣿⣿⣿⣷⣦⡀⣸⣿⣿⣿⣿
⢹⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⡁
⣾⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⡇
⣿⣿⣿⣿⠿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣷
⢹⣿⣿⠇⠀⠈⠻⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⢠⣿⣿⣿
⣾⣿⣿⣄⡀⠀⠀⣈⣿⣿⣿⣿⣿⣦⡀⠀⠀⠀⣸⣿⣿⣿
⣿⣿⣿⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿
⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀""" + Fore.RESET)


    dir = input("[~] Введите путь к файлам игры Dota 2: ")

    check_dota(dir)
    check_vpk(os.getcwd())
    work_dirs(dir)
    copy_files(os.getcwd(), dir)

    print("[+] Установка мода успешно завершена!")
    input("[~] Нажмите Enter чтобы закрыть окно.")
    os._exit(0)

try:
    if __name__ == "__main__":
        main()
except:
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{now}-dump.txt"
    with open(filename, "w") as f:
            f.write(f"Exception occurred: {datetime.now()}\n")
            f.write(f"{sys.exc_info()}\n")
    print(f"\n[!] Во время выполнения программы возникла ошибка. Отчет об ошибке сохранен в {filename}.\n[~] Вы можете прислать этот файл мне в телеграм, чтобы я вам помог.\n[~] @staticsyscall")
    input("[~] Нажмите Enter чтобы закрыть окно.")
    os._exit(0)
