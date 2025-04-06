import bpy

def draw_collection_row(collection, menu, index=0):
    row = menu.row()
    row.label(text='-'*index + collection.name)
    editable = (collection.override_library or collection.library) is not None
    row.prop(collection.fom_layout_manager, "visibility", text="")
    for child in collection.children:
        draw_collection_row(child, menu, index+1)

class FOMCollectionPropertyGroup(bpy.types.PropertyGroup):
    visibility: bpy.props.EnumProperty(items=[
        ("inherit", "Inherit", ""),
        ("active", "Active", ""),
        ("exclude", "Exclude", ""),
        ("mask_holdout", "Mask_holdout", ""),
        ("mask", "Mask", ""),
        ("holdout", "Holdout", "")
    ], name="Visibility", default=0)

    show_children: bpy.props.BoolProperty(default=False)

class FOMCollectionManagerPanel(bpy.types.Panel):
    bl_label = "FOM Layout Manager"
    bl_idname = "COLLECTION_PT_fom_layout_manager"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        if collection:
            layout.prop(collection.fom_layout_manager, "visibility")

class FOMLayoutManagerPanel(bpy.types.Panel):
    bl_label = "FOM Layout Manager"
    bl_idname = "VIEW3D_PT_fom_layout_manager"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Layout Manager"

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        if collection:
            draw_collection_row(collection, layout)
            pass


def register():
    bpy.types.Collection.fom_layout_manager = bpy.props.PointerProperty(
        type=FOMCollectionPropertyGroup,
        name="FOM Layout Manager",
        description="Custom layout manager for collections"
    )
    bpy.types.LayerCollection.foobar = bpy.props.BoolProperty(default=True)

def unregister():
    del bpy.types.Collection.fom_layout_manager
    del bpy.types.LayerCollection.foobar