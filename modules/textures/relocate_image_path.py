import bpy
from bpy.path import abspath
from pathlib import Path

material: bpy.types.Material = bpy.data.materials.get("my_material")
override = material.override_create(remap_local_usages=True)



# for image in bpy.data.images:
# 	if (lib := image.library) is not None:
# 		lib_path = Path(abspath(lib.filepath)).parent
# 		if (img_path := image.filepath).startswith("//"):
# 			full_path = lib_path / img_path.replace("//", "")
# 			resolved_path = full_path.resolve()
			
# 			if not resolved_path.exists():
# 				print(f"{image.name} path not found [{resolved_path}]")
# 				continue

			# Copying the file

			# Changing the filepath with the new one

		# print(full_path)