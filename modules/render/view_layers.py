import bpy

view_layers = {
	"00_ENV": True,
	"01_SET": True,
	"02_SETDRESS": True,
	"03_SUBJECT": True,
}

for vl, state in view_layers.items():
	vl : bpy.types.ViewLayer = bpy.context.scene.view_layers.get(vl, None)
	if vl:
		vl.use = state