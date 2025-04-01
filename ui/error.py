import bpy
from ..utils import refresh_areas
from bpy.path import display_name
from bpy.types import SpaceView3D

draw_handle = None
drawed = False

errors = {
    "sync_mode": False 
}

def draw_modal_viewport():
    import gpu
    from gpu_extras.batch import batch_for_shader

    context = bpy.context
    region = context.region

    shader = gpu.shader.from_builtin('UNIFORM_COLOR')
    gpu.state.blend_set("ALPHA")
    vertices = (
        (0, 0),
        (region.width, 0),
        (region.width, region.height),
        (0, region.height),
    )
    indices = ((0, 1, 2), (2, 3, 0))
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)

    # shader.bind()
    shader.uniform_float("color", (1.0, 0.0, 0.0, 0.1))  # Red with transparency
    batch.draw(shader)
    gpu.state.blend_set("NONE")
    refresh_areas()

class VIEW3D_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Listed Errors"
    bl_idname = "VIEW3D_MT_custom_menu"

    @classmethod
    def poll(cls, context):
        global drawed
        return drawed

    def draw(self, context):
        layout = self.layout

        global errors
        for error, state in errors.items():
            if state:
                layout.label(text=display_name(error))


def check_error() -> float:
    global errors
    global drawed
    errors["sync_mode"] = bpy.context.scene.sync_mode != "FRAME_DROP"

    filepath = bpy.context.blend_data.filepath
    if "sequences" not in filepath:
        return None

    if any(errors.values()):
        show_error()
        drawed = True
        return 0.1
    elif drawed:
        clear_error()

    return 1

def clear_error():
    global draw_handle
    refresh_areas()
    if draw_handle is not None:
        bpy.types.SpaceView3D.draw_handler_remove(draw_handle, "WINDOW")
        draw_handle = None
    drawed = False

def show_error():
    global draw_handle

    if draw_handle is not None:
        return
    
    draw_handle = bpy.types.SpaceView3D.draw_handler_add(
        draw_modal_viewport, (), 'WINDOW', 'POST_PIXEL'
    )

def draw_custom_menu(self, context):
    global drawed
    layout = self.layout
    if drawed: 
        layout.menu(VIEW3D_MT_CustomMenu.bl_idname)

def register():
    bpy.app.timers.register(
        check_error, first_interval=0, persistent=True
    )
    bpy.types.VIEW3D_HT_header.append(draw_custom_menu)

def unregister():
    bpy.app.timers.unregister(check_error)
    
    bpy.types.VIEW3D_HT_header.remove(draw_custom_menu)
