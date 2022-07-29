from types import NoneType
import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb
import bpy, mathutils

# List to store target's avaliable props
prop_list = []


def update_list(context, target):
    # Reset list and append avaliable properties
    prop_list.clear()
    rhubarb = context.object.rhubarb
    for prop_name, _ in target.items():
        # if GPencil find TimeOffset modifier's offset property
        if rhubarb.obj_modes != "timeoffset":
            if "int" in str(type(target[f"{prop_name}"])) or "float" in str(
                type(target[f"{prop_name}"])
            ):
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


def mode_options_generator(self, context):
    obj_enum = (
        "obj",
        "Object",
        "Keyframe integer or float property on any object's data",
        "OBJECT_DATA",
        1,
    )
    bone_enum = (
        "bone",
        "Bone",
        "Keyframe integer or float property on any bone in Pose Mode",
        "BONE_DATA",
        2,
    )
    timeoffset_enum = (
        "timeoffset",
        "TimeOffset",
        "Directly keyframe time offset modifier",
        "MOD_TIME",
        3,
    )

    if (
        context.active_object.type == "GPENCIL"
        and context.object.grease_pencil_modifiers.items() != []
    ):
        mode_items = [
            obj_enum,
            timeoffset_enum,
        ]
        return mode_items
    if context.active_object.type == "ARMATURE":
        mode_items = [
            obj_enum,
            bone_enum,
        ]
        return mode_items
    else:
        mode_items = [
            obj_enum,
        ]
        return mode_items


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
        rhubarb = context.active_object.rhubarb
        if rhubarb.obj_modes == "bone":
            prop_list.clear()
            bone = sc.bone_selection
            target = obj.pose.bones["{0}".format(bone)]
            update_list(context, target)
            return target
        if (
            rhubarb.obj_modes == "timeoffset"
            and obj.grease_pencil_modifiers.items() != []
        ):
            prop_list.clear()
            target = obj.grease_pencil_modifiers
            update_list(context, target)
            return target
        else:
            target = obj
            prop_list.clear()
            update_list(context, target)
            return target

    def draw(self, context):
        # Panel Definitions
        sc = context.scene
        obj = context.object
        rhubarb = context.active_object.rhubarb
        layout = self.layout

        # Display active object name
        layout.label(text=f"Active Object: {obj.name}")  # TODO Improve this.
        row = layout.row(align=True)
        row.prop(rhubarb, "obj_modes", text="Object Mode", toggle=True)

        # if obj is Armature select a bone to target
        if rhubarb.obj_modes == "bone":
            layout.prop_search(sc, "bone_selection", obj.data, "bones", text="Bone")
        row = layout.row()
        # Load and Select Properties

        if rhubarb.presets == "":
            row.alert = True
            row.label(text="No avaliable properties", icon="ERROR")
        row.prop(
            rhubarb,
            "presets",
            text="",
        )

        # row.operator("rhubarb.enum_get", text="Load Properties")

        # User editable Mouth Definitions
        col = layout.column()
        col.prop(rhubarb, "mouth_a", text="Mouth A (MBP)")
        col.prop(rhubarb, "mouth_b", text="Mouth B (EE/etc)")
        col.prop(rhubarb, "mouth_c", text="Mouth C (E)")
        col.prop(rhubarb, "mouth_d", text="Mouth D (AI)")
        col.prop(rhubarb, "mouth_e", text="Mouth E (O)")
        col.prop(rhubarb, "mouth_f", text="Mouth F (WQ)")
        col.prop(rhubarb, "mouth_g", text="Mouth G (FV)")
        col.prop(rhubarb, "mouth_h", text="Mouth H (L)")
        col.prop(rhubarb, "mouth_x", text="Mouth X (rest)")

        # Set Rhubarb Executable depencies
        row = layout.row(align=True)
        row.prop(rhubarb, "sound_file", text="Sound file")
        row = layout.row(align=True)
        row.prop(rhubarb, "dialog_file", text="Dialog file")
        row = layout.row()
        row.prop(rhubarb, "start_frame", text="Start frame")

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
    presets: bpy.props.EnumProperty(
        items=enum_items_generator, name="Select Target Property"
    )

    obj_modes: bpy.props.EnumProperty(
        name="Select mode",
        items=mode_options_generator,
        description="Run Rhubarb Lipsync in",
    )


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
