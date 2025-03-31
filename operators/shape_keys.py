import bpy


class ReverseUVShapeKeyOperator(bpy.types.Operator):
    bl_idname = "object.reverse_uv_shape_key"
    bl_label = "Reverse UV Shape Key"
    bl_description = "Reverse the UV shape key of the UV_Mesh object"
    bl_options = {'REGISTER', 'UNDO'}

    toggle: bpy.props.BoolProperty(default=True)
    value: bpy.props.BoolProperty(default=True)

    def execute(self, context):
        obj = context.scene.objects.get("UV_Mesh")
        if not obj:
            self.report({'ERROR'}, "UV_Mesh object not found")
            return {'CANCELLED'}
        
        shape_key = obj.data.shape_keys.key_blocks.get("uv")
        if not shape_key:
            self.report({'ERROR'}, "UV shape key not found")
            return {'CANCELLED'}
        
        shape_key.value = 1 - shape_key.value if self.toggle else self.value
        return {'FINISHED'}

class DisableNodesModifierOperator(bpy.types.Operator):
    bl_idname = "object.disable_nodes_modifier"
    bl_label = "Disable NODES Modifier"
    bl_description = "Disable the NODES modifier from the object Vert.001"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.scene.objects.get("Vert.001")
        if not obj:
            self.report({'ERROR'}, "Object 'Vert.001' not found")
            return {'CANCELLED'}
        
        modifier = obj.modifiers.get("NODES")
        if not modifier:
            self.report({'ERROR'}, "NODES modifier not found on 'Vert.001'")
            return {'CANCELLED'}
        
        modifier.show_viewport = not modifier.show_viewport
        modifier.show_in_editmode = not modifier.show_in_editmode
        self.report({'INFO'}, "NODES modifier disabled")
        return {'FINISHED'}

class ReloadDeformedClothOperator(bpy.types.Operator):
    bl_idname = "object.reload_deformed_cloth"
    bl_label = "Reload Deformed Cloth"
    bl_description = "Reload the deformed cloth simulation for the object Cloth"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.scene.objects.get("Vert.001")
        target = context.scene.objects.get("UV_Mesh")
        if not obj or not target:
            self.report({'ERROR'}, f"obj: {obj} | target: {target}")
            return {'CANCELLED'}
        
        surf = obj.modifiers.get("SURF")
        if not surf.is_bound:
            self.report({"ERROR"}, "Not bound.")
            return {"CANCELLED"}

        mode = context.mode
        shape_key = target.data.shape_keys.key_blocks.get("uv")
        if not shape_key:
            self.report({"ERROR"}, "No shape key")
            return {"CANCELLED"}
        value = shape_key.value
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.reverse_uv_shape_key(toggle=False,value=True)
        bpy.ops.object.surfacedeform_bind(modifier=surf.name)

        bpy.ops.object.surfacedeform_bind(modifier=surf.name)
        if not value:
            bpy.ops.object.reverse_uv_shape_key(toggle=False,value=False)
        if mode == "EDIT_MESH": bpy.ops.object.mode_set(mode="EDIT")

        return {'FINISHED'}
    
class SetVisibleOperator(bpy.types.Operator):
    bl_idname = "object.set_visible"
    bl_label = "Set Visible"
    bl_description = "Set visibility of objects"
    bl_options = {'REGISTER', 'UNDO'}

    value: bpy.props.BoolProperty(default=True)

    @classmethod
    def poll(cls, context):
        return context.mode == "EDIT_MESH"

    def execute(self, context):
        if self.value:
            bpy.ops.object.vertex_group_assign()
        else:
            bpy.ops.object.vertex_group_remove_from()
        return {'FINISHED'}

