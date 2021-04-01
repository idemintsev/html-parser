# html-parser
Простой парсер для html-файлов с консольным интерфейсом

Достает из HTML-файла Имя, Фамилию, Отчество. ФИО должны быть написаны латиницей или кириллицей.
ФИО содержится только в теге <p class="full_name">ФИО<\/p>
Если внутри тега находится 3 слова  — считаем, что это Фамилия, Имя, Отчество.
2 слова — это Фамилия, Имя.
1 слово — это Имя.
Если внутри тега находится 4 и более слов — считаем, что это что-то сложное и непонятное, что не поддаётся автоматической обработке, и пишем предупреждение.

Результаты парсинга выводит на консоль.
В качестве параметров принимает:
filename - полное имя файла (вместе с расширением <filename.html>). Обязательный параметр.
path_to_file - путь к HTML-файлу. Можно не указывать, если HTML-файл находится в тойже директории, что и parser.py

Запускается из терминала: ./parser.py <filename.html>
Более подробная информация ./parser.py --h
