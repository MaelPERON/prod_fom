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

		self.report({"INFO"}, "\n\nChecking...")

		checklist_items = {
			"Resolution": {
				"values": [render.resolution_x, render.resolution_y],
				"expected": [1280, 720],
			},
			"Percentage": {
				"values": [render.resolution_percentage],
				"expected": [100],
			},
			"Film Transparent": {
				"values": [render.film_transparent],
				"expected": [True],
			},
			"Samples": {
				"values": [scene.cycles.samples],
				"expected": [512],
			},
			"Use Denoising": {
				"values": [scene.cycles.use_denoising],
				"expected": [False],
			},
			"Use Auto Tile": {
				"values": [scene.cycles.use_auto_tile],
				"expected": [True],
			},
			"Tile Size": {
				"values": [scene.cycles.tile_size],
				"expected": [512],
			},
		}

		errors = []

		for item, settings in checklist_items.items():
			values = settings.get("values", None)
			expected = settings.get("expected", None)
			if values is None:
				self.report({"WARNING"}, f"[{item}] No values found.")
				continue
			if expected is None:
				self.report({"WARNING"}, f"[{item}] Expected data not found.")
				continue

			if not(values == expected):
				errors.append([item, settings])
				self.report({"ERROR"}, f"[{item}] Expected '{expected}', got '{values}' instead")

		if (n := len(errors)) < 1:
			self.report({"INFO"}, "Checklist : Everything's ok !!!")
		else:
			self.report({"ERROR"}, f"Ouch ! {n} errors found :c")
		return {"FINISHED"}