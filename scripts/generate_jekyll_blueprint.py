import yaml
import os
from os import listdir
from os.path import isfile, join
import shutil
from itertools import cycle, islice
from datetime import datetime, timedelta
import io


def clear_previous_generated_folder(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


root_data = '_data'
path_authors = 'authors'
path_titles = '_titles'
path_posts = '_posts'
dummy_date_for_draw_posts = '1970-01-01'

clear_previous_generated_folder(path_authors)
clear_previous_generated_folder(path_titles)
clear_previous_generated_folder(path_posts)


def is_published(title):
    return "publication-date" in title


def is_not_published(title):
    return "publication-date" not in title


def is_social_network_candidate(title):
    fragments = title['fragments'] if "fragments" in title else []
    any_fragment_released = any("social-network-candidate" in fragment for fragment in fragments)
    return "social-network-candidate" in title or any_fragment_released


def generate_author(author):
    id_author = author['id']
    author_name = author['name']
    if 'image' in author:
        author_image = author['image']['name']
    else:
        author_image = ''
    os.mkdir(path_authors + '/' + id_author)
    contents = """---
title_page_full: """ + author_name + """  
title_author_image: """ + author_image + """ 
pagination:
  enabled: true
  category: """ + id_author + """
---"""
    with io.open(path_authors + '/' + id_author + '/paginated.html', mode='w', encoding='utf-8') as text_file:
        text_file.write(contents.encode('utf-8').decode('utf-8'))


def generate_title_pages(author):
    if author['category'] == 'image':
        return

    titles = author['titles']
    for title in titles:
        if is_published(title):
            id_title = title['id']
            contents = '---\ntitle_id: ' + id_title + '\n---'
            with io.open(path_titles + '/' + id_title + '.md', mode='w', encoding='utf-8') as text_file:
                text_file.write(contents.encode('utf-8').decode('utf-8'))


def generate_post(title, author_category, author_id,
                  only_social_network_candidate=False,
                  only_no_published=False,
                  only_first_fragment=False):
    if only_no_published:
        valid = is_not_published(title)
    elif only_social_network_candidate:
        valid = is_social_network_candidate(title)
    else:
        valid = is_published(title)
    if valid:
        id_title = title['id']
        fragments = title['fragments'] if "fragments" in title else []

        if not fragments:
            contents = """---
title_id: """ + id_title + """
categories: [""" + author_category + """, """ + author_id + """]
---"""
            if 'publication-date' in title:
                file_post_name = path_posts + '/' + title[
                    'publication-date'] + '-' + author_category + '-' + id_title + '.md'
            else:
                file_post_name = path_posts + '/' + dummy_date_for_draw_posts + '-' + author_category + '-' + id_title + '.md'

            with io.open(file_post_name, mode='w', encoding='utf-8') as text_file:
                text_file.write(contents.encode('utf-8').decode('utf-8'))
        else:
            if only_first_fragment:
                _fragments = fragments[0:1]
                if 'publication-date' in title:
                    _fragments[0]['publication-date'] = title['publication-date']
                else:
                    _fragments[0]['publication-date'] = dummy_date_for_draw_posts
            else:
                _fragments = fragments
            for fragment in _fragments:
                if only_no_published:
                    invalid = "publication-date" in title
                elif only_social_network_candidate:
                    invalid = "social-network-candidate" not in fragment
                else:
                    invalid = "publication-date" not in title

                if invalid:
                    continue
                fragment_number = fragment['number']
                contents = """---
title_id: """ + id_title + """
fragment: """ + fragment_number + """
categories: [""" + author_category + """, """ + author_id + """]
---"""
                if "publication-date" in fragment:
                    file_post_name = path_posts + '/' + fragment[
                        'publication-date'] + '-' + author_category + '-' + id_title + '-' + fragment['number'] + '.md'
                else:
                    file_post_name = path_posts + '/' + dummy_date_for_draw_posts + '-' + author_category + '-' + \
                                     fragment['number'] + '-' + id_title + '.md'

                with io.open(file_post_name, mode='w', encoding='utf-8') as text_file:
                    text_file.write(contents.encode('utf-8').decode('utf-8'))


def roundrobin(*iterables):
    "roundrobin('ABC', 'D', 'EF') --> A D E B F C"
    # Recipe credited to George Sakkis
    pending = len(iterables)
    nexts = cycle(iter(it).next for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))


file_names = [f for f in listdir(root_data) if isfile(join(root_data, f)) and f != ".DS_Store"]
contents = [open(root_data + '/' + file_name, 'r').read() for file_name in file_names]
authors = [yaml.load(content)[0] for content in contents]

for author in authors:
    generate_author(author)
    generate_title_pages(author)

    author_id = author['id']
    author_category = author['category']
    titles = author['titles']

    for title in titles:
        generate_post(title, 'author', author_id, only_first_fragment=False)
        generate_post(title, author_category, author_id, only_first_fragment=True)
        generate_post(title, 'draw', author_id, only_no_published=True, only_first_fragment=True)
        generate_post(title, 'social-network-candidate', author_id, only_social_network_candidate=True)


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


they_titles = [f for f in listdir(path_posts) if "-they-" in f]
they_titles.sort(reverse=True)
they_titles = list(f7([f.split("-")[-1].replace('.md', '') for f in they_titles]))

our_titles = [f for f in listdir(path_posts) if "-we-" in f]
our_titles.sort(reverse=True)
our_titles = list(f7([f.split("-")[-1].replace('.md', '') for f in our_titles]))

all_home_titles = []

for i in range(len(they_titles)):
    all_home_titles.append(they_titles[i])
    if i < len(our_titles):
        all_home_titles.append(our_titles[i])

d = datetime.today()

for home_title in all_home_titles:
    for author in authors:
        for title in author['titles']:
            if title['id'] == home_title:
                title['publication-date'] = d.strftime('%Y-%m-%d')
                d = d - timedelta(days=1)
                generate_post(title, 'home', author['id'], only_first_fragment=True)
