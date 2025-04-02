import bpy
import json
import os

def save_render_settings(filepath):
    scene = bpy.context.scene
    render = scene.render

    settings = {
        "resolution_x": render.resolution_x,
        "resolution_y": render.resolution_y,
        "resolution_percentage": render.resolution_percentage,
        "image_settings": {
            "file_format": render.image_settings.file_format,
            "color_mode": render.image_settings.color_mode,
            "color_depth": render.image_settings.color_depth,
            "compression": render.image_settings.compression,
        },
        "fps": scene.render.fps,
        "fps_base": scene.render.fps_base,
        "filepath": render.filepath,
        "ffmpeg": {
            "format": render.ffmpeg.format,
            "codec": render.ffmpeg.codec,
            "audio_codec": render.ffmpeg.audio_codec,
            "video_bitrate": render.ffmpeg.video_bitrate,
            "audio_bitrate": render.ffmpeg.audio_bitrate,
            "gopsize": render.ffmpeg.gopsize,
            "max_b_frames": render.ffmpeg.max_b_frames,
            "use_lossless_output": render.ffmpeg.use_lossless_output,
        }
    }

    with open(filepath, 'w') as f:
        json.dump(settings, f, indent=4)

    print(f"Render settings saved to {filepath}")

# Example usage
output_path = os.path.join(os.path.dirname(__file__), "../json/render_settings.json")
save_render_settings(output_path)