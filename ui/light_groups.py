import bpy
from ..operators.light_groups import ForceSceneUpdateLightGroups

bpy.types.ViewLayer.lightgroups_list = bpy.props.StringProperty(default="",description="Light groups list, coma separated.")

def draw_custom_menu(self, context):
    layout : bpy.types.UILayout = self.layout
    layout.separator()
    layout.operator(ForceSceneUpdateLightGroups.bl_idname, text="Update Light Groups", icon='LIGHT_SUN')
    layout.prop(context.view_layer, "lightgroups_list", text="Synced Light Groups")

def register():
    bpy.types.CYCLES_RENDER_PT_passes_lightgroups.append(draw_custom_menu)

def unregister():
    bpy.types.CYCLES_RENDER_PT_passes_lightgroups.remove(draw_custom_menu)