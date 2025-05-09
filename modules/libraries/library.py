import bpy
import random
from math import radians
from pathlib import Path
import re

# Path to the .blend file
blend_file_path = r"G:\Mon Drive\ENSI\01_E3\Film 1mn\02_PROD\assets\props\poulie\work\fom-props-model-poulie-v001.blend"

# Collection name to link

def replace_last_terminal_line(message):
    print("\033[F\033[K" + message, end="\r")

def add_cache_file(file: Path, adding=False):
	if file.exists() and file.is_file():
		if (cache_file := bpy.context.blend_data.cache_files.get(file.name, None)) is None or adding:
			bpy.ops.cachefile.open("EXEC_REGION_WIN", filepath=file.resolve().as_posix())
			cache_files = (cache for cache in bpy.context.blend_data.cache_files if file.name in cache.name)
			cache_file = next(reversed(list(cache_files)), None)
			if cache_file is not None:
				cache_file.use_fake_user = not adding
		return cache_file
	return None

def import_cache_files(cache_folder):
	for file in reversed(list(cache_folder.iterdir())):
		if file.is_file() and file.name.endswith(".abc"):
			add_cache_file(file, False)

def get_cache_name(cache_file_name):
	'''
		:return: cache_file_name
		'''
	return re.sub(r"(.*)(\.abc)(.*$)", r"\1\2", cache_file_name)

def get_cache_file(cache_file_name):
	'''
		:return: cache_file
		'''
	search_name = get_cache_name(cache_file_name)
	return bpy.context.blend_data.cache_files.get(search_name, None)

def set_driver(cache: bpy.types.CacheFile, rig: bpy.types.Object, animated : bool = False):
	if cache is None or rig is None:
		return print("No Cache file or Armature found")
	cache.override_frame = True
	cache.object_paths
	
	''' Creating the driver, its expression and variables '''
	driver = cache.driver_add("frame").driver
	while driver.variables:
		driver.variables.remove(driver.variables[0])
	
	if animated:
		driver.expression = "f"
		
		f = driver.variables.new()
		f.type = "SINGLE_PROP"
		f.name = "f"
		f.targets[0].id = rig
		f.targets[0].data_path = f'pose.bones["root"]["frame"]'
	else:
		driver.expression = f"(frame*0.75)-(frame*0.75)%2"

def get_rig(coll):
	for obj in coll.all_objects:
		if obj.type == "ARMATURE":
			return obj
		
def is_animated(cache_name, rig):
	if (search := re.search(r"^(\w*)[_\-](\w*)[_\-](\d{2,})[_\-](static|chute)\.abc(\.\d{1,})?$", cache_name)) is not None:
		root_bone = rig.pose.bones.get("root")
		groups = search.groups()
		part, index, anim = groups[1], int(groups[2]), groups[3] == "chute"
		if anim and root_bone["animated"] == 1 and root_bone[part]+1 == index:
			# print(f"Found animation for {cache_name}")
			return True
	return False

setdress_collection = bpy.data.collections["SETDRESSING"]

def delete_instances(collection=None):
	for coll in collection.children:
		if coll.name.startswith("PS-poulie"):
			setdress_collection.children.unlink(coll)

	if not collection:
		collection = bpy.context.scene.collection
	
	bpy.data.orphans_purge(do_recursive=True)
	for instancer in instancers:
		instancer.hide_viewport = False

def load_instances(collection=None, collection_name="PS-poulie.000", iterations=0, chance : float = None):
	global ACTIONS
	with bpy.data.libraries.load(blend_file_path, link=True) as (data_from, data_to):
		if collection_name in data_from.collections and collection_name not in data_to.collections:
			data_to.collections.append(collection_name)

		for action in data_from.actions:
			print("Loading action:", action)
			if action.startswith("A_"):
				data_to.actions.append(action)
		

	ACTIONS = {action.name: action for action in data_to.actions}

	if not collection:
		collection = bpy.context.scene.collection


	for coll in data_to.collections:
		if coll.name == collection_name:
			for i in range(iterations):
				if chance is None or random.random() < chance  :
					print(f"Creating instance {i}...")
					override_collection = coll.override_hierarchy_create(bpy.context.scene, bpy.context.view_layer, do_fully_editable=True)
					bpy.context.scene.collection.children.unlink(override_collection)
					bpy.data.collections["SETDRESSING"].children.link(override_collection)
					instance_init(override_collection, i)

