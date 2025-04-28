import bpy
import os
import re
from bpy.types import Operator
from bpy.path import basename, display_name_from_filepath
from ..utils import get_collection

class Mixin():
	@classmethod
	def poll(self, context):
		return True

class Create(Mixin, Operator):
	bl_idname = "scene.fom_asset_create"
	bl_label = "Create Asset File"

	# TODO: check if asset already exists
	
	def execute(self, context):
		pass
		return {"FINISHED"}

class Open(Mixin, Operator):
	bl_idname = "scene.fom_asset_open"
	bl_label = "Open Asset"

	# TODO: open last or selected version of said selected asset
	
	def execute(self, context):
		pass
		return {"FINISHED"}

class Increment(Mixin, Operator):
	bl_idname = "scene.fom_asset_increment"
	bl_label = "Increment Asset"
	
	def execute(self, context):
		pass
		return {"FINISHED"}
	

class OpenFileBrowser(Mixin, Operator):
	bl_idname = "scene.fom_asset_open_file_browser"
	bl_label = "Open File Browser"

	def execute(self, context):
		windows = context.window_manager.windows
		main_window = next(window for window in windows if window.screen)
		area = max(windows[0].screen.areas, key=lambda a: a.width * a.height)

		with context.temp_override(area=area):
			original_resolution_x = context.scene.render.resolution_x
			original_resolution_y = context.scene.render.resolution_y


			context.scene.render.resolution_x = int(main_window.width/2)
			context.scene.render.resolution_y = int(main_window.height/2)

			bpy.ops.render.view_show("INVOKE_DEFAULT")
			window = context.window_manager.windows[-1]
			area = window.screen.areas[0]
			area.type = "FILE_BROWSER"
			area.ui_type = "ASSETS"
			area.tag_redraw()

			def defer():
				params = area.spaces.active.params
				if not params:
					return 0

				try:
					params.asset_library_reference = "FOM"
				except TypeError:
					# If the reference doesn't exist.
					params.asset_library_reference = "All"
				params.import_type = 'APPEND'

			bpy.app.timers.register(defer)


			# with context.temp_override(area=area):

			# bpy.ops.screen.area_duplicate()

			# window = context.window_manager.windows[-1]

			# with context.temp_override(window=window):
			# 	area = window.screen.areas[0]
			# 	area.type = "FILE_BROWSER"
			# 	area.ui_type = "ASSETS"
			# 	area.tag_redraw()

		context.scene.render.resolution_x = original_resolution_x
		context.scene.render.resolution_y = original_resolution_y


		return {"FINISHED"}

class ClearAssetFile(Mixin, Operator):
	bl_idname = "scene.fom_asset_clear"
	bl_label = "Clear Asset File"
	asset = None

	overwrite: bpy.props.BoolProperty(name="Overwrite File", description="Automatically saves after removing assets from file.", default=False)

	# Split the file name by "-"
	@staticmethod
	def get_file_params(filepath):
		file_name = basename(filepath)
		params = file_name.split("-")
		if len(params) != 5:
			raise None

		project, asset_type, asset_name, task, version = params
		return {
			"file_name": file_name,
			"filepath": filepath,
			"project": project,
			"asset_type": asset_type,
			"asset_name": asset_name,
			"task": task,
			"version": int(re.sub(r"(v)?(\d{1,})(\.blend)", r"\2", version))
		}
	
	@classmethod
	def poll(self, context):
		return self.get_file_params(context.blend_data.filepath) is not None
	
	def execute(self, context):
		directory = os.path.dirname(context.blend_data.filepath)
		self.asset = self.get_file_params(context.blend_data.filepath)
		version_list = []

		for filename in os.listdir(directory):
			if filename.endswith(".blend") and filename != self.asset["file_name"]:
				filepath = os.path.join(directory, filename)
				file_params = self.get_file_params(filepath)
				if file_params is not None:
					print(f"Adding version from {filename}")
					version_list.append(file_params["version"])

		# Get the latest version number
		if len(version_list) < 1:
			self.report({"WARN"}, "No other files found in the directory")
			return {"CANCELLED"}
		
		latest_version = max(version_list)

		if latest_version > self.asset["version"]:
			# Get all objects and collections marked as assets
			assets = []
			for obj in bpy.data.objects:
				if obj.asset_data is not None:
					assets.append(obj)
			for collection in bpy.data.collections:
				if collection.asset_data is not None:
					assets.append(collection)

			for asset in assets:
				# Remove the asset data
				self.report({"INFO"}, f"Clearing asset {asset.name}")
				asset.asset_clear()

			# Save the file if OVERWRITE is set to True
			if self.overwrite:
				print("Saving file...")
				bpy.ops.wm.save_mainfile()
				print("File saved.")
			
			return {"FINISHED"}
		self.report({"INFO"}, "No newer versions found. Cannot remove assets.")

class OpenAssetFolder(Mixin, Operator):
	bl_idname = "scene.fom_asset_open_folder"
	bl_label = "Open Asset Folder"

	@classmethod
	def poll(self, context):
		return context.asset is not None

	def execute(self, context):
		asset = context.asset
		if not asset:
			self.report({"ERROR"}, "No asset selected")
			return {"CANCELLED"}

		asset_path = bpy.path.abspath(asset.full_library_path)
		folder_path = asset_path[:-len(bpy.path.basename(asset_path))]
		if not os.path.exists(folder_path):
			self.report({"ERROR"}, "Asset path does not exist")
			return {"CANCELLED"}

		# Open the file explorer at the asset location
		if os.name == 'nt':
			os.startfile(folder_path)
		elif os.name == 'posix':
			os.system(f'xdg-open "{folder_path}"')
		else:
			self.report({"ERROR"}, "Unsupported OS")
			return {"CANCELLED"}

		return {"FINISHED"}
	
