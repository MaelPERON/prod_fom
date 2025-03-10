import bpy

from ..operators.asset_manager import OpenAssetFolder

def AssetMenu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OpenAssetFolder.bl_idname, text="Open Asset Folder")

def register():
    bpy.types.ASSETBROWSER_MT_context_menu.append(AssetMenu)

def unregister():
    bpy.types.ASSETBROWSER_MT_context_menu.remove(AssetMenu)