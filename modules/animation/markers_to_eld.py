import csv
from pathlib import Path
import re

class SecondsToTimecode:
	def __init__(self, seconds : float, fps=24):
		assert type(seconds) == float
		self.hours = seconds // 3600 + 1
		self.minutes = (seconds % 3600) // 60
		self.seconds = int(seconds) % 60
		self.frames = int((seconds % 1) * fps)

	def add(self, hours, minutes, seconds, frames):
		self.hours += hours
		self.minutes += minutes
		self.seconds += seconds
		self.frames += frames
		
		return self

	def __str__(self):
		return f"{int(self.hours):02}:{int(self.minutes):02}:{int(self.seconds):02}:{int(self.frames):02}"

def frames_to_timecode(frame, fps=24):
    """Convert frame number to timecode string HH:MM:SS:FF."""
    hours = frame // (3600 * fps) + 1
    minutes = (frame % (3600 * fps)) // (60 * fps)
    seconds = (frame % (60 * fps)) // fps
    frames = frame % fps
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def marker_string(index, name, start, duration, fps=24):
	output = "$INDEX  001      V     C        $IN $OUT $IN $OUT  \n |C:ResolveColorBlue |M:$NAME |D:$DURATION\n\n"
	source_in = SecondsToTimecode(float(start))
	replace_map = {
		"$INDEX": f'{index:03}',
		"$NAME": name,
		"$IN": str(source_in),
		"$OUT": str(source_in.add(0,0,0,1)),
		"$DURATION": round(float(duration)*fps)
	}

	for key, val in replace_map.items():
		output = re.sub(re.escape(key), str(val), output)
	return output

json = Path(__file__).parent / "../../json/"

def main():
	with open((json / "markers.edl").resolve().as_posix(), "w") as f:
		f.truncate(0)
		f.write("TITLE: Markers Exported\nFCM: NON-DROP FRAME\n")

		with open((json / "markers.csv").resolve().as_posix(), "r") as marker_file:
			reader = csv.DictReader(marker_file)
			markers = [row for row in reader]
			for i, row in enumerate(sorted(markers, key=lambda row: float(row["Start"]))):
				output = marker_string(i, row["Name"], row["Start"], row["Duration"])
				print(f"Writing marker {row['Name']} ///")
				f.write(output)
				print(f"\tWritten.")
main()