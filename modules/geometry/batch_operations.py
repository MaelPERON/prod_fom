import bpy

def remove_modifier(obj, types = []) -> None:
    for mod in obj.modifiers:
        if mod.type in types:
            print(f"Removed {mod.name} ({mod.type}) modifier from {obj.name}")
            obj.modifiers.remove(mod)


for obj in bpy.context.selected_objects:
    remove_modifier(obj, types=["MESH_SEQUENCE_CACHE"])