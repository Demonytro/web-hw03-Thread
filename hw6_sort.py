# python-hw6-sort - Домашнее задание 6 
# Скрипт должен проходить по указанной во время вызова папке и сортировать все файлы по группам

# web-hw03-Thread
#

import os
from pathlib import Path
import sys
# import shutil
import string
import re
from zipfile import ZipFile


import argparse
# from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging




name_folders = {
    'images': ('.jpeg', '.png', '.jpg', '.svg'),
    'video': ('.avi', '.mp4', '.mov', '.mkv'),
    'documents': ('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'),
    'audio': ('.mp3', '.ogg', '.wav', '.amr'),
    'archives': ('.zip', '.gz', '.tar'),
    'unknown': None
}

count_dub = 0

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
            if len(string) > index+1:
                if string[index+1] not in lower_case_letters.keys():
                    char = char.upper()
            else:
                char = char.upper()
        if not re.search('[a-z A-Z0-9]', char):
            char = '-'
        translit_string += char

    return translit_string


def sort_folder(path_folder):

    list_path_subfolder = list(path_folder.iterdir())
    if not list_path_subfolder:
        return 
    else:
        for file_folder in list_path_subfolder:
            if file_folder.is_dir():
                sort_folder(file_folder)
            else:
                sort_files(file_folder)
    return


def sort_files(path_file):

    name, ext = path_file.stem, path_file.suffix
    global count_dub
    count_dub += 1

    if ext in name_folders['images']:
        new_path = os.path.join(path_start_folder, 'images')
        
    elif ext in name_folders['video']:
        new_path = os.path.join(path_start_folder, 'video')

    elif ext in name_folders['documents']:
        new_path = os.path.join(path_start_folder, 'documents')

    elif ext in name_folders['audio']:
        new_path = os.path.join(path_start_folder, 'audio')

    elif ext in name_folders['archives']:
        new_path = Path(os.path.join(path_start_folder, 'archives'))
        with ZipFile(path_file, 'r') as zObject:
            zObject.extractall(new_path)
        # shutil.unpack_archive(path_file, extract_dir)
        # new_path = os.path.join(path_start_folder, 'archives')
        # os.remove (path_file)

    else:
        new_path = os.path.join(path_start_folder, 'unknown')

    norma_name = normalize(name)

    new_name = f'{norma_name}{ext}'
    new_path_name = os.path.join(new_path, new_name)

    try:
        path_file.rename(new_path_name)
    except:
        new_name = f'{norma_name}_{count_dub}{ext}'
        new_path_name = Path(os.path.join(new_path, new_name))
        path_file.rename(new_path_name)


# ---------------------------------------------------------------------------


if __name__ == '__main__':


path_start_folder = Path(sys.argv[-1])

list_path_first = list(path_start_folder.iterdir())

for new_folder in name_folders:
    path_new_dir = os.path.join(path_start_folder, new_folder)
    if not os.path.exists(path_new_dir):
        os.makedirs(path_new_dir)
    else:
        print('don\'t make up folder', path_new_dir)

for any_path in list_path_first:
    
    if any_path.is_dir():
        sort_folder(any_path)
        if any_path.name in name_folders:
            continue
        else:
            shutil.rmtree(any_path)
    else:
        sort_files(any_path)

list_sort_done = list(path_start_folder.iterdir())
print('Sort done!\n', list_sort_done)
