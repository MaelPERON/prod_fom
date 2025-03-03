import bpy
import os
from bpy.types import Operator

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

		return {"FINISHED"}