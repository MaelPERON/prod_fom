import bpy
from bpy import types

def instance_obj(context: types.Context, obj: types.Object):
    master_collection = next((coll for coll in context.blend_data.collections if obj.name in coll.objects), None)
    collection = obj.instance_collection
    override_collection = collection.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer, do_fully_editable=True)
    if not override_collection:
        print(f"Failed to create override for {obj.name}")
        return -1
    
    obj.hide_set(True)
    obj.hide_render = True

    rig = next((o for o in override_collection.all_objects if o.type == "ARMATURE"), None)
    if not rig:
        print(f"No rig found in {override_collection.name}")
        return 0

    master_collection.children.link(override_collection)

    root_bone = next((b for b in rig.pose.bones if b.name.lower() == "root"), None)
    root_bone.matrix = obj.matrix_world # Assuming the z root bone axis is point upward

    return 1

class SelectedInstancesToCollectionOverrides(types.Operator):
    bl_idname = "object.selected_instances_to_collection_overrides"
    bl_label = "Selected Instances to Collection Overrides"
    bl_description = "Convert selected instances to collection overrides"
    bl_options = {'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            state = instance_obj(context, obj)
            if state == -1:
                self.report({'ERROR'}, f"Failed to create override for {obj.name}")
                return {'CANCELLED'}
            elif state == 0:
                self.report({'ERROR'}, f"No rig found in {obj.name}")

        self.report({'INFO'}, "Instances converted to collection overrides")
        return {'FINISHED'}