"""Preprocess the Violet model

The model is available for download from
    https://sketchfab.com/3d-models/0c257bf4c4074cdaa05ad2fb55ceadb1

The Python Imaging Library is required
    pip install pillow
"""

from __future__ import print_function

import json
import os
import zipfile

from PIL import Image

from utils.gltf import dump_obj_data

SRC_FILENAME = "violet_arena_of_valor_3d_model.zip"
DST_DIRECTORY = "../assets/violet"

OBJ_FILENAMES = [
    "face.obj",
    "weapon0.obj",
    "weapon1.obj",
    "headstar.obj",
    "bow.obj",
    "hair.obj",
    "skirt.obj",
    "body.obj",
]

IMG_FILENAMES = {
    "textures/1118_SunShangXiang_body_VeryHigh.002_baseColor.png": "body_diffuse.tga",
    "textures/1118_SunShangXiang_face_VeryHigh.002_baseColor.png": "face_diffuse.tga",
    "textures/1118_SunShangXiang_hair_VeryHigh.002_baseColor.png": "hair_diffuse.tga",
    "textures/1118_SunShangXiang_Weapon.002_baseColor.png": "weapon_diffuse.tga",
}


def process_meshes(zip_file):
    gltf = json.loads(zip_file.read("scene.gltf"))
    buffer = zip_file.read("scene.bin")

    for mesh_index, filename in enumerate(OBJ_FILENAMES):
        if filename:
            obj_data = dump_obj_data(gltf, buffer, mesh_index)
            filepath = os.path.join(DST_DIRECTORY, filename)
            with open(filepath, "w") as f:
                f.write(obj_data)


def load_image(zip_file, filename):
    with zip_file.open(filename) as f:
        image = Image.open(f)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        return image


def save_image(image, filename, size=512):
    if max(image.size) > size:
        image = image.resize((size, size), Image.LANCZOS)
    filepath = os.path.join(DST_DIRECTORY, filename)
    image.save(filepath, rle=True)


def process_images(zip_file):
    for old_filename, tga_filename in IMG_FILENAMES.items():
        image = load_image(zip_file, old_filename)
        save_image(image, tga_filename)


def main():
    if not os.path.exists(DST_DIRECTORY):
        os.makedirs(DST_DIRECTORY)

    with zipfile.ZipFile(SRC_FILENAME) as zip_file:
        process_meshes(zip_file)
        process_images(zip_file)


if __name__ == "__main__":
    main()
