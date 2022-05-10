import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb


class RhubarbLipsyncPanel(bpy.types.Panel):
    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AI Lipsync"
    bl_label = "Controller AI Lipsync"
    bl_context = "posemode"

    def draw(self, context):

        layout = self.layout

        prop = context.object.rhubarb

        row = layout.row()
        row.operator(operator="object.rhubarb_lipsync_storemouths")
        row.operator(operator="object.rhubarb_lipsync_defemouths")
        row = layout.row()
        row.menu("OBJECT_MT_select_test")

        col = layout.column()
        col.prop(prop, "mouth_a", text="Mouth A (MBP)")
        col.prop(prop, "mouth_b", text="Mouth B (EE/etc)")
        col.prop(prop, "mouth_c", text="Mouth C (E)")
        col.prop(prop, "mouth_d", text="Mouth D (AI)")
        col.prop(prop, "mouth_e", text="Mouth E (O)")
        col.prop(prop, "mouth_f", text="Mouth F (WQ)")
        col.prop(prop, "mouth_g", text="Mouth G (FV)")
        col.prop(prop, "mouth_h", text="Mouth H (L)")
        col.prop(prop, "mouth_x", text="Mouth X (rest)")

        row = layout.row(align=True)
        row.prop(prop, "sound_file", text="Sound file")

        row = layout.row(align=True)
        row.prop(prop, "dialog_file", text="Dialog file")

        row = layout.row()
        row.prop(prop, "start_frame", text="Start frame")

        row = layout.row()

        if not (context.preferences.addons[__package__].preferences.executable_path):
            row.label(
                text="Please set rhubarb executable location in addon preferences"
            )
            row = layout.row()

        row.operator(operator="object.rhubarb_lipsync")


# Panel now stores all values in the same property group but it is not in pose mode Next step is to clean up the operator.


class MouthShapesProperty(bpy.types.PropertyGroup):
    mouth_a: bpy.props.IntProperty(name="moutha")
    mouth_b: bpy.props.IntProperty(name="mouthb")
    mouth_c: bpy.props.IntProperty(name="mouthc")
    mouth_d: bpy.props.IntProperty(name="mouthd")
    mouth_e: bpy.props.IntProperty(name="mouthe")
    mouth_f: bpy.props.IntProperty(name="mouthf")
    mouth_g: bpy.props.IntProperty(name="mouthg")
    mouth_h: bpy.props.IntProperty(name="mouthh")
    mouth_x: bpy.props.IntProperty(name="mouthx")
    # Made these into integer values, but they are still connected the mouth shapes because the operator calles line 85

    sound_file: bpy.props.StringProperty(name="sound_file", subtype="FILE_PATH")
    dialog_file: bpy.props.StringProperty(name="dialog_file", subtype="FILE_PATH")
    stored_mouths: bpy.props.IntVectorProperty(name="stored_mouths", size=9)
    default_mouths: bpy.props.IntVectorProperty(name="default_mouths", size=9)
    start_frame: bpy.props.IntProperty(name="start_frame")


class BasicMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout
        prop1 = context.object.rhubarb
        layout.prop(prop1, "stored_mouths", text="text")


def register():
    bpy.utils.register_class(MouthShapesProperty)
    bpy.utils.register_class(RhubarbLipsyncPanel)
    bpy.utils.register_class(BasicMenu)

    bpy.types.Action.mouth_shapes = bpy.props.PointerProperty(type=MouthShapesProperty)
    bpy.types.Object.rhubarb = bpy.props.PointerProperty(type=MouthShapesProperty)

    # swap this out for the one in the screenshop and replicate changes in to op
    # A collection of F-Curves for animation  = Returns a new pointer property definition. This is the line that the operator calls


def unregister():
    bpy.utils.unregister_class(MouthShapesProperty)
    bpy.utils.unregister_class(RhubarbLipsyncPanel)
    bpy.utils.unregister_class(BasicMenu)
