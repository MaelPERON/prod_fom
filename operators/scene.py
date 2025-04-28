import bpy
import re
from datetime import datetime
from pathlib import Path
from ..utils import extract_from_filename, open_directory_in_explorer


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

def set_properties(scene: bpy.types.Scene, mode):
    for prop, settings in scene_properties.items():
            if getattr(scene, prop, None) is None and (prop_type := getattr(settings, "type", None)) != "LOD":
                if prop_type == "LOD":
                    if mode != "DEFAULT":
                        boolean = mode == "LOW"
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
        set_properties(context.scene, mode="LOW")
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
        set_properties(scene, self.mode)

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
            scene = context.scene
            camera = scene.camera.name
            render = scene.render

            # Store current render settings
            render_settings = {
                "filepath": context.scene.render.filepath,
                "image_settings": render.image_settings.file_format,
                "codec": render.ffmpeg.codec,
                "format": render.ffmpeg.format
            }

            root_folder = Path("c:/tmp/FOM/Playblast")
            filename = f"{seq}_{shot}_{task}_v{version}_{camera}" + ("-v" + datetime.now().strftime("%m%d_%H%M%S") if self.include_date else "") + '.mp4'
            render.filepath = (root_folder / filename).resolve().as_posix()
            render.image_settings.file_format = 'FFMPEG'
            render.ffmpeg.codec = 'H264'
            render.ffmpeg.format = 'MPEG4'
            try:
                bpy.ops.render.opengl(animation=True, write_still=True, view_context=True)
            finally:
                if self.open_folder:
                    open_directory_in_explorer(root_folder)
                render.filepath = render_settings["filepath"]
                render.image_settings.file_format = render_settings["image_settings"]
                render.ffmpeg.codec = render_settings["codec"]
                render.ffmpeg.format = render_settings["format"]

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

class ImportRenderTree(bpy.types.Operator):
    bl_idname = "animation.fom_import_render_tree"
    bl_label = "Import Render Tree"
    bl_description = "Import a render tree into the current scene"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # Placeholder for future implementation
        path = bpy.path.abspath("G:/Mon Drive/ENSI/01_E3/Film 1mn/02_PROD/assets/nodes/rendering.blend")
        node_name = "BASE_CONFO"

        ''' Checking the existence of an already created confo node '''
        node_groups = (ng for ng in context.blend_data.node_groups if ng.bl_idname == "ConfoTree")
        node_group = next(node_groups, None)
        if node_group is not None:
            if context.scene.get("active_confo_editor", None).name == node_group.name:
                self.report({"WARNING"}, f'{node_name} already set in scene.')
                return {"CANCELLED"}
            
            setattr(context.scene, "unattribut", node_group)
            self.report({"WARNING", f'Set "{node_group.name}" as active confo editor (found {len(node_groups)-1} other)'})
            return {"FINISHED"}
    

        ''' Appending base confo node group '''
        with bpy.data.libraries.load(path, link=False) as (data_from, data_to):
            if "BASE_CONFO" in data_from.node_groups:
                data_to.node_groups = ["BASE_CONFO"]
            else:
                self.report({'ERROR'}, f"'BASE_CONFO' node tree not found in {path}")
                return {'CANCELLED'}
        

        ''' Setting the node group as the scene active confo editor '''
        node_group : bpy.types.Node = data_to.node_groups[0]
        if hasattr(context.scene, "active_confo_editor"):
            context.scene.active_confo_editor = context.blend_data.node_groups.get("BASE_CONFO")
        
        ''' Renaming the confo node group according to the filename nomenclature. '''
        if context.blend_data.is_saved:
            extract = extract_from_filename(Path(context.blend_data.filepath).name)
            if extract is not None:
                seq, shot = extract.groups()[:2]
                node_group.name = f'CONFO_{seq}_{shot}'


        ''' Setting it as the active node group tree for every confo editor areas.'''
        for workspace in context.blend_data.workspaces:
            for screen in workspace.screens:
                for area in screen.areas:
                    if area.type == "NODE_EDITOR" and area.ui_type == "ConfoTree":
                        for space in area.spaces:
                            if space.type == "NODE_EDITOR":
                                space : bpy.types.SpaceNodeEditor
                                space.pin = True
                                space.node_tree = node_group

        return {'FINISHED'}