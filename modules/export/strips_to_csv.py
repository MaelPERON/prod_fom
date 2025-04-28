import bpy
import csv  # Add import for csv module
C = bpy.context
D = bpy.data
from mathutils import *
from math import *
from pathlib import Path

colors = [
	"FF0000",  # Red
	"FFA500",  # Orange
	"FFFF00",  # Yellow
	"008000",  # Green
	"0000FF",  # Blue
	"800080",  # Purple
	"FFC0CB",  # Pink
	"A52A2A",  # Brown
	"808080"   # Gray
]

area = [area for area in bpy.context.screen.areas if area.type == "DOPESHEET_EDITOR"][0]
sequences = bpy.context.selected_sequences
sequences.sort(key=lambda el: el.frame_final_start)
seq_set = set([seq.name[0:2] for seq in sequences])
scene = bpy.context.scene
markers = scene.timeline_markers
with bpy.context.temp_override(area=area):
	for mark in markers:
		markers.remove(mark)
	# for seq in sequences:
	# 	scene.timeline_markers.new(name=seq.name,frame=seq.frame_final_start)
# print('\n'.join(seq.name for seq in sequences))
print(seq_set, len(seq_set))

# Create CSV file
with open(Path(__file__).parent / "markers.csv", mode='w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["Start", "Name", "Length", "Color"])
	# writer.writerow(["Start", "Name", "Length", "Color", "Frames"])
	for seq in sequences:
		position = seq.frame_final_start / scene.render.fps
		frames = (seq.frame_final_end - seq.frame_final_start)
		length = frames / scene.render.fps
		color = '' if seq.color_tag == "NONE" else colors[int(seq.color_tag[-2:])-1]
		writer.writerow([float(position), seq.name, float(length), color])
		# writer.writerow([float(position), seq.name, float(length), color, frames])