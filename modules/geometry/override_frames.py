import bpy
from math import *

coll = bpy.context.blend_data.collections.get("Simulation")


for obj in coll.objects:
    if obj.name.startswith("PATRON"):
        for mod in obj.modifiers:
            if mod.type == "MESH_SEQUENCE_CACHE":
                cache: bpy.types.CacheFile = mod.cache_file
                if cache is not None:
                    cache.override_frame = True
                    driver = cache.driver_add("frame").driver
                    driver.expression = f"var"
                    while driver.variables:
                        driver.variables.remove(driver.variables[0])

                    var = driver.variables.new()
                    var.name = "var"
                    var.type = "CONTEXT_PROP"
                    # var.targets[0].id_type = 'SCENE'
                    # var.targets[0].id = bpy.context.scene
                    var.targets[0].context_property = 'ACTIVE_SCENE'
                    var.targets[0].data_path = '["FOM_sim_frame"]'