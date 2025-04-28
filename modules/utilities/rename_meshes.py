import bpy
import re

def get_name(name):
    return re.sub(r"(_low|_high)", r"", name)

for obj in bpy.context.selected_objects:
    new_name = get_name(obj.name)
    # if re.search(r"_high", obj.name) is not None:
    #     if (mesh := bpy.data.meshes.get(new_name)) is None:
    #         print(f"{new_name} not found in meshes")
    #         continue

    #     obj.data = mesh
    #     print(f"{obj.name} -> {obj.data.name}")
    #     continue

    if obj.type == "MESH":
        old_name = obj.data.name
        obj.data.name = new_name
        print(f"{old_name} -> {obj.data.name}")
        
    else:
        print(f"{obj.name} is not a mesh")