def instance_init(override_collection, i):
	global hide_instancer
	rig = get_rig(override_collection)
	instancer = instancers[i]
	if hide_instancer:
		instancer.hide_viewport = True
	rig.location.x = instancer.location.x
	rig.location.y = instancer.location.y
	rig.rotation_euler[2] = instancer.rotation_euler[2]

	if rig:
		# Regular pose bone settings
		pose_bone = rig.pose.bones.get("TWEAK-bout")
		if pose_bone:
			random_offset = random.uniform(15, 33)
			pose_bone.location.y += random_offset/10

		root = rig.pose.bones.get("root")
		root["pant"] = random.randint(0,2)
		root["shirt"] = random.randint(0,2)
		root["helmet_pos"] = random.randint(0,3)
		root["helmet"] = random.random() >= 0.5

		panier = rig.pose.bones.get("TWEAK-panier")
		angle = random.uniform(-20, 20) if random.random() < 0.5 else random.uniform(160, 200)
		panier.rotation_euler[1] = radians(angle)

		# Setting all the needed actions for the rig
		# anim_data = rig.animation_data
		# for track in anim_data.nla_tracks:
		# 	anim_data.nla_tracks.remove(track)

		# for track_name, action_name in TRACKS.items():
		# 	action = actions.get(action_name, None)
		# 	if action:
		# 		track = anim_data.nla_tracks.new()
		# 		track.name = track_name
		# 		strip = track.strips.new(f"{i}_{action_name}", 1, action)
		# 		strip.blend_type = "REPLACE"
		# 		strip.extrapolation = "HOLD"

def modify_instances(collection=None, col_prefix="RIG-", edit_rig = True):
	if not collection:
		collection = bpy.context.scene.collection

	global cache_mode

	print("Modifying instances...")
	for coll in collection.children:
		if coll.name.startswith(col_prefix):
			for obj in coll.all_objects:
				if obj.type == "ARMATURE" and edit_rig:
					rig = obj
					print(f"Modifying {rig.name}...")
					modify_rig(rig)
					continue
				if obj.type == "MESH":
					rig = obj.parent
					animated = is_animated(obj.name, rig)
					cache_file = add_cache_file(cache_folder_path / get_cache_name(obj.name), True) if animated else get_cache_file(obj.name)
					if cache_file is not None and cache_mode != "pass":
						for mod in obj.modifiers:
							if mod.type == "MESH_SEQUENCE_CACHE":
								obj.modifiers.remove(mod)
						if cache_mode == "none":
							print(f"No cache file for {obj.name}")
							continue
						print(f"({coll.name}) Adding cache file to {obj.name}...")
						mod = obj.modifiers.new(name="Cache File", type="MESH_SEQUENCE_CACHE")
						mod : bpy.types.MeshSequenceCacheModifier
						mod.cache_file = cache_file
						mod.object_path = re.sub(r"(.*)(\.\d{1,})$", r"\1", f'/{cache_file.name}')
						set_driver(cache_file, obj.parent, animated)
					continue
			else:
				continue

	print("Instance modified.")

def modify_rig(rig: bpy.types.Object):
	anim_data = rig.animation_data
	tracks = anim_data.nla_tracks
	height = tracks.get("HEIGHT")
	height.mute = True
	
	hauteur = rig.pose.bones.get("TWEAK-hauteur")
	if hauteur:
		hauteur.location.y = 3.6
	
	pose_bone = rig.pose.bones.get("TWEAK-bout")
	if pose_bone:
		random_offset = random.uniform(4.2, 6.9) # IT_01
		# random_offset = random.uniform(6.2 , 7) # IT_02
		# pose_bone.location.y = random_offset
		pass


	wind_tracks = [track for track in tracks if track.name.startswith("A_wind")]
	global already_set_wind
	if not already_set_wind:
		for wind_track in wind_tracks: 
			wind_track.mute = True

		if wind_tracks:
			track = random.choice(wind_tracks)
			# track.mute = False
	else:
		for track in wind_tracks:
			if track.mute == False:
				for strip in track.strips:
					for curve in strip.fcurves:
						for keyframe in curve.keyframe_points:
							curve.keyframe_points.remove(keyframe, fast=True) 
					strip.use_animated_influence = True
					strip.influence = random.uniform(0.1 , 0.2)
	
	# for track_name, action_name in TRACKS.items():
	# 	track = anim_data.nla_tracks.new()
	# 	track.name = track_name
	# 	action = ACTIONS.get(action_name, None)
	# 	print(action_name, action)

instancers = [obj for obj in bpy.context.scene.objects if "instancer" in obj.name]

hide_instancer = False
already_set_wind = False
cache_mode = "none" # none / set / pass
ACTIONS = {}
TRACKS = {
	"HEIGHT": "A_height",
}
cache_folder_path = Path("D:/Sims/FOM_HangingClothes/renamed")
# GENERATE = False
GENERATE = input("Generate instances? (y/n): ") == "y"

def main():
	import_cache_files(cache_folder_path)

	# chance = 1 # IT01
	chance = 0.5
	# chance = 1/10 # Testings
	if GENERATE:
		delete_instances(setdress_collection)
		load_instances(setdress_collection ,"PS-poulie.000", len(instancers), chance)

	# edit_rig = False
	edit_rig = input("Edit rig? (y/n): ") == "y"
	modify_instances(setdress_collection, "PS-poulie", edit_rig)

main()