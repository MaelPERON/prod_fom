import bpy
import re

for scene in bpy.data.scenes:
	for vl in scene.view_layers:
		if re.search(r"^\d{1,}_", vl.name) is not None:
			# vl.
			pass