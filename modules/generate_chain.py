import bpy

for obj in bpy.data.objects:
    if obj.name.startswith("TEMP_"):
        bpy.data.objects.remove(obj, do_unlink=True)
chain_path = bpy.data.objects.get("BASE_CHAIN_PATH")
chain = bpy.data.objects.get("BASE_CHAIN")

node_trim = bpy.data.node_groups.get("TRIM_CURVE")
node_tailor = bpy.data.node_groups.get("TAILOR_CURVE")

if chain_path:
    new_chain_path = chain_path.copy()
    new_chain_path.data = chain_path.data.copy()
    new_chain_path.name = "TEMP_path"
    bpy.context.collection.objects.link(new_chain_path)
    new_chain_path.select_set(True)
    bpy.context.view_layer.objects.active = new_chain_path
    mod = new_chain_path.modifiers.new("Trim", "NODES")
    mod.node_group = node_trim
    mod["Socket_2"] = 1.5


if chain:
    new_chain = chain.copy()
    new_chain.data = chain.data.copy()
    new_chain.name = "TEMP_chain"
    bpy.context.collection.objects.link(new_chain)
    mod = new_chain.modifiers.new("Tailor", "NODES")
    mod.node_group = node_tailor
    mod["Socket_2"] = new_chain_path
    bpy.context.view_layer.objects.active = new_chain
    bpy.ops.object.select_all(action='DESELECT')
    new_chain.select_set(True)
    bpy.ops.object.convert(target='MESH')

    bpy.ops.object.convert(target='CURVE')
    new_chain.data.resolution_u = 24
    for spline in new_chain.data.splines:
        spline.type = 'BEZIER'
        for point in spline.bezier_points:
            point.handle_left_type = 'AUTO'
            point.handle_right_type = 'AUTO'

    mod = new_chain.modifiers.new("Curve", "CURVE")
    mod.object = new_chain_path
    mod.deform_axis = "POS_Z"

# Create a new armature
bpy.ops.object.armature_add(enter_editmode=True, location=new_chain_path.location)
armature = bpy.context.object
armature.name = "TEMP_armature"

# Add a root bone
bpy.ops.armature.bone_primitive_add(name="Root")
root_bone = armature.data.edit_bones["Bone"]
root_bone.name = "Root"
root_bone.head = (0, 0, 0)
root_bone.tail = (0.5, 0, 0)
root_bone.roll = 0

# Exit edit mode
bpy.ops.object.mode_set(mode='OBJECT')