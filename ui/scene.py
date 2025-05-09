import bpy
from ..operators.scene import SetSceneProperties, get_scene_properties, SetSceneCustomProperties, SetFrameRangeStep, SwitchViewLayer, ChangeRenderPrefix
from ..operators.render import RenderChecklist

def create_property(prop, settings):
	rna_uiitem = None
	match (type := getattr(settings, "type", None)):
		case "STRING":
			rna_uiitem = bpy.props.StringProperty(
				name=prop,
				description=settings["description"],
				default=settings["default"],
			)
		case "FLOAT":
			rna_uiitem = bpy.props.FloatProperty(
				name=prop,
				description=settings["description"],
				default=settings["default"],
				min=settings.get("min", 0.0),
				max=settings.get("max", 1.0),
			)
		case "INT":
			rna_uiitem = bpy.props.IntProperty(
				name=prop,
				description=settings["description"],
				default=settings["default"],
				min=settings.get("min", 0),
				max=settings.get("max", 100),
			)
		case "BOOL":
			rna_uiitem = bpy.props.BoolProperty(
				name=prop,
				description=settings["description"],
				default=settings["default"],
			)
		case "ENUM":
			rna_uiitem = bpy.props.EnumProperty(
				name=prop,
				description=settings["description"],
				items=[(k, v, "") for k, v in settings.items()],
			)
		case "NAME":
			rna_uiitem = bpy.props.StringProperty(
				name=prop,
				description=settings["description"],
				default=settings["default"],
			)
	return rna_uiitem

def register():
	pass
	# for prop, settings in get_scene_properties().items():
	# 	if prop not in bpy.types.Scene.bl_rna.properties:
	# 		print(f"Registering {prop} property")
	# 		bpy.types.Scene.__annotations__[prop] = create_property(prop, settings)

class PropertyPanel():
	bl_label = "Scene Properties"
	bl_category = "Prod FOM"
	bl_region_type = 'UI'

	def draw(self, context):
		layout = self.layout
		draw_menu(layout, context)

class ViewPropertiesPanel(bpy.types.Panel, PropertyPanel):
	bl_idname = "PROD_FOM_PT_RootPropertiesPanel"
	bl_space_type = 'VIEW_3D'

class ConfoPropertiesPanel(bpy.types.Panel, PropertyPanel):
	bl_idname = "PROD_FOM_PT_ConfoPropertiesPanel"
	bl_space_type = 'NODE_EDITOR'

class ConfoLightGroup(bpy.types.Panel, PropertyPanel):
	bl_idname = "PROD_FOM_PT_ConfoLG"
	bl_space_type = 'NODE_EDITOR'

	def draw(self, context: bpy.types.Context):
		objs = [obj for obj in context.selected_objects if obj.type == "LIGHT"]
		lgs = set()
		layout = self.layout

		for obj in objs:
			if obj.lightgroup != "":
				lgs.add(obj.lightgroup)
		
		layout.label(text=str(lgs))




def draw_menu(layout: bpy.types.UILayout, context):
	scene : bpy.types.Scene = context.scene

	layout.operator(SetSceneCustomProperties.bl_idname)
	layout.separator()
	layout.operator_context = "EXEC_SCREEN"

	# Add a button to set the scene properties
	for mode in ["LOW", "HIGH", "DEFAULT"]:
		op = layout.operator(SetSceneProperties.bl_idname, text=f"Set {mode} Poly Settings")
		op.mode = mode

	layout.separator()
	layout.prop(scene.render, "film_transparent")
	layout.prop(scene.cycles, "texture_limit_render")

	col = layout.column()
	row = layout.row(align=True)
	for vl in ["All","00_ENV","01_SET","02_SETDRESS","03_SUBJECT"]:
		vl = scene.view_layers.get(vl, None)
		if vl:
			if vl.name != "All":
				col.prop(vl, "use", toggle=True, text=f"{vl.name}")
			op = row.operator(SwitchViewLayer.bl_idname, text=f"{vl.name}")
			op.view_layer_name = vl.name

	col.prop(scene.render, "use_single_layer", toggle=True)

	layout.separator()
	for setting in ["QUICK", "FULL"]:
		op = layout.operator(RenderChecklist.bl_idname, text=f"Render Checklist ({setting})")
		op.mode = setting

	layout.separator()
	for setting in ["FULL","HALF","FML"]:
		op = layout.operator(SetFrameRangeStep.bl_idname, text=f"Frame step : {setting}")
		op.mode = setting

	row = layout.row(align=True)
	for prefix in ["fml","ld","hd"]:
		op = row.operator(ChangeRenderPrefix.bl_idname, text=prefix.upper())
		op.new_prefix = prefix
	# for prop, settings in get_scene_properties().items():
	# 	if prop in scene:
	# 		if (type := getattr(settings, "type", None)) == "LOD":
	# 			layout.prop(scene, prop, text=settings["name"], toggle=True)
	# 		else:
	# 			layout.prop(scene, prop, text=settings["name"])