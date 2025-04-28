import bpy


def get_light_groups(view_layer: bpy.types.ViewLayer) -> list[str]:
    return [lg.name for lg in view_layer.lightgroups]

def set_light_groups(view_layer: bpy.types.ViewLayer, light_groups: list[str], light_groups_list: str | None = None):
    filter = light_groups_list.lower().split(",") if light_groups_list else None
    for lg in light_groups:
        if lg not in view_layer.lightgroups:
            if light_groups_list is None or lg.lower() in filter:
                view_layer.lightgroups.add(name=lg)


class ForceSceneUpdateLightGroups(bpy.types.Operator):
    bl_idname = "fom.scene_update_light_groups"
    bl_label = "Update Light Groups"
    bl_description = "Update light groups in the current view layer"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        light_groups = []
        for vl in context.scene.view_layers:
            if vl.name != context.view_layer.name:
                light_groups.extend(get_light_groups(vl))

        view_layer = context.view_layer

        set_light_groups(view_layer, light_groups, view_layer.lightgroups_list)
        return {'FINISHED'}