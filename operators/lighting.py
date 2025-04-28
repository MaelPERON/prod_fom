import bpy
import re

coll_pattern = r"(LGT-)?(.*)$"

class LIGHTING_OT_name_automation(bpy.types.Operator):
	bl_idname = "lighting.name_automation"
	bl_label = "Lighting Name Automation"
	bl_description = "Automate naming of lighting objects"
	bl_options = {'REGISTER', 'UNDO'}

	def execute(self, context):
		light_collection : bpy.types.Collection = context.blend_data.collections.get("LIGHTING")

		if not light_collection:
			self.report({"ERROR"}, "No Light collection found")
			return {"CANCELLED"}
		
		collections : list[bpy.types.Collection] = light_collection.children_recursive

		for coll in collections:
			coll_name = "LGT-" + re.sub(coll_pattern, r"\2", coll.name)
			coll.name = coll_name

			for obj in coll.objects:
				if obj.type == "LIGHT":
					light_group = coll_name.upper().replace("LGT-", "")
					obj.lightgroup = light_group

					if context.view_layer.lightgroups.get(light_group) is None:
						context.view_layer.lightgroups.add(name=light_group)

		return {'FINISHED'}