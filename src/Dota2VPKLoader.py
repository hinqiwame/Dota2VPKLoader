import winreg
import os
import shutil
from datetime import datetime
from colorama import Fore, init
import sys

def find_dota_directory():
    """
    Поиск пути к папке с файлами игры Dota 2 используя реестр Windows.
    """
    try:
        steam_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Valve\\Steam")
        steam_path = winreg.QueryValueEx(steam_key, "SteamPath")[0]
        library_folders_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")

        with open(library_folders_path, "r") as file:
            content = file.read()

        paths = [steam_path]
        for line in content.split("\n"):
            if "\"path\"" in line:
                library_path = line.split("\"")[3]
                paths.append(library_path)

        for path in paths:
            dota_path = os.path.join(path, "steamapps", "common", "dota 2 beta", "game")
            if os.path.exists(dota_path):
                print("[+] Папка Dota 2 найдена!")
                dota_path_normalized = os.path.normpath(dota_path)
                return dota_path_normalized
    except:
        return None

def check_mod_files(wdir):
    """
    Проверка наличия VPK и gameinfo.gi файлов.
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

def process_mod_directories(dir):
    """
    Работа с папками для мода.
    """
    print("[~] Работа с папками для мода...")
    
    if os.path.exists(f"{dir}\\Dota2SkinChanger"):
        print("[~] Найдена существующая папка Dota2SkinChanger. Производится очистка...")
        entries = os.listdir(f"{dir}\\Dota2SkinChanger")
        
        for entry in entries:
            entry_path = os.path.join(f"{dir}\\Dota2SkinChanger", entry)
            
            if os.path.isfile(entry_path):
                os.remove(entry_path)
                print(f"[+] {entry_path} удален")
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                print(f"[+] {entry_path} удален")
    else:
        os.makedirs(f"{dir}\\Dota2SkinChanger", exist_ok=True)
        print(f"[+] Папка Dota2SkinChanger создана в {dir}.")

def copy_mod_files(wdir, dir):
    """
    Перемещение файлов мода в соответствующие папки.
    """
    print("[~] Работа с файлами мода...")
    wpath = os.path.normpath(wdir)
    shutil.move(f"{wpath}\\pak01_dir.vpk", f"{dir}\\Dota2SkinChanger")
    print("[+] pak01_dir.vpk установлен")
    gameinfo_destination = f"{dir}\\dota\\gameinfo.gi"
    if os.path.exists(gameinfo_destination):
        os.remove(gameinfo_destination)
    shutil.move(f"{wpath}\\gameinfo.gi", f"{dir}\\dota")
    print("[+] gameinfo.gi заменен в файлах игры")

def main():
    """
    Функция, инициализирующая все остальные.
    """
    init()

    os.system("title Dota2VPKLoader / Created by https://t.me/staticsyscall / https://github.com/meth1337")

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
    
    print("\n[*] Инструкция по использованию: https://github.com/meth1337/Dota2VPKLoader\n")

    dir = find_dota_directory()
    if dir is None:
        print("[!] Скрипту не удалось автоматически найти путь к файлам игры Dota 2. Пожалуйста, введите путь вручную.")
        dir = input("[~] Введите путь к файлам игры Dota 2: ")
    else:
        pass

    check_mod_files(os.getcwd())
    process_mod_directories(dir)
    copy_mod_files(os.getcwd(), dir)

    print("[+] Установка мода успешно завершена! Приятной игры <3")
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
