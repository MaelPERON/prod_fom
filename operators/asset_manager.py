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