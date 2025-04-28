import bpy

def find_collection(layer_collection, name):
    if layer_collection.collection.name == name:
        yield layer_collection
    for child_collection in layer_collection.children:
        yield from find_collection(child_collection, name)

def iterate_collection_children(collection: bpy.types.LayerCollection):
	for child in collection.children:
		child.exclude = False
		iterate_collection_children(child)

coll = next(find_collection(bpy.context.view_layer.layer_collection, "SETDRESSING"), None)

if coll is not None:
	iterate_collection_children(coll)

# if coll:
# 	iterate_collection_children(coll)