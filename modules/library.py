import bpy

# Path to the .blend file
blend_file_path = r"G:\Mon Drive\ENSI\01_E3\Film 1mn\02_PROD\assets\props\poulie\work\fom-props-model-poulie-v001.blend"

# Collection name to link

def get_rig(coll):
	for obj in coll.all_objects:
		if obj.type == "ARMATURE":
			return obj

collection_name = "PS-poulie.000"
setdress_collection = bpy.data.collections["SETDRESSING"]

def delete_instances(collection=None):
	for coll in collection.children:
		setdress_collection.children.unlink(coll)

	if not collection:
		collection = bpy.context.scene.collection
	
	bpy.data.orphans_purge(do_recursive=True)

def load_instances(collection=None):
	with bpy.data.libraries.load(blend_file_path, link=True) as (data_from, data_to):
		if collection_name in data_from.collections and collection_name not in data_to.collections:
			data_to.collections.append(collection_name)

	if not collection:
		collection = bpy.context.scene.collection

	for coll in data_to.collections:
		if coll.name == collection_name:
			for i in range(10):
				print(f"Creating instance {i}...")
				override_collection = coll.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer, do_fully_editable=True)
				bpy.context.scene.collection.children.unlink(override_collection)
				bpy.data.collections["SETDRESSING"].children.link(override_collection)

def instance_init(override_collection, i):
	rig = get_rig(override_collection)
	rig.location.x = i%10 * 2
	rig.location.y = i//10 * 2

delete_instances(setdress_collection)
load_instances(setdress_collection)