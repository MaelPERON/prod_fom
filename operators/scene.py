import bpy
import re

class ExportPlaybast(bpy.types.Operator):
    bl_idname= "scene.export_playbast"
    bl_label = "Export Playbast"
    bl_description = "Export the current scene for playblast"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(self, context):
        return context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        return {'FINISHED'}