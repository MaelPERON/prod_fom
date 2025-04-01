import bpy
from bpy.path import display_name_from_filepath
from pathlib import Path

def get_collection(string):
    list = [coll for coll in bpy.data.collections if string in coll.name]
    return None if len(list) < 1 else list[0]

def get_objs(objs):
    return [obj for obj in objs if obj.type == "MESH"]

def set_mesh_name(obj):
    obj.data.name = obj.name

def is_asset(filepath):
    return len(filepath.split("02_PROD\\assets")) >= 1

def obj_to_json(obj):
    new_obj = {}
    for attr in dir(obj):
        if attr.startswith("__") or attr.startswith("bl_"): continue
        value = getattr(obj, attr, None)
        id_data = getattr(value, "id_data", None)
        # print(attr, value, id_data)
        new_obj[attr] = value if id_data is None else None
    return new_obj

def get_work_dir(filepath):
    return Path(filepath).parent

def refresh_areas(areas=None):
    areas = areas or bpy.context.screen.areas
    for area in areas:
        if area.type == "VIEW_3D":
            area.tag_redraw()