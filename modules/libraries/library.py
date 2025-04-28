import bpy
import random
from math import radians

# Path to the .blend file
blend_file_path = r"G:\Mon Drive\ENSI\01_E3\Film 1mn\02_PROD\assets\props\poulie\work\fom-props-model-poulie-v001.blend"

# Collection name to link

def replace_last_terminal_line(message):
    print("\033[F\033[K" + message, end="\r")

def get_rig(coll):
	for obj in coll.all_objects:
		if obj.type == "ARMATURE":
			return obj

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

def load_instances(collection=None, collection_name="PS-poulie.000", iterations=0):
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
				if random.random() < 1/2  :
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

def modify_instances(collection=None, col_prefix="RIG-"):
	if not collection:
		collection = bpy.context.scene.collection

	print("Modifying instances...")
	for coll in collection.children:
		if coll.name.startswith(col_prefix):
			for obj in coll.all_objects:
				if obj.type == "ARMATURE":
					rig = obj
					print(f"Modifying {rig.name}...")
					modify_rig(rig)
					break
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
		# random_offset = random.uniform(4.2, 6.9) # IT_01
		random_offset = random.uniform(6.2 , 7) # IT_02
		pose_bone.location.y = random_offset


	wind_tracks = [track for track in tracks if track.name.startswith("A_wind")]
	global already_set_wind
	if not already_set_wind:
		for wind_track in wind_tracks: 
			wind_track.mute = True

		if wind_tracks:
			track = random.choice(wind_tracks)
			track.mute = False
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
ACTIONS = {}
TRACKS = {
	"HEIGHT": "A_height",
}
 
already_set_wind = False
# delete_instances(setdress_collection)
# load_instances(setdress_collection ,"PS-poulie.000", len(instancers))
modify_instances(setdress_collection, "PS-poulie")