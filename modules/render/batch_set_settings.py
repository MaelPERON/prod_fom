import bpy

for scene in bpy.data.scenes:
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 25
    scene.render.film_transparent = True
    scene.cycles.samples = 128
    scene.cycles.use_denoising = True
    scene.cycles.use_auto_tile = False
    scene.cycles.tile_size = 512
    scene["low_chain"] = False

    for cam in [obj for obj in scene.objects if obj.type == "CAMERA"]:
        cam.data.dof.use_dof = False