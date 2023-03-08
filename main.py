"""
Відсортувати файли в папці.
"""

import argparse
from pathlib import Path
from shutil import copyfile, copy, rmtree
from threading import Thread
import logging
import string
import re
import os

"""
--source [-s] picture
--output [-o]
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []
count_dub = 0


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path) -> None:
    global count_dub
    for el in path.iterdir():
        if el.is_file():
            name_el, ext = el.stem, el.suffix
            # ext = el.suffix[1:]

            new_path = output / ext[1:]
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                el_norma = normalize(name_el)
                norma_name = f'{el_norma}{ext}'
                new_path_norma_name = os.path.join(new_path, norma_name)

                if not os.path.exists(new_path_norma_name):
                    # pass
                    copy(el, new_path_norma_name)

                else:
                    count_dub += 1
                    print(count_dub)
                    new_name = f'{norma_name}_{count_dub}{ext}'
                    new_path_norma_name = os.path.join(new_path, new_name)
                    copy(el, new_path_norma_name)

            except OSError as error:
                logging.error(error)


def normalize(string):
    """ This function works just fine """
    capital_letters = {
        u'А': u'A',
        u'Б': u'B',
        u'В': u'V',
        u'Г': u'G',
        u'Д': u'D',
        u'Е': u'E',
        u'Ё': u'E',
        u'Ж': u'Zh',
        u'З': u'Z',
        u'И': u'I',
        u'Й': u'Y',
        u'К': u'K',
        u'Л': u'L',
        u'М': u'M',
        u'Н': u'N',
        u'О': u'O',
        u'П': u'P',
        u'Р': u'R',
        u'С': u'S',
        u'Т': u'T',
        u'У': u'U',
        u'Ф': u'F',
        u'Х': u'H',
        u'Ц': u'Ts',
        u'Ч': u'Ch',
        u'Ш': u'Sh',
        u'Щ': u'Sch',
        u'Ъ': u'-',
        u'Ы': u'Y',
        u'Ь': u'-',
        u'Э': u'E',
        u'Ю': u'Yu',
        u'Я': u'Ya'
    }

    lower_case_letters = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'e',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'y',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'h',
        u'ц': u'ts',
        u'ч': u'ch',
        u'ш': u'sh',
        u'щ': u'sch',
        u'ъ': u'-',
        u'ы': u'y',
        u'ь': u'-',
        u'э': u'e',
        u'ю': u'yu',
        u'я': u'ya'
    }

    translit_string = ""

    for index, char in enumerate(string):
        if char in lower_case_letters.keys():
            char = lower_case_letters[char]
        elif char in capital_letters.keys():
            char = capital_letters[char]
            if len(string) > index + 1:
                if string[index + 1] not in lower_case_letters.keys():
                    char = char.upper()
            else:
                char = char.upper()
        if not re.search('[a-z A-Z0-9]', char):
            char = '-'
        translit_string += char

    return translit_string


def choice_delete(path: Path) -> None:
    while True:
        choice_del = input('Do you want to delete ( y / n ) >>> ')
        if choice_del == 'y':
            input('Are you sure (ctrl + c)  ')
            rmtree(path)
            break
        else:
            print('See you !')
            break


if __name__ == "__main__":

    logging.basicConfig(level=logging.ERROR, format="%(threadName)s %(message)s")
    print(source, output)
    folders.append(source)
    grabs_folder(source)
    print(folders)
    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]

    print("Можно видалять стару папку якщо треба")

    choice_delete(output)
