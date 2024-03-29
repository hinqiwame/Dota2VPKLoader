import requests
import winreg
import os
import shutil
from datetime import datetime
from colorama import Fore, init
import importlib.util
import sys

current_version = "0.0.7"  # Версия скрипта

def positive_log(text):
    print(f"[+] {text}")

def negative_log(text):
    print(f"[!] {text}")

def neutral_log(text):
    print(f"[~] {text}")

def get_latest_version(url: str) -> str:
    """
    Минорная функция взаимодействующая с check_for_updates.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip().strip('\n')

def check_for_updates(current_version: str, version_url: str) -> None:
    """
    Проверка лоадера на наличие обновлений.
    """
    latest_version = get_latest_version(version_url)
    if latest_version != current_version:
        positive_log("Для вашей сборки найдено новое обновление! Скачать его можно здесь: https://github.com/qqqwwqeeqqwe/Dota2VPKLoader/releases/latest")
    else:
        neutral_log("Для вашей сборки не найдено обновлений.")

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
                dota_path_normalized = os.path.normpath(dota_path)
                return dota_path_normalized
    except:
        return None

def check_mod_files(working_directory):
    """
    Проверка наличия VPK и gameinfo.gi файлов.
    """
    neutral_log("Проверка VPK...")
    wpath_vpk = os.path.join(working_directory, "pak01_dir.vpk")
    
    if os.path.exists(wpath_vpk):
        positive_log("VPK найден!")
    else:
        negative_log("VPK не найден. Пожалуйста, убедитесь что VPK мод находится в той же папке что и этот скрипт и перезапустите скрипт.")
        input("[~] Нажмите Enter чтобы закрыть окно.")
        os._exit(0)
    
    neutral_log("Проверка gameinfo...")
    wpath_gameinfo = os.path.join(working_directory, "gameinfo.gi")
    
    if os.path.exists(wpath_gameinfo):
        positive_log("Gameinfo найден!")
    else:
        negative_log("Gameinfo не найден. Пожалуйста, убедитесь что gameinfo.gi находится в той же папке что и этот скрипт и перезапустите скрипт.")
        input("[~] Нажмите Enter чтобы закрыть окно.")
        os._exit(0)

def process_mod_directories(dota_directory):
    """
    Работа с папками для мода.
    """
    neutral_log("Работа с папками для мода...")
    
    if os.path.exists(f"{dota_directory}\\Dota2SkinChanger"):
        neutral_log("Найдена существующая папка Dota2SkinChanger. Производится очистка...")
        entries = os.listdir(f"{dota_directory}\\Dota2SkinChanger")
        
        for entry in entries:
            entry_path = os.path.join(f"{dota_directory}\\Dota2SkinChanger", entry)
            
            if os.path.isfile(entry_path):
                os.remove(entry_path)
                print(f"[+] {entry_path} удален")
            elif os.path.isdir(entry_path):
                shutil.rmtree(entry_path)
                print(f"[+] {entry_path} удален")
    else:
        os.makedirs(f"{dir}\\Dota2SkinChanger", exist_ok=True)
        positive_log(f"Папка Dota2SkinChanger создана в {dota_directory}.")

def copy_mod_files(working_directory, dota_directory):
    """
    Перемещение файлов мода в соответствующие папки.
    """
    neutral_log("Работа с файлами мода...")
    working_path = os.path.normpath(working_directory)
    shutil.copy(f"{working_path}\\pak01_dir.vpk", f"{dota_directory}\\Dota2SkinChanger")
    positive_log("pak01_dir.vpk установлен")
    gameinfo_destination = f"{dota_directory}\\dota\\gameinfo.gi"
    gameinfo_branchspecific_destination = f"{dota_directory}\\dota\\gameinfo_branchspecific.gi"
    if os.path.exists(gameinfo_destination):
        os.remove(gameinfo_destination)
    if os.path.exists(gameinfo_branchspecific_destination):
        os.remove(gameinfo_branchspecific_destination)
    shutil.copy(f"{working_path}\\gameinfo.gi", f"{dota_directory}\\dota")
    shutil.copy(f"{working_path}\\gameinfo_branchspecific.gi", f"{dota_directory}\\dota")
    positive_log("gameinfo.gi заменен в файлах игры")

def automatic_bug_report(bot_token, chat_id, path):
    """
    Автоматический баг репорт в Telegram бота.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    with open(path, "rb") as document:
        files = {"document": document}
        data = {"chat_id": chat_id}
        response = requests.post(url, data=data, files=files)
    return response

def initialize_user_scripts(folder_path: str):
    """
    Простая реализация пользовательских скриптов.
    """
    if not os.path.exists(folder_path):
        #print(f"[~] Папка {folder_path} не найдена. Работа скрипта продолжается без пользовательских скриптов.")
        pass
        return
    
    files = os.listdir(folder_path)
    py_files = [file for file in files if file.endswith(".py")]

    if not py_files:
        negative_log(f"В папке {folder_path} не найдено пользовательских скриптов.")
        return
    
    for py_file in py_files:
        script_path = os.path.join(folder_path, py_file)
        module_name = os.path.splitext(py_file)[0]

        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            module.main()
        else:
            negative_log(f"Функция main не найдена в скрипте {py_file}")

def main():
    """
    Функция, инициализирующая все остальные.
    """
    init()

    os.system(f"title Dota2VPKLoader {current_version} / Created by https://t.me/qqqwwqwwwwwe / https://github.com/qqqwwqeeqqwe")

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
    
    print("\n[*] Инструкция по использованию: https://github.com/qqqwwqeeqqwe/Dota2VPKLoader\n")

    # Hooks
    check_for_updates(current_version, "https://raw.githubusercontent.com/qqqwwqeeqqwe/Dota2VPKLoader/main/version")

    dota_directory = find_dota_directory()
    if dota_directory is None:
        negative_log("Скрипту не удалось автоматически найти путь к файлам игры Dota 2. Пожалуйста, введите путь вручную.")
        dota_directory = input("[~] Введите путь к файлам игры Dota 2: ")
    else:
        positive_log("Папка Dota 2 найдена!")
        pass

    initialize_user_scripts("Scripts")
    check_mod_files(os.getcwd())
    process_mod_directories(dota_directory)
    copy_mod_files(os.getcwd(), dota_directory)

    positive_log("Установка мода успешно завершена! Приятной игры <3")
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
            f.close()

    automatic_bug_report("5795495484:AAEcA4RThUWu-srVFXcxV_JfJZYgaWSWL8c", "1201313345", filename)

    negative_log("Во время выполнения программы возникла ошибка. Отчет об ошибке был автоматически отправлен через Telegram-бота.")
    input("[~] Нажмите Enter чтобы закрыть окно.")
    os._exit(0)
