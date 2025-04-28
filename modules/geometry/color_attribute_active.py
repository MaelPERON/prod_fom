import bpy

color_attribute = "Color"

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        if (attribute := obj.data.color_attributes.get(color_attribute)) is not None:
            obj.data.attributes.active_color = attribute
            print(f"+ Set active color attribute '{color_attribute}' on object '{obj.name}'.")
        else:
            print(f"- Color attribute '{color_attribute}' not found in object '{obj.name}'.")