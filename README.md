# ERC20 detector

Структура проекта:

- celery_impl: конфигурация селери и задач
- core: конфигурация проекта
- database: содержит реализацию подключения к БД, таблицы, репозитории и миграции
- errors: украл с прошлого проекта реализацию Exceptions (использовалось для FastAPI). Здесь использую только в BaseRepository, однако при любом raise приложение будет падать
- models: содержит pydantic модели
- services: верхний слой, который хранит бизнес-логику
- utils: утильные методы

## Запуск приложения

Для старта приложения необходимо установить зависимости, запустить докер контейнеры с БД и брокером.
```sh
poetry install
docker compose up -d
```
И запустить воркер с планировщиком.
```sh
celery -A src.main.app worker -B
```
Или запустить планировщик вне воркера.
```sh
celery -A src.main.app worker --loglevel=INFO
celery -A src.main.app beat
```
Первый способ для тестирования более предпочителен (далее объяснено почему).

## Работа приложения

Сначала создаётся сервис версий, который собирает все версии из репозиториев гитхаба. Сами репозитории жёстко заданы в core.settings. При парсинге версий вычисляется хеш текущей версии для того, чтобы не добавлять одинаковые реализации под разные версии. Здесь возникает проблема, когда мы отдельно запускаем воркер и планировщик данный сервис срабатывает 2 раза, т.к. находится в модуле main. Я не нашёл как можно решить эту проблему, если мы препроцессим. Возможным решением будет не препроцессить версии, а хранить их в БД, и создать таску, которая будет переодически проверять и добавлять новые версии контрактов.

Далее при запуске задачи создаётся асинхронная сессия, репозитории, сервис и запускается основной метод сервиса. В задаче проверяется появились ли новые необработанные контракты и происходит их обработка. Я так и не смог найти нормального способа парсить solidity код. Нашёл единственную библиотеку, которая практически недокументированна. При проверке стандарта, проверяется есть ли в исходном коде контракта нужные функции. Здесь есть момент с events. Насколько я понял они могут наследоваться из интерфейса и необязательно будут в контракте явно. В общем тут всё зависит от бизнес-требований - в каком виде будут добавляться новые контракты. К сожалений мой код будет соотносить друг с другом полную копию реализации из репозитория (как мне и было сказано), но при необходимости можно поменять метод check_contract_version в классе сервиса если есть точные правила по которым мы относим код контракта к определённой версии.

В приложение есть возможность добавлять новые стандарты путём добавление сервисов и задач. Горизонтальной масштабируемости можно достигнуть путём увелечения кол-ва воркеров и разбития основной задачи по анализу всех доступных контрактов на более мелкие асинхронные подзадачи, где будет анализироваться определённый чанк контрактов.

В среднем приложение на стандартных настройках celery обрабатывает 1 контракт 0.15-0.16 секунды, что составляет около 4_000_000 контрактов в неделю, однако при горизантальном масштабировании я уверен это число можно увеличить.
