import bpy
from bpy_extras.io_utils import ImportHelper
from . import  op_blender_rhubarb

class RhubarbLipsyncPanel(bpy.types.Panel):
    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_label = "Rhubarb Lipsync"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (obj and obj.type == 'ARMATURE')


    def draw(self, context):
        layout = self.layout

        prop = context.object.pose_library.mouth_shapes

        col = layout.column()
        col.prop(prop, 'mouth_a', "Mouth A")
        col.prop(prop, 'mouth_b', "Mouth B")
        col.prop(prop, 'mouth_c', "Mouth C")
        col.prop(prop, 'mouth_d', "Mouth D")
        col.prop(prop, 'mouth_e', "Mouth E")
        col.prop(prop, 'mouth_f', "Mouth F")
        col.prop(prop, 'mouth_g', "Mouth G")
        col.prop(prop, 'mouth_h', "Mouth H")
        col.prop(prop, 'mouth_x', "Mouth X")

        row = layout.row(align=True)
        row.prop(prop, 'sound_file', text='Sound file')

        row = layout.row(align=True)
        row.prop(prop, 'dialog_file', text='Dialog file')

        row = layout.row()
        row.prop(prop, 'start_frame', text='Start frame')

        row = layout.row()
        row.operator(operator = "object.rhubarb_lipsync")



pose_markers = []

def pose_markers_items(self, context):
    """Dynamic list of items for Object.pose_libs_for_char."""

    lib = bpy.context.object.pose_library

    if not context or not context.object:
        return []

    pose_markers = [(marker, marker, 'Poses', '', idx) for idx, marker in enumerate(lib.pose_markers.keys())]
    return pose_markers

poses = bpy.props.EnumProperty(
    items=pose_markers_items,
    name='Poses',
    description='Poses',
)

class MouthShapesProperty(bpy.types.PropertyGroup):
    mouth_a = poses
    mouth_b = poses
    mouth_c = poses
    mouth_d = poses
    mouth_e = poses
    mouth_f = poses
    mouth_g = poses
    mouth_h = poses
    mouth_x = poses

    sound_file = bpy.props.StringProperty(name="sound_file",subtype='FILE_PATH')
    dialog_file = bpy.props.StringProperty(name="dialog_file",subtype='FILE_PATH')

    start_frame = bpy.props.IntProperty(name="start_frame")

def register():
    bpy.utils.register_class(MouthShapesProperty)
    bpy.utils.register_class(RhubarbLipsyncPanel)

    bpy.types.Action.mouth_shapes = bpy.props.PointerProperty(type=MouthShapesProperty)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncPanel)