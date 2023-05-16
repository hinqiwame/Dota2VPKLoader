# В этом примере скрипт будет скачивать мод прямо после нахождения папки Dota 2.
import requests  # Импортируем библиотеку requests для работы с HTTP запросами
import sys
sys.path.append("..")  # Перемещаемся на уровень ниже чтобы можно было взаимодействовать с основным скриптом
from Dota2VPKLoader import *  # Импортируем все функции из основного скрипта

def main():  # Определяем главную функцию
    # Отправляем HTTP запрос для получения файла по указанному URL
    response = requests.get("https://raw.githubusercontent.com/meth1337/Dota2VPKLoader/main/src/Dota2VPKLoaderScriptSDK/pak01_dir.vpk", stream=True)
    response.raise_for_status()  # Проверяем статус ответа сервера

    # Открываем файл с указанным именем для записи в двоичном режиме
    with open("pak01_dir.vpk", "wb") as f:
        # Читаем содержимое ответа сервера по частям (chunks)
        for chunk in response.iter_content(chunk_size=8192):
            # Если chunk не пустой, записываем его в файл
            if chunk:
                f.write(chunk)
    
    # Выводим сообщение о успешной загрузке файла
    positive_log("Мод с сервера установлен!")