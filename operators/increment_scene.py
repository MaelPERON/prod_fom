import bpy
from os import path
from bpy.path import basename
import re
from ..utils import extract_from_filename

def increment_file(filepath, new_stage=None):
    work = path.dirname(filepath)
    name, ext = path.splitext(basename(filepath))
    
    if (match := extract_from_filename(name)):
        sequence_id, shot_id, stage, version = match.groups()
    else:
        return (-1, "Filename does not match the expected pattern.")
    

    if new_stage: stage = new_stage
    version = int(version) + 1

    new_filename = f"fom-seq_{sequence_id}-sh_{shot_id}-{stage}-v{version:03d}{ext}"
    new_filepath = path.join(work, new_filename)

    bpy.ops.wm.save_as_mainfile(filepath=new_filepath)

    return (1, new_filepath)


class IncrementSceneOperator(bpy.types.Operator):
    bl_idname = "scene.increment"
    bl_label = "Increment Scene"
    bl_description = "Increment the scene version"

    new_stage: bpy.props.StringProperty(default="",name="New Stage",description="New stage for the scene (layout, anim, lighting, etc.)")

    @classmethod
    def poll(self, context):
        return extract_from_filename(basename(context.blend_data.filepath)) is not None
    
    def execute(self, context):
        filepath = context.blend_data.filepath
        status, new_filepath = increment_file(filepath, self.new_stage)
        if status == 1:
            self.report({'INFO'}, f"File saved as {new_filepath}")
        else:
            self.report({'ERROR'}, new_filepath)
        return {'FINISHED'}
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "new_stage")