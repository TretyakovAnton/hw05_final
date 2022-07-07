<h1> Социальная сеть YaTube</h1>
<h2>Опиание проекта:</h2>
В проекте реализованы следующие функции:

- добавление/удаление постов авторизованными пользователями
- редактирование постов только его автором
- возможность авторизованным пользователям оставлять комментарии к постам
- подписка/отписка на понравившихся авторов
- создание отдельной ленты с постами авторов, на которых подписан пользователь
- создание отдельной ленты постов по группам(тематикам)

Подключены пагинация, кеширование, авторизация пользователя, возможна смена пароля через почту.
Неавторизованному пользователю доступно только чтение.


<h2>Мануал по устновке проекта</h2>

<h4><i>1.Клонировать репозиторий и перейти в него в командной строке:</i></h4>

    git clone https://github.com/TretyakovAnton/hw05_final.git

    cd api_final_yatube

<h4><i>2.Установить виртуальное окружение</i></h4>

    python -m venv venv

<h4><i>3.Запустить виртуальное окружение</i></h4>

    venv\Scripts\activate

<h4><i>4.Установить зависимости из файла requirements.txt:</i></h4>

    python -m pip install --upgrade pip

    pip install -r requirements.txt

<h4><i>5.Выполнить миграции:</i></h4>

    python manage.py migrate

<h4><i>6.Запустить проект:</i></h4>

    python manage.py runserver

<h1>Инструментарий:</h1>

    Django 2.2.16
    Python 3.7
    Django debug toolbar
    SQLite
    Django ORM
    

