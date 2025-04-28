import bpy
import re

rig = bpy.context.scene.objects.get("RIG-poulie.000")

def add_drivers_to_objects(objects: list[bpy.types.Object]):
	if rig is None:
		return print("No Armature found")
	
	for obj in objects:
		if (match := re.search(r"prop_(shirt|pant)[-_](\d{1,})-(chute|static)", obj.name)) is not None:
			_type, _version, _anim = match.group(1), int(match.group(2)), match.group(3)

			for mod in obj.modifiers:
				if mod.type == "MESH_SEQUENCE_CACHE":
					cache: bpy.types.CacheFile = mod.cache_file
					if cache is not None:
						cache.override_frame = True
						driver = cache.driver_add("frame").driver
						driver.expression = f"var if var > 0 else 0"
						while driver.variables:
							driver.variables.remove(driver.variables[0])
						
						x = driver.variables.new()
						x.name = "var"
						x.type = 'SINGLE_PROP'
						x.targets[0].id = rig
						x.targets[0].data_path = f'pose.bones["root"]["frame"]'
			
			print(obj.name)
			for prop in ["hide_render", "hide_viewport"]:
				driver = obj.driver_add(prop).driver
				driver.expression = f"not(((var == {_version-1} and animated == {_anim == 'chute'}) or show_all))"

				while driver.variables:
					driver.variables.remove(driver.variables[0])

				x = driver.variables.new()
				x.name = "var"
				x.type = 'SINGLE_PROP'
				x.targets[0].id = rig
				x.targets[0].data_path = f'pose.bones["root"]["{_type}"]'

				show_all = driver.variables.new()
				show_all.name = "show_all"
				show_all.targets[0].id = rig
				show_all.targets[0].data_path = 'pose.bones["root"]["show_all"]'
				
				animated = driver.variables.new()
				animated.name = "animated"
				animated.targets[0].id = rig
				animated.targets[0].data_path = 'pose.bones["root"]["animated"]'

# Example usage:
add_drivers_to_objects([obj for obj in bpy.context.scene.objects if obj.name.startswith("prop_")])