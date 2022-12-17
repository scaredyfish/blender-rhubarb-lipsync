from types import NoneType
import bpy
from bpy_extras.io_utils import ImportHelper
import bpy, mathutils

# List to store target's avaliable props
prop_list = []


def get_target(context):
    sc = context.scene
    obj = context.active_object
    rhubarb = context.window_manager.rhubarb_panel_settings
    if rhubarb.obj_modes == "bone":
        bone = sc.bone_selection
        target = obj.pose.bones.get(bone)
        return target, obj
    if rhubarb.obj_modes == "timeoffset":
        target = obj.grease_pencil_modifiers
        return target, obj
    else:
        target = context.object
        return target, obj
    return


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
