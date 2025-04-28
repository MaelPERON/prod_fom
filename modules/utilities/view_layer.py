import bpy

def traverse_tree(t,i=0):
    yield (t,i)
    for child in t.children:
        yield from traverse_tree(child,i+1)

view_layer = bpy.context.view_layer
collections = traverse_tree(bpy.context.layer_collection)
collections = sorted(collections, key=lambda x: x[1])

for coll, index in collections:
    print(coll.name)
    coll.exclude = False

pass