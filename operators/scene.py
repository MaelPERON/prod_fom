import bpy
import re
from datetime import datetime
from ..utils import extract_from_filename, open_directory_in_explorer


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