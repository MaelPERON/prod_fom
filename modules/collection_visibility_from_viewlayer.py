import bpy

def collection_tree(layer_collection, parent=None, index=0):
    coll = layer_collection.collection
    obj = {"collection": coll, "parent": parent, "index": index}

    if hasattr(coll, "fom_layout_manager"):
        obj["visibility"] 

    for child in layer_collection.children:
        yield from collection_tree(child, layer_collection, index+1)

for obj in collection_tree(bpy.context.view_layer.layer_collection):
    coll = obj["collection"]
    print(coll.collection.fom_layout_manager)