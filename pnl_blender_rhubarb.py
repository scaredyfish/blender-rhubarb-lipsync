import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb
import bpy, mathutils

"""Below are definitions for enumurated list of properties. 
List of properties will be used for fetching how many 
custom properties exist on a bone or object."""

prop_list = []


def enum_items_generator(self, context):
    enum_items = []
    for e, d in enumerate(prop_list):
        enum_items.append((d[0], d[0], d[0], e))
    return enum_items


def report(self, message):  # Just to report errors
    self.report({"ERROR"}, message)
    return {"CANCELLED"}


class enum_get_blender_rhubarb(bpy.types.Operator):
    """Operator for adding avaliable properties
    from bone to enum list for panel."""

    bl_idname = "rhubarb.enum_get"
    bl_label = "List rhubarb destination properties"
    bl_description = "Add new enum items to list for dropdown menu"

    def execute(self, context):
        # append bone properties to display in dropdown
        global prop_list
        sc = bpy.data.scenes["Scene"]
        obj = context.object
        bone = sc.bone_selection
        sc = bpy.data.scenes["Scene"]
        obj = context.object
        if sc.obj_selection:
            if sc.obj_selection.type == "ARMATURE":
                bone = sc.bone_selection
                bone_path = obj.pose.bones["{0}".format(bone)]
            else:
                bone_path = obj
        eea = context.object.rhubarb
        aob = context.view_layer.objects.active

        if aob == None:  # For case when there is no active object
            return report(self, "No active object selected!!!")

        prop_list.clear()
        for prop_name, _ in bone_path.items():
            prop_list.append((prop_name, prop_name, prop_name))
        return {"FINISHED"}


class pnl_blender_rhubarb(bpy.types.Panel):
    """Panel to control options of rhubarb operator"""

    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AI Lipsync"
    bl_label = "Controller AI Lipsync"

    # Pointer definitions
    bpy.types.Scene.obj_selection = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.bone_selection = bpy.props.StringProperty()

    def draw(self, context):
        sc = bpy.data.scenes["Scene"]
        obj = context.object
        prop = context.object.rhubarb
        layout = self.layout

        # Bone Selection Menu
        # https://gist.github.com/daylanKifky/252baea63eb0c39858e3e9b57f1af167
        layout.prop(sc, "obj_selection", text="")

        if sc.obj_selection:
            if sc.obj_selection.type == "ARMATURE":
                layout.prop_search(
                    sc, "bone_selection", sc.obj_selection.data, "bones", text="Bone"
                )

        # Dropdown of avaliable properties
        col = layout.column(align=True)
        eea = context.object.rhubarb
        row = layout.row()

        # Load and Select Properties
        row = col.row(align=True)
        row.operator("rhubarb.enum_get", text="Load Properties")
        row.prop(eea, "presets", text="")

        # Mouth Definitions
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

        # Set Rhubarb Executable depencies
        row = layout.row(align=True)
        row.prop(prop, "sound_file", text="Sound file")
        row = layout.row(align=True)
        row.prop(prop, "dialog_file", text="Dialog file")
        row = layout.row()
        row.prop(prop, "start_frame", text="Start frame")

        # Button to run rhubarb operator
        row = layout.row()
        row.operator(operator="object.rhubarb_lipsync")


class pgrp_blender_rhubarb(bpy.types.PropertyGroup):
    """definitions for rhubarb properties"""

    # Mouth shape properties
    mouth_a: bpy.props.IntProperty(name="moutha", default=1)
    mouth_b: bpy.props.IntProperty(name="mouthb", default=2)
    mouth_c: bpy.props.IntProperty(name="mouthc", default=3)
    mouth_d: bpy.props.IntProperty(name="mouthd", default=4)
    mouth_e: bpy.props.IntProperty(name="mouthe", default=5)
    mouth_f: bpy.props.IntProperty(name="mouthf", default=6)
    mouth_g: bpy.props.IntProperty(name="mouthg", default=7)
    mouth_h: bpy.props.IntProperty(name="mouthh", default=8)
    mouth_x: bpy.props.IntProperty(name="mouthx", default=9)

    # rhubarb executable dependcies
    sound_file: bpy.props.StringProperty(name="sound_file", subtype="FILE_PATH")
    dialog_file: bpy.props.StringProperty(name="dialog_file", subtype="FILE_PATH")
    start_frame: bpy.props.IntProperty(name="start_frame")

    # testing mouth def presets
    stored_mouths: bpy.props.IntVectorProperty(name="stored_mouths", size=9)

    # store avaliable props in enum
    presets: bpy.props.EnumProperty(items=enum_items_generator, name="Position Preset")


ctr = [
    enum_get_blender_rhubarb,
    pgrp_blender_rhubarb,
    pnl_blender_rhubarb,
]


def register():
    for cls in ctr:
        bpy.utils.register_class(cls)
    bpy.types.Object.rhubarb = bpy.props.PointerProperty(type=pgrp_blender_rhubarb)


def unregister():
    for cls in reversed(ctr):
        bpy.utils.unregister_class(cls)
