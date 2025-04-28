import bpy
import json
import os
from pathlib import Path

asset_path = Path("G:/Mon Drive/ENSI/01_E3/Film 1mn/02_PROD/assets")
sequence_path = Path("G:/Mon Drive/ENSI/01_E3/Film 1mn/02_PROD/sequences")

def save_version_to_json(json_folder: Path):
	filepath = bpy.data.filepath
	if not filepath:
		print("No blend file is currently opened.")
		return

	filepath = Path(filepath)

	# Load existing data from the JSON file if it exists
	json_file_path = (json_folder / "versions.json")
	if json_file_path.exists():
		with open(json_file_path.resolve().as_posix(), "r") as json_file:
			try:
				existing_data = json.load(json_file)
				json_file.close()
			except json.JSONDecodeError:
				existing_data = {}
	else:
		existing_data = {}

	def compare(path_a: Path, path_b: Path) -> bool:
		path_a = path_a.resolve().as_posix()
		path_b = path_b.resolve().as_posix()
		print(path_a, path_b)
		return path_a in path_b

	is_asset = compare(asset_path, filepath)
	is_shot = compare(sequence_path, filepath)

	group_name = "asset" if is_asset else ("shot" if is_shot else "unknow")

	existing_data[filepath.name] = {
		"version": bpy.data.version,
		"type": group_name,
		"filepath": filepath.as_posix()
	}

	with open(json_file_path.resolve().as_posix(), "w") as json_file:
		json.dump(existing_data, json_file, indent=4)
		json_file.close()

	print(f"Version information saved to {json_file_path}\n\n\n\n\n\n\n")

root_path = Path(__file__).parent / "../json/"
save_version_to_json(root_path)