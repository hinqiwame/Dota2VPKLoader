# Пример использования функций из основного скрипта
import sys
sys.append("..")  # Перемещаемся на уровень ниже чтобы можно было взаимодействовать с основным скриптом
from Dota2VPKLoader import *  # Импортируем все функции из основного скрипта

print(get_latest_version("https://raw.githubusercontent.com/meth1337/Dota2VPKLoader/main/version"))  # Вывод последней версии Dota2VPKLoader

# Результат:
# 0.0.5 (Пример)
