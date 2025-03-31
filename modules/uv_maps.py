import bpy

# Iterate through all selected objects
for obj in bpy.context.selected_objects:
	if obj.type == 'MESH':  # Ensure the object is a mesh
		uv_layers = obj.data.uv_layers
		
		# Rename the active UV Map to "MD_UVMap"
		if uv_layers.active:
			uv_layers.active.name = "MD_UVMap"
		
		# Create a new UV Map called "B_UVMap" if it doesn't exist
		if "B_UVMap" not in uv_layers:
			new_uv_map = uv_layers.new(name="B_UVMap")
			uv_layers.active = new_uv_map  # Set it as active
			new_uv_map.active_render = True