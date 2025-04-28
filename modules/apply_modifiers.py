import bpy

def apply_modifiers():
    # Get all selected objects
    selected_objects = bpy.context.selected_objects

    for obj in selected_objects:
        if obj.type == 'MESH':  # Ensure the object is a mesh
            # Apply modifiers in stack order
            for modifier in obj.modifiers:
                if modifier.type != "ARMATURE":
                    continue
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.modifier_apply(modifier=modifier.name)

# Run the function
apply_modifiers()