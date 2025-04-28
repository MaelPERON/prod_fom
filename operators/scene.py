import bpy
import re
from datetime import datetime
from ..utils import extract_from_filename, open_directory_in_explorer
from pathlib import Path


scene_properties = {
    "FOM_world_diff_int": {
        "name": "World Diffuse Intensity",
        "description": "Intensity of the world diffuse light",
        "default": 1.0,
    },
    "FOM_world_cam_int": {
        "name": "World Camera Intensity",
        "description": "Intensity of the world diffuse light",
        "default": 1.0,
    },
    "FOM_neon_led_intensity": {
        "name": "Neon LED Intensity",
        "description": "Intensity of the neon LED light",
        "default": 1.0,
    },
    "FOM_neon_led_multiply": {
        "name": "Neon LED Multiply",
        "description": "Multiply factor for the neon LED light",
        "default": 1.0,
    },
    "low_chains": {
        "name": "Low Chain",
        "description": "Use low chain settings",
        "type": "LOD",
        "inverted": True,
        "default": True
    },
    "low_ground": {
        "name": "Low Ground",
        "description": "Use low ground settings",
        "type": "LOD",
        "default": True
    },
}

def get_scene_properties():
    global scene_properties
    return scene_properties

def set_properties(scene: bpy.types.Scene):
    for prop, settings in scene_properties.items():
            if getattr(scene, prop, None) is None and (prop_type := getattr(settings, "type", None)) != "LOD":
                if prop_type == "LOD":
                    if self.mode != "DEFAULT":
                        boolean = self.mode == "LOW"
                        scene[prop] = not boolean if getattr(settings, "inverted", False) else boolean
                else:
                    scene[prop] = settings["default"]
            else:
                print(f"Property {prop} already exists in the scene. Skipping creation.")
                continue

class SetSceneCustomProperties(bpy.types.Operator):
    bl_idname = "animation.fom_set_scene_custom_properties"
    bl_label = "Set Scene Custom Properties"
    bl_description = "Set custom properties for the scene"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Placeholder for custom property logic
        set_properties(context.scene)
        self.report({'INFO'}, "Custom properties set successfully")
        return {'FINISHED'}

class SetSceneProperties(bpy.types.Operator):
    bl_idname = "animation.fom_set_scene_properties"
    bl_label = "Set Scene Properties"
    bl_description = "Set the scene properties based on the current file name"
    bl_options = {"REGISTER"}

    mode: bpy.props.EnumProperty(items=[
        ("LOW", "Low Poly", "Set low poly settings"),
        ("HIGH", "High Poly", "Set high poly settings"),
        ("DEFAULT", "Default", "Set default settings"),
    ], default="DEFAULT",name="Mode",description="Select the mode to set the scene properties")

    @classmethod
    def poll(self, context):
        return True

    def execute(self, context):
        # Render settings
        scene = context.scene
        scene.render.resolution_x = 1280
        scene.render.resolution_y = 720
        scene.render.resolution_percentage = 25 if self.mode == "LOW" else 100
        scene.cycles.adaptive_threshold = 0.05 if self.mode == "LOW" else 0.02
        scene.render.film_transparent = True
        scene.cycles.samples = 128 if self.mode == "LOW" else 512
        scene.cycles.use_denoising = False
        scene.cycles.use_auto_tile = True
        scene.cycles.tile_size = 512
        if self.mode == "HIGH":
            scene.render.use_simplify = self.mode == False

        # Variables
        set_properties(scene)

        # for cam in [obj for obj in scene.objects if obj.type == "CAMERA"]:
        #     cam.data.dof.use_dof = False
        return {'FINISHED'}

class ExportPlaybast(bpy.types.Operator):
    bl_idname= "animation.fom_export_playbast"
    bl_label = "Export Playbast"
    bl_description = "Export the current scene for playblast"
    bl_options = {"REGISTER"}

    open_folder: bpy.props.BoolProperty(
        name="Open Folder",
        description="Open the folder containing the exported file",
        default=True
    )

    include_date: bpy.props.BoolProperty(
        name="Include Date",
        description="Include the current date in the filename",
        default=True
    )

    @classmethod
    def poll(self, context):
        return context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        if match := extract_from_filename(bpy.path.display_name_from_filepath(context.blend_data.filepath)):
            seq, shot, task, version = match.groups()
            camera = context.scene.camera.name

            render_filepath = context.scene.render.filepath

            root_folder = "c:/tmp/FOM/Playblast"
            context.scene.render.filepath = f"{root_folder}/{seq}_{shot}_{task}_v{version}_{camera}" + ("-v" + datetime.now().strftime("%m%d_%H%M%S") if self.include_date else "") + '.mp4'
            bpy.ops.render.opengl(animation=True, write_still=True, view_context=True)
            context.scene.render.filepath = render_filepath

            if self.open_folder:
                open_directory_in_explorer(root_folder)
        else:
            self.report({'ERROR'}, "Filename does not match the expected pattern")
            return {"CANCELLED"}
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "open_folder", toggle=True)
        layout.prop(self, "include_date", toggle=True)