class SetExporters(Mixin, Operator):
	bl_idname = "scene.fom_set_exporters"
	bl_label = "Set Exporters"

	def execute(self, context):
		high_settings = {'add_leaf_bones': True, 'apply_scale_options': 'FBX_SCALE_NONE', 'apply_unit_scale': True, 'armature_nodetype': 'NULL', 'axis_forward': '-Z', 'axis_up': 'Y', 'bake_anim': False, 'bake_anim_force_startend_keying': True, 'bake_anim_simplify_factor': 1.0, 'bake_anim_step': 1.0, 'bake_anim_use_all_actions': True, 'bake_anim_use_all_bones': True, 'bake_anim_use_nla_strips': True, 'bake_space_transform': False, 'batch_mode': 'OFF', 'check_existing': True, 'collection': '', 'colors_type': 'SRGB', 'embed_textures': False, 'filepath': '//..\\export\\{{name}}_high.fbx', 'filter_glob': '*.fbx', 'global_scale': 1.0, 'mesh_smooth_type': 'OFF', 'object_types': {'MESH'}, 'path_mode': 'RELATIVE', 'primary_bone_axis': 'Y', 'prioritize_active_color': False, 'secondary_bone_axis': 'X', 'use_active_collection': False, 'use_armature_deform_only': False, 'use_batch_own_dir': True, 'use_custom_props': False, 'use_mesh_edges': False, 'use_mesh_modifiers': True, 'use_mesh_modifiers_render': True, 'use_metadata': True, 'use_selection': False, 'use_space_transform': True, 'use_subsurf': False, 'use_triangles': False, 'use_tspace': False, 'use_visible': False}
		low_settings = {'add_leaf_bones': True, 'apply_scale_options': 'FBX_SCALE_NONE', 'apply_unit_scale': True, 'armature_nodetype': 'NULL', 'axis_forward': '-Z', 'axis_up': 'Y', 'bake_anim': False, 'bake_anim_force_startend_keying': True, 'bake_anim_simplify_factor': 1.0, 'bake_anim_step': 1.0, 'bake_anim_use_all_actions': True, 'bake_anim_use_all_bones': True, 'bake_anim_use_nla_strips': True, 'bake_space_transform': False, 'batch_mode': 'OFF', 'check_existing': True, 'collection': '', 'colors_type': 'SRGB', 'embed_textures': False, 'filepath': '//..\\export\\{{name}}_low.fbx', 'filter_glob': '*.fbx', 'global_scale': 1.0, 'mesh_smooth_type': 'OFF', 'object_types': {'MESH'}, 'path_mode': 'RELATIVE', 'primary_bone_axis': 'Y', 'prioritize_active_color': False, 'secondary_bone_axis': 'X', 'use_active_collection': False, 'use_armature_deform_only': False, 'use_batch_own_dir': True, 'use_custom_props': False, 'use_mesh_edges': False, 'use_mesh_modifiers': True, 'use_mesh_modifiers_render': True, 'use_metadata': True, 'use_selection': False, 'use_space_transform': True, 'use_subsurf': False, 'use_triangles': False, 'use_tspace': False, 'use_visible': False}

		filename = display_name_from_filepath(bpy.data.filepath)
		object = filename.split('-')[-2]

		def obj_to_json(obj):
			new_obj = {}
			for attr in dir(obj):
				if attr.startswith("__") or attr.startswith("bl_"): continue
				value = getattr(obj, attr, None)
				id_data = getattr(value, "id_data", None)
				# print(attr, value, id_data)
				new_obj[attr] = value if id_data is None else None
			return new_obj

		collections = {
			"high": get_collection("High"),
			"low": get_collection("Low")
		}

		for type, collection in collections.items():
			if collection is None:
				print(f"{type} collection not available")
			with context.temp_override(collection=collection):
				if len(collection.exporters) < 1:
					self.report({"INFO"}, f"Added exporter {type} to {collection.name}")
					bpy.ops.collection.exporter_add('INVOKE_DEFAULT',name="IO_FH_fbx")
				exporter = collection.exporters[0]
				settings = exporter.export_properties
				new_settings = low_settings if type == "low" else high_settings
				for setting, value in new_settings.items():
					setattr(settings, setting, value)

				settings.filepath = settings.filepath.replace("{{name}}", object)

			self.report({"INFO"}, f"Settings set for {collection.name}")
		return {"FINISHED"}

class LowCollectionPreparation(Mixin, Operator):
	bl_idname = "scene.fom_low_collection_preparation"
	bl_label = "Low Collection Preparation"

	def execute(self, context):
		collection = get_collection("Low")
		if collection is None:
			self.report({"WARN"}, f"Could not find low poly collection")
			return {"CANCELLED"}
		
		for obj in collection.objects:
			if obj.type == "MESH":
				obj.name = re.sub(r"_high(\.\d+)?$", "_low", obj.name)
				for mod in obj.modifiers:
					if mod.type.lower() not in ["nodes","mask","multires","armature","collision","particle_instance","particle_system"]:
						print(f"[{obj.name}]\t\tremoving '{mod.name}'\t({mod.type})")
						obj.modifiers.remove(mod)
		return {"FINISHED"}