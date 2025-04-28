import bpy

def copy_color_attributes_from_active():
    active_obj = bpy.context.view_layer.objects.active
    selected_objects = bpy.context.selected_objects

    if not active_obj or active_obj not in selected_objects:
        print("No active object or active object not in selection.")
        return

    if not hasattr(active_obj.data, "color_attributes"):
        print("Active object has no color attributes.")
        return

    active_color_attributes = active_obj.data.color_attributes

    for obj in selected_objects:
        if obj == active_obj or not hasattr(obj.data, "color_attributes"):
            continue

        for color_attr in active_color_attributes:
            if color_attr.name not in obj.data.color_attributes:
                new_attr = obj.data.color_attributes.new(
                    name=color_attr.name,
                    type="FLOAT_COLOR",
                    domain=color_attr.domain
                )

copy_color_attributes_from_active()