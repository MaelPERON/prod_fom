import bpy

C = bpy.context
D = bpy.data

bone = C.active_pose_bone

bone["$seconds"] = int(24*60*60)