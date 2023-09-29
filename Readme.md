**Инструкция по запуску docker-compose**
1) Склонировать репозиторий
2) Перейти в корневую директорию проекта
3) Выполнить команду `docker-compose up`
> Для проверки работы ПО можно воспользоваться Postman, Insomnia или же отправлять запросы через Swagger 
>> Swagger документация доступна по адресу [http://localhost:6969/apidocs]
 
---
**Инструкция по запуску из среды разработки**
> Внимание! Проект сконфигурирован для запуска через docker-compose, возможны проблемы с локальным запуском
1) В config.yaml указать актуальную конфигурацию
2) Запустить redis и postges
3) Для создания таблиц в БД `alembic upgrade head`
4) Установить переменную окружения CONFIG_PATH={absolute_path_to_config.yaml}, например
CONFIG_PATH=/home/user/Documents/testProjectUrbantech/config.yaml
5) Установить библиотеки из requirements.txt
6) Запустить rest_app, data_saver и image_handler