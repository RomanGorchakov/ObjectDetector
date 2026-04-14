import os


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_image_files(folder):
    return [
        f for f in os.listdir(folder)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))
    ]
