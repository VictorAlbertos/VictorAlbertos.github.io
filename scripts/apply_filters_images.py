from PIL import Image
from PIL import ImageEnhance
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
root_img_originals = 'img_originals'
root_assets_images = 'assets/img'
clear_previous_generated_folder(root_assets_images)

file_names = [f for f in listdir(root_data) if isfile(join(root_data, f)) and f != ".DS_Store"]
contents = [open(root_data + '/' + file_name, 'r').read() for file_name in file_names]
authors = [yaml.load(content)[0] for content in contents]

images_authors = []
images_titles = []
for author in authors:
    if "image" in author:
        images_authors.append(author['image'])

    for title in author['titles']:
        if "image" in title:
            if author['category'] == 'punctum':
                title['image']['keep_original'] = True
            images_titles.append(title['image'])

source = root_img_originals + '/authors/'
files = os.listdir(source)
for f in files:
    if f != ".DS_Store":
        shutil.move(source + f, root_img_originals)

source = root_img_originals + '/titles/'
files = os.listdir(source)
for f in files:
    if f != ".DS_Store":
        shutil.move(source + f, root_img_originals)

source = root_img_originals + '/punctum/'
files = os.listdir(source)
for f in files:
    if f != ".DS_Store":
        shutil.move(source + f, root_img_originals)

all_images = images_authors + images_titles
all_images_names = [f for f in listdir(root_img_originals) if
                    isfile(join(root_img_originals, f)) and f != ".DS_Store"]
for image_name in all_images_names:
    candidates = [image for image in all_images if image['name'] == image_name]
    if candidates:
        image_properties = candidates[0]
        original = Image.open(root_img_originals + '/' + image_name).convert('RGB')
        updated = Image.open(root_img_originals + '/' + image_name).convert('RGB')

        if 'color' in image_properties:
            updated = ImageEnhance.Color(updated).enhance(float(image_properties['color']))
        if 'contrast' in image_properties:
            updated = ImageEnhance.Contrast(updated).enhance(float(image_properties['contrast']))

        updated.save(root_assets_images + '/' + image_name)
        if 'keep_original' in image_properties:
            original.save(root_assets_images + '/original_' + image_name)

Image.open(root_img_originals + '/' + 'favicon.ico').save(root_assets_images + '/' + 'favicon.ico')
Image.open(root_img_originals + '/' + 'title_image.jpeg').save(root_assets_images + '/' + 'title_image.jpeg')
