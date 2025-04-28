import bpy
from bpy.path import display_name_from_filepath, abspath
from pathlib import Path
import shutil
import re

def get_work_dir(filepath):
    return Path(filepath).parent

def increment_version(version):
    number = int(re.sub(r"(v)?(\d{1,})", r'\2', version))
    return f'v{str(number+1).zfill(3)}'

def increment_filepath(filepath, new_stage="model"):
    args = display_name_from_filepath(filepath).split("-")
    version = args.pop()
    new_version = increment_version(version)
    if len(args) != 4:
        return filepath
    prefix, type, stage, name = args

    return '-'.join([prefix, type, new_stage, name, new_version])

def main():
    filepath = bpy.data.filepath
    work_dir = get_work_dir(filepath)
    new_filepath = work_dir / increment_filepath(filepath, "uv")
    shutil.copyfile(filepath, new_filepath)
    for collection in bpy.data.collections:
        if collection.asset_data is not None:
            collection.asset_clear()
    bpy.ops.wm.open_mainfile(filepath=new_filepath)

# filepath = 'G:\\Mon Drive\\ENSI\\01_E3\\Film 1mn\\02_PROD\\assets\\set_dress\\poteau_cordon\\work\\fom-chara-model-poteau_cordon-v002.blend'
# print(increment_filepath(filepath))
# print(get_work_dir(filepath))

if __name__ == "__main__":
    main()