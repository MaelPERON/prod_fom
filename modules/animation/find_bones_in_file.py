import bpy

bone_name = "MCH-ground"

def find_bone_named_mch_ground():
    global bone_name
    result = []
    for obj in bpy.data.objects:
        if obj.type == 'ARMATURE':
            armature = obj.data
            if bone_name in armature.bones:
                result.append((obj.name, obj.is_library_indirect, obj.library))
    return result

# Example usage
found_objects = find_bone_named_mch_ground()
print(f"Objects with '{bone_name}' bone:", found_objects)