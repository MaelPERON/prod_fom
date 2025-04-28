import bpy
import re

pattern = r"(LGT-)?(.*)$"
auto_light_linking = {
	"rim_bdt": ["CHARACTERS"],
	"rim_chara": ["CHARACTERS"],
	"rim_bdt_props": ["CHARACTERS","PROPS"],
	"rim_props": ["PROPS"],
	"rim_extras": ["LAYOUT_EXTRAS"],
	"rim_setdress": ["SETDRESSING"],
	"rim_four": ["Four"]
}

def get_ll_name(ll_group: str): return f"LL {ll_group.upper()}"

def get_ll_collection(ll_group: str):
	return bpy.context.blend_data.collections.get(get_ll_name(ll_group), None)

def find_collections(lighting_collection : bpy.types.Collection):
	collections : list[bpy.types.Collection] = lighting_collection.children_recursive
	print(f"Processing {len(collections)} collections in {lighting_collection.name}...")
	for coll in collections:
		print(f"Checking collection: {coll.name}")
		if (search := re.search(pattern, coll.name)) is not None:
			LL_group = search.group(2) # Lighting Linking Group Name
			print(f"Pattern matched. LL_group: {LL_group}")
			LL_coll = get_ll_collection(LL_group)

			collections : bpy.types.BlendDataCollections = bpy.context.blend_data.collections

			if LL_coll is None: # Création groupe light linking
				print(f"{LL_group} group not found. Creating new group...")
				LL_coll = collections.new(name=get_ll_name(LL_group))
				print(f"\tCreated {LL_coll.name}.")
				if (coll_list := auto_light_linking.get(LL_group.lower(), None)):
					for coll_child_name in coll_list:
						print(f"\tLooking for child collection: {coll_child_name}")
						coll_child : bpy.types.Collection = collections.get(coll_child_name, None)
						if not coll_child:
							print(f"\t\t{coll_child_name} not found!")	
							continue
						LL_coll.children.link(coll_child)
						print(f"\t\tAdded {coll_child.name}")
				else:
					print(f"{LL_group} not in auto light linking's list.")
					continue

			# Setting link states
			print(f"Setting link states for {LL_coll.name}...")
			for light_child in [coll.light_linking for coll in LL_coll.collection_children]:
				light_child.link_state = "INCLUDE"

			# Attribution groupe light linking
			print(f"{LL_group}: Applying light linking to objects...")
			for obj in coll.objects:
				print(f"\tApplying light linking to object: {obj.name}")
				LL_obj = obj.light_linking
				LL_obj.blocker_collection = LL_coll
				LL_obj.receiver_collection = LL_coll
	
		else:
			print(f"No pattern match for {coll.name}")

lighting_collection = bpy.context.blend_data.collections.get("LIGHTING")
find_collections(lighting_collection)
