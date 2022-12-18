from types import NoneType
import bpy
from bpy_extras.io_utils import ImportHelper
import bpy, mathutils

mouth_shapes = (
    "mouth_a",
    "mouth_b",
    "mouth_c",
    "mouth_d",
    "mouth_e",
    "mouth_f",
    "mouth_g",
    "mouth_h",
    "mouth_x",
)

# List to store target's avaliable props
prop_list = []


def initlize_props(rig_settings):
    """Integer Properties must be initilized if they are not already set to a value
    NOTE: Default value on prop doesn't return as integer until user resets integer to default."""
    # if a single setting is set do not initilie props
    initilized = True
    for index, mouth in enumerate(mouth_shapes):
        if not rig_settings.get(mouth):
            initilized = False
    if initilized:
        return

    for index, mouth in enumerate(mouth_shapes):
        if not rig_settings.get(mouth):
            rig_settings[mouth] = index


def debugger(msg):
    print(f"Blender Rhubarb Lip Sync: {msg}")


def get_target(context):
    sc = context.scene
    obj = context.active_object
    rhubarb = context.window_manager.rhubarb_panel_settings
    if rhubarb.obj_modes == "bone" and obj.type == "ARMATURE":
        return obj.pose.bones.get(sc.bone_selection), obj
    if rhubarb.obj_modes == "timeoffset":
        target = obj.grease_pencil_modifiers
        return target, obj
    else:
        target = context.object
        return target, obj


def refresh_target(context):
    prop_list.clear()
    target, object = get_target(context)
    if target:
        update_list(context.window_manager.rhubarb_panel_settings, target)
    return object


def update_list(rhubarb_settings, target):
    # Reset list and append avaliable properties
    for prop_name, _ in target.items():
        # if GPencil find TimeOffset modifier's offset property
        if rhubarb_settings.obj_modes != "timeoffset":
            if "int" in str(type(target[f"{prop_name}"])) or "float" in str(
                type(target[f"{prop_name}"])
            ):
                prop_list.append((prop_name, prop_name, prop_name))
        else:
            # else find INT properties on selected bone
            prop_list.append((prop_name, prop_name, prop_name))
