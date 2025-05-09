import bpy
from pathlib import Path

coll = bpy.data.collections.get("Clothes")

for obj in coll.objects:
    for mod in obj.modifiers:
        if mod.type == "MESH_SEQUENCE_CACHE":
            mod : bpy.types.MeshSequenceCacheModifier
            cache : bpy.types.CacheFile = mod.cache_file
            path = Path(cache.filepath)
            cache.filepath = path.as_posix().replace("Users/m.peron/", "")