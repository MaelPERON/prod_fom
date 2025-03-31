import bpy


class ShowModifierOperator(bpy.types.Operator):
	bl_idname = "object.show_modifier"
	bl_label = "Toggle Side Visibility"
	bl_description = "Toggle the RIGHT modifier on the bdt_pant object"
	bl_options = {'REGISTER', 'UNDO'}

	left: bpy.props.BoolProperty(default=False)

	def execute(self, context):
		obj = bpy.data.objects.get("bdt_pant")
		if not obj:
			self.report({'ERROR'}, "Object 'bdt_pant' not found")
			return {'CANCELLED'}
		
		left = obj.modifiers.get("LEFT")
		if not left:
			self.report({'ERROR'}, "Modifier 'RIGHT' not found on 'bdt_pant'")
			return {'CANCELLED'}
		
		left.show_viewport = self.left
		left.show_in_editmode = self.left

		return {'FINISHED'}

class ToggleInvertVertexGroupOperator(bpy.types.Operator):
	bl_idname = "object.toggle_invert_vertex_group"
	bl_label = "Toggle Invert Vertex Group"
	bl_description = "Toggle the invert_vertex_group attribute of the LEFT modifier on the bdt_pant object"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		obj = bpy.data.objects.get("bdt_pant")
		if not obj:
			self.report({'ERROR'}, "Object 'bdt_pant' not found")
			return {'CANCELLED'}
		
		left = obj.modifiers.get("LEFT")
		if not left:
			self.report({'ERROR'}, "Modifier 'LEFT' not found on 'bdt_pant'")
			return {'CANCELLED'}
		
		left.invert_vertex_group = not left.invert_vertex_group

		return {'FINISHED'}

class HideFacesFromVertexGroupOperator(bpy.types.Operator):
	bl_idname = "object.hide_faces_from_vertex_group"
	bl_label = "Hide Faces from Vertex Group"
	bl_description = "Hide faces associated with the 'LEFT_SIDE' vertex group in the 'bdt_pant' mesh"
	bl_options = {'REGISTER', 'UNDO'}

	left_side: bpy.props.BoolProperty(default=True)
	isolate: bpy.props.BoolProperty(default=True)

	def execute(self, context):
		obj = bpy.data.objects.get("bdt_pant")
		if not obj or obj.type != 'MESH':
			self.report({'ERROR'}, "Mesh object 'bdt_pant' not found")
			return {'CANCELLED'}
		
		side = "SIDE_LEFT" if self.left_side else "SIDE_RIGHT"
		vertex_group = obj.vertex_groups.get(side)
		if not vertex_group:
			self.report({'ERROR'}, f"Vertex group '{side}' not found on 'bdt_pant'")
			return {'CANCELLED'}
		
		obj.vertex_groups.active = vertex_group
		override = context.copy()

		if context.active_object == obj:
			bpy.ops.object.mode_set(mode="EDIT")
			bpy.ops.mesh.reveal(select=False)
			bpy.ops.mesh.select_mode(type="FACE")

			if self.isolate:
				bpy.ops.object.vertex_group_select()
				bpy.ops.mesh.hide(unselected=True)

		return {'FINISHED'}
