import tempfile
import os
import shutil

def get_tmp_dir(path)->str:
    temp_dir = tempfile.gettempdir()

    # Define the new directory name
    new_dir_name = "keyfiles"

    # Construct the full path for the new directory
    new_dir_path = os.path.join(temp_dir, new_dir_name, path)

    # Create the new directory
    os.makedirs(new_dir_path, exist_ok=True)

    return new_dir_path

def clean_tmp_dir(path:str)->None:
    if os.path.exists(path):
        shutil.rmtree(path)

def move_directory(src: str, dest: str) -> None:
    shutil.move(src, dest)