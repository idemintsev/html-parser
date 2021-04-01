#!/usr/bin/env python3
import argparse
import os
import re

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit('Установите библиотеку beautifulsoup4==4.9.3')


class HtmlFileParser:
    """
    Use Python3.8
    Парсер для HTML-файлов.
    Достает из HTML-файла Имя, Фамилию, Отчество. ФИО должны быть написаны латиницей или кириллицей.
    Результаты парсинга выводит на консоль.

    В качестве параметров принимает:
    filename - полное имя файла (вместе с расширением <filename.html>). Обязательный параметр.
    path_to_file - путь к HTML-файлу. Можно не указывать, если HTML-файл находится в тойже директории, что и parser.py
    """

    def __init__(self, filename: str, path_to_file=None):
        self.filename = filename
        if path_to_file is None:
            self.path_to_file = os.path.join(os.path.dirname(__file__), self.filename)
        else:
            self.path_to_file = os.path.join(os.path.abspath(path_to_file), self.filename)
        self.re_tags = re.compile(r'(.*<p class=\"full_name\">[\sa-zA-ZА-Яа-яЁё+-]+<\/p>.*)')
        self.fullname_pattern = re.compile(r'[\sa-zA-ZА-Яа-яЁё+-]+')

    def check_file_format(self) -> bool:
        """
        Проверяет имеет ли файл для парсинга расширение html.
        :return: False or True
        """
        if self.filename.endswith('.html'):
            return True
        print('Неизвестный формат файла. Файл должен иметь расширение "html".')
        return False

    def read_file(self):
        try:
            with open(self.path_to_file) as file:
                for line in file:
                    yield line
        except FileNotFoundError as exc:
            print('Не удалось открыть файл.\nОшибка в имени файла или директории!')

    def find_tags_with_full_name(self, line: str) -> str:
        """
        Ищет строки, соответствующие регулярному выражению, описанному в self.re_tags и достает из них текст.
        :param line: строка из распарсиваемого html-файла
        :return: строку, соответствующую self.re_tags
        """
        match = re.match(self.re_tags, line)
        if match:
            tags_parser = BeautifulSoup(line, 'html.parser')
            full_name = tags_parser.get_text()
            full_name = ' '.join(full_name.split())
            return full_name

    def format_full_name(self, full_name: str) -> list:
        """
        Проверяет не пустая ли строка. Если строка содержит ФИО, то преобразует ее к списку.
        :param full_name:
        :return: ['', '', '',] или ['', '',] или ['',]
        """
        unformated_full_name = full_name
        if len(unformated_full_name) > 0:
            full_name = [elem for elem in unformated_full_name.split()]
            return full_name

    def check_and_print_result(self, full_name: list):
        """
        Выводит на консоль результаты парсинга.
        """
        if not full_name is None:
            if len(full_name) == 3:
                surname, name1, name2 = full_name
                result = 'Ура! Мы нашли фамилию: {surname}, имя: {name1}, отчество: {name2}!'.format(
                    surname=surname, name1=name1, name2=name2)
            elif len(full_name) == 2:
                surname, name, = full_name
                result = 'Ура! Мы нашли фамилию: {surname}, имя: {name}: !'.format(surname=surname, name=name)
            elif len(full_name) == 1:
                result = 'Ура! Мы нашли имя: {surname}!'.format(surname=full_name[0])
            else:
                result = 'Упс! Кажется что-то слишком сложное'
            print(result)

    def start(self):
        if self.check_file_format():
            file = self.read_file()
            for line in file:
                full_name = self.find_tags_with_full_name(line)
                if full_name:
                    formated_full_name = self.format_full_name(full_name)
                    self.check_and_print_result(formated_full_name)


if __name__ == '__main__':
    parser_console = argparse.ArgumentParser(description='Запускае парсер HTML-файлов')
    parser_console.add_argument(
        type=str, dest='filename', help='Название HTML файла. Например test.html.'
    )
    parser_console.add_argument(
        '--dirname', type=str, default=None, dest='dirname',
        help='Путь к файлу. Параметр можно не указывать, если HTML-файл находится в той же директории, '
             'что и запускаемый модуль.'
    )

    data_from_console = parser_console.parse_args()
    html_parser = HtmlFileParser(filename=data_from_console.filename, path_to_file=data_from_console.dirname)
    html_parser.start()
