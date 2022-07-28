from types import NoneType
import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb
import bpy, mathutils

# List to store target's avaliable props
prop_list = []


def update_list(obj, target):
    # Reset list and append avaliable properties
    prop_list.clear()
    for prop_name, _ in target.items():
        # if GPencil find TimeOffset modifier's offset property
        if obj.grease_pencil_modifiers.items() == []:
            if "int" in str(type(target[f"{prop_name}"])):
                prop_list.append((prop_name, prop_name, prop_name))
        else:
            # else find INT properties on selected bone
            prop_list.append((prop_name, prop_name, prop_name))


# Generate list of items from target's props
def enum_items_generator(self, context):
    enum_items = []
    for e, d in enumerate(prop_list):
        enum_items.append((d[0], d[0], d[0], e))
    return enum_items


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

    @classmethod
    def poll(cls, context: bpy.types.Context):
        global prop_list
        sc = context.scene
        obj = context.object
        bone = sc.bone_selection
        if obj.type == "ARMATURE":
            prop_list.clear()
            bone = sc.bone_selection
            target = obj.pose.bones["{0}".format(bone)]
            update_list(obj, target)
            return target
        if obj.type == "GPENCIL" and obj.grease_pencil_modifiers.items() != []:
            prop_list.clear()
            target = obj.grease_pencil_modifiers
            update_list(obj, target)
            return target
        else:
            target = obj
            prop_list.clear()
            update_list(obj, target)
            return target

    def draw(self, context):
        # Panel Definitions
        sc = context.scene
        obj = context.object
        prop = context.object.rhubarb
        layout = self.layout

        # Display active object name
        layout.label(text=f"Active Object: {obj.name}")  # TODO Improve this.

        # if obj is Armature select a bone to target
        if obj.type == "ARMATURE":
            layout.prop_search(sc, "bone_selection", obj.data, "bones", text="Bone")

        # Load and Select Properties
        row = layout.row(align=True)
        # row.operator("rhubarb.enum_get", text="Load Properties")
        row.prop(prop, "presets", text="")

        # User editable Mouth Definitions
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

        # Button to execute rhubarb operation
        row = layout.row()
        row.operator(operator="object.rhubarb_lipsync")


class pgrp_blender_rhubarb(bpy.types.PropertyGroup):
    """definitions for rhubarb properties"""

    # Mouth shape properties
    # TODO these are all set to zero because user must manually initilize them.
    mouth_a: bpy.props.IntProperty(name="moutha", default=0)
    mouth_b: bpy.props.IntProperty(name="mouthb", default=0)
    mouth_c: bpy.props.IntProperty(name="mouthc", default=0)
    mouth_d: bpy.props.IntProperty(name="mouthd", default=0)
    mouth_e: bpy.props.IntProperty(name="mouthe", default=0)
    mouth_f: bpy.props.IntProperty(name="mouthf", default=0)
    mouth_g: bpy.props.IntProperty(name="mouthg", default=0)
    mouth_h: bpy.props.IntProperty(name="mouthh", default=0)
    mouth_x: bpy.props.IntProperty(name="mouthx", default=0)

    # rhubarb executable dependcies
    sound_file: bpy.props.StringProperty(name="sound_file", subtype="FILE_PATH")
    dialog_file: bpy.props.StringProperty(name="dialog_file", subtype="FILE_PATH")
    start_frame: bpy.props.IntProperty(name="start_frame")
    presets: bpy.props.EnumProperty(items=enum_items_generator, name="Position Preset")


ctr = [
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
