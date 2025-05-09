import bpy
import re

cache_file_name = "prop_pant_01-static.abc.001"
search_name = re.sub(r"(.*)(\.abc)(.*$)", r"\1\2", cache_file_name)
cache_file = bpy.context.blend_data.cache_files.get(cache_file_name, None)
pass