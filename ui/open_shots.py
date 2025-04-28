import bpy
import os
import re
from ..utils import open_directory_in_explorer

root_folder = "G:\\Mon Drive\\ENSI\\01_E3\\Film 1mn\\02_PROD\\sequences"

def get_directory_content_recursive(directory_path):
	content = []
	for root, dirs, files in os.walk(directory_path):
		for name in dirs + files:
			content.append(os.path.join(root, name))
	return content

def get_first_level_folders(directory_path):
	try:
		return [entry.name for entry in os.scandir(directory_path) if entry.is_dir()]
	except FileNotFoundError:
		print(f"Directory not found: {directory_path}")
		return []

def sequences_tab():
	global root_folder
	return get_first_level_folders(root_folder)

def shots_tab(sequence):
	global root_folder
	return sorted(get_first_level_folders(os.path.join(root_folder, sequence)))

def shot_files(sequence, shot):
	global root_folder
	return [file for file in get_directory_content_recursive(os.path.join(root_folder, sequence, shot)) if file.endswith(".blend")]

class UI_Settings(bpy.types.PropertyGroup):
	# sequence: bpy.props.EnumProperty(
	# 	name="Sequence",
	# 	description="Select a sequence",
	# 	items=sequences_tab(),
	# 	default="",
	# )

	test: bpy.props.BoolProperty(default=False)


class PROD_FOM_OT_OpenFolder(bpy.types.Operator):
	bl_idname = "prod_fom.open_folder"
	bl_label = "Open Folder"
	bl_description = "Open the specified folder in the file explorer"

	folder_path: bpy.props.StringProperty(name="Folder Path", description="Path to the folder to open")

	def execute(self, context):
		open_directory_in_explorer(self.folder_path)
		return {'FINISHED'}

class PROD_FOM_PT_OpenShotsPanel(bpy.types.Panel):
	bl_label = "Open Shots"
	bl_idname = "PROD_FOM_PT_OpenShotsPanel"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_category = "Prod FOM"

	def draw(self, context):
		layout = self.layout
		draw_menu(layout, context)

class PROD_FOM_MT_OpenShotsMenu(bpy.types.Menu):
	bl_label = "Open Shots"
	bl_idname = "PROD_FOM_MT_OpenShotsMenu"

	def draw(self, context):
		layout = self.layout
		draw_menu(layout, context)


def draw_menu(layout: bpy.types.UILayout, context: bpy.types.Context):
	def add_button(file, sublayout, header_button=False):
		filename = os.path.basename(file)
		match = re.match(r"fom-seq_(\w*)-sh_(\d{1,})-(\w*)-v(\d{1,}).blend", filename)
		if match:
			sequence_id, shot_id, stage, version = match.groups()
			icon = {
				"layout": "SCENE_DATA",
				"anim": "ARMATURE_DATA",
				"lighting": "LIGHT"
			}
			op = sublayout.operator("wm.open_mainfile", text=f"{sequence_id}_{shot_id}-{stage}-v{version}" if not header_button else f"", icon=icon.get(stage, "LIBRARY_DATA_BROKEN"))
			op.filepath = file
			op.display_file_selector = False

	for sequence in sequences_tab():
		seq_header, seq_body = layout.panel(idname=sequence,default_closed=True)
		seq_header.label(text=sequence, icon="FILE_FOLDER")
		op = seq_header.operator("prod_fom.open_folder")
		op.folder_path = os.path.join(root_folder, sequence)

		if seq_body:
			for shot in shots_tab(sequence):
				sh_header, sh_body = seq_body.panel(idname=shot,default_closed=True)
				sh_header.label(text=shot, icon="CAMERA_DATA")
				for i, file in enumerate(reversed(shot_files(sequence, shot))):
					if i == 0:
						add_button(file, sh_header, True)
					if sh_body: add_button(file, sh_body)


def register():
	bpy.types.Window.prod_fom = bpy.props.PointerProperty(type=UI_Settings)

def unregister():
	del bpy.types.Window.prod_fom