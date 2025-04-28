import bpy

# Ensure an armature is selected and in pose mode
if bpy.context.object and bpy.context.object.type == 'ARMATURE' and bpy.context.object.mode == 'POSE':
    object = bpy.context.object
    armature = object.data
    collections = armature.collections_all
    for bone in object.pose.bones:
        prefix = bone.name.split("-")[0]  # Get the first three letters of the bone name
        collection = collections.get(prefix)
        if collection is not None:
            collection.assign(bone)
            print(f"Bone '{bone.name}' assigned to group '{prefix}'")
        else:
            print(f"Collection {prefix} doesn't exist.")
else:
    print("Please select an armature and switch to Pose Mode.")