# VoteMapper

Рабочая директория:

    $ mkdir votemapper
    $ cd votemapper

Создаем окружение vitrualenv:

    $ virtualenv --no-site-packages env
    $ source env/bin/activate

Устанавливаем пакет в режиме разработки:

    $ git clone git@github.com:nextgis/votemapper.git
    $ pip install -e votemapper

Загружаем тестовые данные по выборам в ГосДуму 2011 года в Москве:

    $ git clone git@github.com:nextgis/vm-2011-moscow-duma.git
    $ mkdir output
    $ votemapper vm-2011-moscow-duma/config.yaml output

В результате в директории output окажется набор статических файлов с
интерактивной веб-картой. Приблизительный результат можно посмотреть
[тут](http://nextgis.github.io/vm-2011-moscow-duma/).