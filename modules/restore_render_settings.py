import bpy
import json
import os

def set_render_settings(root, prop, value):
    if type(value) == dict:
        for k, v in value.items():
            if (new_root := getattr(root, prop, None)) is not None:
                set_render_settings(new_root, k, v)
    else:
        if hasattr(root, prop):
            setattr(root, prop, value)
            print(f"Set render setting '{prop}' to '{value}'.")
        else:
            print(f"Property '{prop}' not found in render settings.")

def restore_render_settings_from_json(json_file_path):
    """
    Restore all the scene render settings from the JSON object.
    
    Args:
        json_file_path (str): Path to the JSON file containing render settings.
    """
    try:
        with open(json_file_path, 'r') as file:
            render_settings = json.load(file)

            for setting, value in render_settings.items():
                set_render_settings(bpy.context.scene.render, setting, value)
    except Exception as e:
        print(f"Error restoring render settings: {e}")

# json_path = os.path.join("G:/Mon Drive/Maël PERON/3D/Blender/Assets/ADDONS/Dev/prod_fom/json/render_settings.json")
# restore_render_settings_from_json(json_path)