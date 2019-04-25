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

        if context.object.pose_library:
            prop = context.object.pose_library.mouth_shapes

            col = layout.column()
            col.prop(prop, 'mouth_a', text="Mouth A (MBP)")
            col.prop(prop, 'mouth_b', text="Mouth B (EE/etc)")
            col.prop(prop, 'mouth_c', text="Mouth C (E)")
            col.prop(prop, 'mouth_d', text="Mouth D (AI)")
            col.prop(prop, 'mouth_e', text="Mouth E (O)")
            col.prop(prop, 'mouth_f', text="Mouth F (WQ)")
            col.prop(prop, 'mouth_g', text="Mouth G (FV)")
            col.prop(prop, 'mouth_h', text="Mouth H (L)")
            col.prop(prop, 'mouth_x', text="Mouth X (rest)")

            row = layout.row(align=True)
            row.prop(prop, 'sound_file', text='Sound file')

            row = layout.row(align=True)
            row.prop(prop, 'dialog_file', text='Dialog file')

            row = layout.row()
            row.prop(prop, 'start_frame', text='Start frame')

            row = layout.row()

            if not (context.preferences.addons[__package__].preferences.executable_path):
                row.label(text="Please set rhubarb executable location in addon preferences")
                row = layout.row()

            row.operator(operator = "object.rhubarb_lipsync")

        else:
            row = layout.row(align=True)
            row.label(text="Rhubarb Lipsync requires a pose library")


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
    mouth_a : poses
    mouth_b : poses
    mouth_c : poses
    mouth_d : poses
    mouth_e : poses
    mouth_f : poses
    mouth_g : poses
    mouth_h : poses
    mouth_x : poses

    sound_file : bpy.props.StringProperty(name="sound_file",subtype='FILE_PATH')
    dialog_file : bpy.props.StringProperty(name="dialog_file",subtype='FILE_PATH')

    start_frame : bpy.props.IntProperty(name="start_frame")

def register():
    bpy.utils.register_class(MouthShapesProperty)
    bpy.utils.register_class(RhubarbLipsyncPanel)

    bpy.types.Action.mouth_shapes = bpy.props.PointerProperty(type=MouthShapesProperty)


def unregister():
    bpy.utils.unregister_class(MouthShapesProperty)
    bpy.utils.unregister_class(RhubarbLipsyncPanel)