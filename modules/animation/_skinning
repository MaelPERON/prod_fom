import bpy
from ..operators.skinning import HideFacesFromVertexGroupOperator

class SkinningPanel(bpy.types.Panel):
	bl_label = "Skinning"
	bl_idname = "VIEW3D_PT_skinning"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = 'Tool'

	def draw(self, context):
		layout = self.layout
		layout.label(text="Skinning Tools")
		row = layout.row()
		op = row.operator("object.show_modifier",text="-")
		op.left = False
		op = row.operator("object.show_modifier",text="+")
		op.left = True
		layout.operator("object.toggle_invert_vertex_group")
		row = layout.row()
		op = row.operator(HideFacesFromVertexGroupOperator.bl_idname,text="L")
		op.left_side = True
		op.isolate = True
		op = row.operator(HideFacesFromVertexGroupOperator.bl_idname,text="R")
		op.left_side = False
		op.isolate = True
		op = layout.operator(HideFacesFromVertexGroupOperator.bl_idname,text="Show All")
		op.isolate = False

class ReverseUVShapeKeyPanel(bpy.types.Panel):
    bl_label = "Reverse UV Shape Key"
    bl_idname = "OBJECT_PT_reverse_uv_shape_key"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.reverse_uv_shape_key")
        layout.operator("object.disable_nodes_modifier")
        layout.operator("object.reload_deformed_cloth")
        row = layout.row()
        op = row.operator("object.set_visible",text="+")
        op.value = True
        op = row.operator("object.set_visible",text="-")
        op.value = False