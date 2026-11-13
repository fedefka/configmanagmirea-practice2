# Практическая работа №2. Граф зависимостей APK
Капитанов Федор Александрович, ИКБО-62-25, вариант 12.
## Установка и запуск
```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./run.sh
.venv/bin/python -m unittest discover -s tests -v
```
Для запуска нужны Python 3.9+ и PyYAML. Сборка не требуется.
В PyCharm можно запустить `src/main.py` с интерпретатором проекта.
## Настройки
Программа читает `config.yaml`. Другой файл можно передать первым аргументом.
| Поле | Назначение |
| --- | --- |
| `package` | Имя пакета, в тестовом режиме одна буква A-Z |
| `repository` | URL каталога для одной архитектуры Alpine или путь к тестовому файлу |
| `test_mode` | `false` для Alpine, `true` для тестового файла |
| `filter` | Подстрока имени пакета для исключения, пустая строка отключает фильтр |
Путь к тестовому файлу отсчитывается от папки файла YAML.
## Функции
`load_config` читает YAML. `check_fields` проверяет ключи и значения.
`check_url` проверяет URL. `repository_path` вычисляет путь к тестовому файлу.
`main` печатает настройки и возвращает код 1 при ошибке.
## Примеры
```sh
./run.sh
./run.sh examples/test.yaml
```
Для проверки ошибок по очереди укажите `package: "bad name"`,
`repository: "ftp://host"`, `test_mode: "true"` или `filter: 3`.
