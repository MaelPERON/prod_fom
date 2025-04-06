import bpy

def assign_vertices_to_vertex_group(obj : bpy.types.Object, vertex_group_name : str):
	mesh = obj.data
	if not mesh or not isinstance(mesh, bpy.types.Mesh):
		raise ValueError("Invalid mesh provided.")
	
	if vertex_group_name not in obj.vertex_groups:
		obj.vertex_groups.new(name=vertex_group_name)
	
	vertex_group = obj.vertex_groups[vertex_group_name]
	vertex_indices = [v.index for v in mesh.vertices]
	vertex_group.add(vertex_indices, 1.0, 'REPLACE')

class ParentToBoneVertexGroup(bpy.types.Operator):
	bl_idname = "object.parent_to_bone_vertex_group"
	bl_label = "Parent to Bone Vertex Group"
	bl_options = {'REGISTER', 'UNDO'}

	auto_parent_armature: bpy.props.BoolProperty(
		name="Auto Parent Armature",
		description="Automatically parent selected meshes to the armature",
		default=True,
	)

	@classmethod
	def poll(self, context):
		armature = context.active_object
		objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
		mode = (context.mode == "POSE" or context.mode == "EDIT_ARMATURE")
		return context.active_object.type == "ARMATURE" and len(objects) > 0 and mode

	def execute(self, context):
		bone = context.active_pose_bone.bone if context.mode == "POSE" else context.active_bone
		if not bone.use_deform:
			self.report({'WARNING'}, "Bone does not deform mesh")
			return {"CANCELLED"}
		objects = [obj for obj in context.selected_objects if obj.type == "MESH"]

		for obj in objects:
			# Auto parenting to armature
			mods = [mod for mod in obj.modifiers if mod.type == 'ARMATURE' and mod.object == context.active_object]
			if not mods and self.auto_parent_armature:
				obj.modifiers.new(name="Armature", type='ARMATURE')
				obj.modifiers["Armature"].object = context.active_object
				self.report({'INFO'}, f"'{obj.name}' parented to '{context.active_object.name}'")

			# Assigning vertices to vertex group
			assign_vertices_to_vertex_group(obj, bone.name)
			self.report({'INFO'}, f"'{obj.name}' deformed by '{bone.name}'")

		self.report({'INFO'}, f"Assigned vertices to vertex group '{bone.name}' in {len(objects)} objects")
		return {'FINISHED'}