# 			---
#
#
#
#
#
#
#
# generate:post
# if category == image
# 	---
# 	title: Vue de village
# 	title_id: vue_de_village
# 	categories: [image, maurice_vlaminck]
# 	---
#
#
#
#
# if category != image
# 	generate_title

import yaml
import os
from os import listdir
from os.path import isfile, join
import shutil


def load_authors_json():
    root_path = '_data'
    file_names = [f for f in listdir(root_path) if isfile(join(root_path, f)) and f != ".DS_Store"]
    contents = [open(f'{root_path}/{file_name}', 'r').read() for file_name in file_names]
    return [yaml.load(content)[0] for content in contents]


def clear_previous_generated_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


path_authors = 'authors'
path_titles = '_titles'

clear_previous_generated_folder(path_authors)
clear_previous_generated_folder(path_titles)


def generate_author(author):
    id_author = author['id']
    os.mkdir(f'{path_authors}/{id_author}')
    contents = f"""---
pagination:
  enabled: true
  category: """ + id_author + """
---"""
    with open(f'{path_authors}/{id_author}/paginated.html', "w") as text_file:
        text_file.write(contents)


def generate_title_page(author):
    if author['category'] == 'image':
        return

    titles = author['titles']

    for title in titles:
        id_title = title['id']
        contents = f'---\ntitle_id: {id_title}\n---'
        with open(f'{path_titles}/{id_title}.md', "w") as text_file:
            text_file.write(contents)


authors = load_authors_json()
for author in authors:
    generate_author(author)
    generate_title_page(author)
