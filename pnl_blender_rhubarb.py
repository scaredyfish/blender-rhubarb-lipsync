import bpy
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

        col = layout.column()
        col.prop(context.object.pose_library, 'mouth_a', "Mouth A")
        col.prop(context.object.pose_library, 'mouth_b', "Mouth B")
        col.prop(context.object.pose_library, 'mouth_c', "Mouth C")
        col.prop(context.object.pose_library, 'mouth_d', "Mouth D")
        col.prop(context.object.pose_library, 'mouth_e', "Mouth E")
        col.prop(context.object.pose_library, 'mouth_f', "Mouth F")
        col.prop(context.object.pose_library, 'mouth_g', "Mouth G")
        col.prop(context.object.pose_library, 'mouth_h', "Mouth H")
        col.prop(context.object.pose_library, 'mouth_x', "Mouth X")

        row = layout.row()
        row.operator(operator = "object.rhubarb_lipsync")

pose_markers = []

def pose_markers_items(self, context):
    """Dynamic list of items for Object.pose_libs_for_char."""

    lib = bpy.context.object.pose_library

    if not context or not context.object:
        return []

    pose_markers = [(marker, marker, 'Poses', '', idx) for idx, marker in enumerate(lib.pose_markers.keys())]
    print(pose_markers)
    return pose_markers

def register():
    bpy.utils.register_class(RhubarbLipsyncPanel)

    poses = bpy.props.EnumProperty(
        items=pose_markers_items,
        name='Poses',
        description='Poses',
    )

    bpy.types.Action.mouth_a = poses
    bpy.types.Action.mouth_b = poses
    bpy.types.Action.mouth_c = poses
    bpy.types.Action.mouth_d = poses
    bpy.types.Action.mouth_e = poses
    bpy.types.Action.mouth_f = poses
    bpy.types.Action.mouth_g = poses
    bpy.types.Action.mouth_h = poses
    bpy.types.Action.mouth_x = poses



def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncPanel)