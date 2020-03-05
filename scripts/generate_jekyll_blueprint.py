import yaml
import os
from os import listdir
from os.path import isfile, join
import shutil


def clear_previous_generated_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


root_data = '_data'
path_authors = 'authors'
path_titles = '_titles'
path_posts = '_posts'

clear_previous_generated_folder(path_authors)
clear_previous_generated_folder(path_titles)
clear_previous_generated_folder(path_posts)


def is_title_ready_to_be_published(title):
    fragments = title['fragments'] if "fragments" in title else []
    any_fragment_released = any("publication-date" in fragment for fragment in fragments)
    return "publication-date" in title or any_fragment_released


def generate_author(author):
    id_author = author['id']
    os.mkdir(f'{path_authors}/{id_author}')
    contents = f'''---
pagination:
  enabled: true
  category: {id_author}
---'''
    with open(f'{path_authors}/{id_author}/paginated.html', "w") as text_file:
        text_file.write(contents)


def generate_title_pages(author):
    if author['category'] == 'image':
        return

    titles = author['titles']
    for title in titles:
        if is_title_ready_to_be_published(title):
            id_title = title['id']
            contents = f'---\ntitle_id: {id_title}\n---'
            with open(f'{path_titles}/{id_title}.md', "w") as text_file:
                text_file.write(contents)


def generate_posts(author):
    author_id = author['id']
    author_category = author['category']
    titles = author['titles']

    for title in titles:
        if not is_title_ready_to_be_published(title):
            continue

        id_title = title['id']
        fragments = title['fragments'] if "fragments" in title else []

        if not fragments:
            contents = f'''---
title_id: {id_title}
categories: [{author_category}, {author_id}]
---'''
            file_post_name = path_posts + '/' + title['publication-date'] + '-' + id_title + '.md'
            with open(file_post_name, "w") as text_file:
                text_file.write(contents)
        else:
            for fragment in fragments:
                if "publication-date" not in fragment:
                    continue
                fragment_number = fragment['number']
                contents = f'''---
title_id: {id_title}
fragment: {fragment_number}
categories: [{author_category}, {author_id}]
---'''
                file_post_name = path_posts + '/' + fragment['publication-date'] + '-' + id_title + '.md'
                with open(file_post_name, "w") as text_file:
                    text_file.write(contents)


file_names = [f for f in listdir(root_data) if isfile(join(root_data, f)) and f != ".DS_Store"]
contents = [open(f'{root_data}/{file_name}', 'r').read() for file_name in file_names]
authors = [yaml.load(content)[0] for content in contents]

for author in authors:
    generate_author(author)
    generate_title_pages(author)
    generate_posts(author)
