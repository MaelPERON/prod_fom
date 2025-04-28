import bpy

from bpy.types import Context, ViewLayer
from .light_groups import ForceSceneUpdateLightGroups

def is_from_confo(vl: ViewLayer):
	return vl.get("is_from_confo")

class UpdateLightGroups(bpy.types.Operator):
	bl_idname = "fom.update_light_groups"
	bl_label = "Update Light Groups"
	bl_description = "A blank operator to update light groups"
	bl_options = {'REGISTER', 'UNDO'}

	def get_light_groups(self, context: Context) -> set:
		light_groups = set()

		for scene in context.blend_data.scenes:
			for vl in scene.view_layers:
				if is_from_confo(vl):
					continue
				for lg in vl.lightgroups:
					light_groups.add(lg.name)

		return light_groups

	def execute(self, context):

		view_layers = [vl for scene in context.blend_data.scenes for vl in scene.view_layers if is_from_confo(vl) is not None]
		light_groups = self.get_light_groups(context)

		for vl in view_layers:
			for lg in light_groups:
				if lg not in vl.lightgroups:
					vl.lightgroups.add(name=lg)

		
		self.report({"INFO"}, "Lightgroups updated.")
		return {'FINISHED'}
	
def node_header_draw(self, context):
	if context.space_data.tree_type == 'ConfoTree' and context.space_data.edit_tree is not None:
		self.layout.operator("fom.update_light_groups", text="Light Groups")


def register():
	bpy.types.NODE_MT_editor_menus.append(node_header_draw)

def unregister():
	bpy.types.NODE_MT_editor_menus.remove(node_header_draw)