# iktin_bot

ТЗ для iktin

## Технологии

Для создания были использованы:
- [Python 3.7.0](https://www.python.org)
- [Aiogram 3.2.0](https://aiogram.dev/)

и многое другое, со списком всех зависимостей можете ознакомиться в файле [requirements.txt](https://github.com/iamksan/iktin_bot/blob/main/requirements.txt)

## Установка

Скопируйте репозиторий в свою папку:
```sh
$git@github.com:iamksan/iktin_bot.git
```

Установите виртуальное окружение:
```sh
$python3 -m venv <myenvname>
```

После установки запустите его:
```sh
$source <myenvname>/scripts/activate
```

Установите зависимости из requirements.txt:
```sh
$pip install -r reqiurements.txt
```

Создайте файлл .env:
```sh
BOT_TOKEN = 6847336274:AAFERQ6A4TsP57R56Jko4OSX6ErFKyZSvFI

ip = localhost:5432
PGUSER = postgres
PGPASSWORD = Miniminiralka1
DATABASE = gino
```

Запустите сервер:
```sh
$python3 bot.py
```


Бот доступен по ссылке https://t.me/iktintest_bot