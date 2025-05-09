import bpy

class RenderChecklist(bpy.types.Operator):
	bl_idname = "render.checklist"
	bl_label = "Render Checklist"
	bl_description = "Checklist for render settings"
	bl_options = {"REGISTER"}

	mode: bpy.props.EnumProperty(items=[
		("QUICK", "Quick", "Quick render settings"),
		("FULL", "Full", "Full render settings"),
	], default="FULL", name="Mode", description="Select the mode to set the render settings")

	@classmethod
	def poll(self, context): return True

	def invoke(self, context, event):
		if self.mode == "FULL":
			return context.window_manager.invoke_props_dialog(self)
		return self.execute(context)

	def draw(self, context):
		layout = self.layout
		layout.label(text="Please confirm the following settings:")
		layout.prop(context.scene.render, "resolution_x", text="Resolution X")
		layout.prop(context.scene.render, "resolution_y", text="Resolution Y")
		layout.prop(context.scene.render, "resolution_percentage", text="Resolution Percentage")
		layout.prop(context.scene.cycles, "samples", text="Samples")
		layout.prop(context.scene.cycles, "use_denoising", text="Use Denoising")
		layout.prop(context.scene.cycles, "tile_size", text="Tile Size")

	def execute(self, context):
		# Check render settings
		scene = context.scene
		render = scene.render

		if self.mode == "FULL":
			self.report({"INFO"}, "FULL mode selected. Proceeding with additional checks.")

		def safe_getpath(path: str, context):
			parts : list[str] = path.split(".")
			root = parts.pop(0)
			if hasattr(context, root):
				obj = getattr(context, root)
				for part in parts:
					if hasattr(obj, part):
						obj = getattr(obj, part)
					else:
						return "UNDEFINED"
						raise AttributeError(f"{part} not found in {path}")
			else:
				print(f"ERROR: {root} not found in locals")
				return "UNDEFINED"
			
			return obj

		self.report({"INFO"}, "\n\nChecking...")

		checklist_items = {
			"Resolution": {
				"values": ["scene.render.resolution_x", "scene.render.resolution_y"],
				"expected": [1280, 720],
			},
			"Percentage": {
				"values": ["scene.render.resolution_percentage"],
				"expected": [100],
			},
			"Film Transparent": {
				"values": ["scene.render.film_transparent"],
				"expected": [True],
			},
			"Samples": {
				"values": ["scene.cycles.samples"],
				"expected": [512],
			},
			"Use Denoising": {
				"values": ["scene.cycles.use_denoising"],
				"expected": [False],
			},
			"Use Auto Tile": {
				"values": ["scene.cycles.use_auto_tile"],
				"expected": [True],
			},
			"Tile Size": {
				"values": ["scene.cycles.tile_size"],
				"expected": [512],
			},
			"File Format": {
				"values": ["scene.render.image_settings.file_format"],
				"expected": ["OPEN_EXR_MULTILAYER"],
			},
			"EXR Codec": {
				"values": ["scene.render.image_settings.exr_codec"],
				"expected": ["DWAA"],
			},
			"Color Depth": {
				"values": ["scene.render.image_settings.color_depth"],
				"expected": ["16"],
			},
			"World Name": {
				"values": ["scene.world.name"],
				"expected": ["Usine_INT_nuit", "Usine_EXT_nuit"],
				"compare": "IN"
			},
			"Render All Layers": {
				"values": ["scene.render.use_single_layer"],
				"expected": [False],
				"is_error": False
			}
		}

		errors = []

		for item, settings in checklist_items.items():
			values = [safe_getpath(setting, context) for setting in settings.get("values", None)]
			expected = settings.get("expected", None)
			if values is None or "UNDEFINED" in values:
				self.report({"ERROR"}, f"[{item}] No values found or contains 'UNDEFINED'.")
				continue
			if expected is None:
				self.report({"WARNING"}, f"[{item}] Expected data not found.")
				continue

			on_error = False
			match settings.get("compare", None):
				case "IN":
					on_error = not any(val in expected for val in values)
				case None:
					on_error = not(values == expected)

			if on_error:
				is_error = settings.get("is_error", True)
				if is_error:
					errors.append([item, settings])
				self.report({"ERROR"}, f"{'💀' if is_error else '👀'} [{item}] Expected '{expected}', got '{values}' instead")

		if (n := len(errors)) < 1:
			self.report({"INFO"}, "Checklist : Everything's ok !!!")
		else:
			self.report({"ERROR"}, f"Ouch ! {n} errors found :c")
		return {"FINISHED"}