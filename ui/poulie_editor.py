import bpy

class POULIE_PT_Panel(bpy.types.Panel):
    bl_label = "Poulie Editor"
    bl_idname = "POULIE_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    @classmethod
    def poll(self, context):
        return context.active_object and context.active_object.name.startswith("RIG-poulie") and context.active_object.type == "ARMATURE"

    def draw(self, context):
        poulie = context.active_object
        layout = self.layout
        layout.label(text="Poulie Editor Panel")

        root_bone = poulie.pose.bones.get("root")
        if root_bone is None:
            return
        
        layout.label(text="Animation")
        row = layout.row()
        row.prop(root_bone, '["animated"]', toggle=True)
        row.prop(root_bone, '["frame"]')

        layout.label(text="Display")
        row = layout.row()
        row.prop(root_bone, '["show_all"]', toggle=True)
        row = layout.row(align=True)
        row.prop(root_bone, '["shirt"]', icon="MATCLOTH")
        row.prop(root_bone, '["pant"]', icon="POSE_HLT")
        row = layout.row(align=True)
        row.prop(root_bone, '["helmet"]', icon="ARMATURE_DATA")
        row.prop(root_bone, '["helmet_pos"]', icon="ARMATURE_DATA")