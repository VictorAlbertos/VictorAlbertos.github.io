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


# generate_author:
# 	folder_author_name:
# 		paginated.html
# 			---
# 			pagination:
# 			  enabled: true
# 			  category: author_id

path_authors = 'authors'


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


if os.path.isdir(path_authors):
    shutil.rmtree(path_authors)
os.mkdir(path_authors)

authors = load_authors_json()
for author in authors:
    generate_author(author)
