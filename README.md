# OleTube
## Установка
1. Клонировать репозиторий:

git clone https://github.com/OleGriG/OleTube.git

2. Установить виртуальное окружение для проекта:

python -m venv venv

3. Активировать виртуальное окружение для проекта:
- для OS Lunix и MacOS

source venv/bin/activate

- для OS Windows

source venv/Scripts/activate

4. Установить зависимости:

python3 -m pip install --upgrade pip
pip install -r requirements.txt

5. Выполнить миграции на уровне проекта:

python3 manage.py makemigrations
python3 manage.py migrate

6. Запустить проект:

python manage.py runserver.

## Автор: Григорьев Олег Андреевич
