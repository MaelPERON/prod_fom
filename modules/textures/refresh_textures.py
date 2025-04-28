import bpy

def refresh_textures():
    for image in bpy.data.images:
        if image.name.startswith("T_"):
            image.reload()
            print(f"Refreshed: {image.name}")

# Call the function
refresh_textures()