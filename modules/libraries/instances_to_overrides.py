import bpy
from bpy import types

def instance_to_override(obj: types.Object):
    master_collection = next((coll for coll in bpy.data.collections if obj.name in coll.objects), None)
    collection = obj.instance_collection
    override_collection = collection.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer, do_fully_editable=True)
    if not override_collection:
        print(f"Failed to create override for {obj.name}")
        return
    
    rig = next((o for o in override_collection.all_objects if o.type == "ARMATURE"), None)
    if not rig:
        print(f"No rig found in {override_collection.name}")
        return
    
    master_collection.children.link(override_collection)
    
    root_bone = next((b for b in rig.pose.bones if b.name.lower() == "root"), None)
    root_bone.matrix = obj.matrix_world # Assuming the z root bone axis is point upward

    obj.hide_set(True)
    obj.hide_render = True
    print(f"Instanced {obj.name}")
    return

for obj in bpy.context.selected_objects:
    if obj.type == "EMPTY" and obj.instance_type == "COLLECTION":
        instance_to_override(obj)