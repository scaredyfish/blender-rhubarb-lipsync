from distutils.util import execute
import enum
import bpy
from bpy import types
from bpy.props import IntProperty, FloatProperty
import blf
import bgl
import io
import sys
import select
import subprocess
from threading import Thread, local
from queue import Queue, Empty
import json
import os
from .core import get_target, debugger


class RHUBARB_OT_Execute_Rhubarb_Lipsync(bpy.types.Operator):
    """Run Rhubarb lipsync"""

    bl_idname = "rhubarb.execute_rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = "Mouth_"
    hold_frame_threshold = 4

    @classmethod
    def poll(cls, context: bpy.types.Context):
        rhubarb = context.window_manager.rhubarb_panel_settings
        if rhubarb.obj_modes == "":
            cls.poll_message_set(f"Select a Target Type")
            return
        if not context.active_object:
            cls.poll_message_set(f"Ensure there is an Active Object")
            return
        if rhubarb.obj_modes == "bone" and context.active_object.type != "ARMATURE":
            cls.poll_message_set(f"Active object is not an Armature")
            return
        if rhubarb.presets == "":
            cls.poll_message_set(f"Select an avaliable Property")
            return
        if not (rhubarb.sound_file or rhubarb.sound_file):
            cls.poll_message_set(f"Select  Sound/Dialogue File")
            return
        return True

    def set_keyframes_on_target(self, obj, target, rhubarb, frame_num, set_pose):
        prop_name = rhubarb.presets
        if rhubarb.obj_modes != "timeoffset":
            target["{0}".format(prop_name)] = set_pose
            self.set_keyframe(target, rhubarb, frame_num - self.hold_frame_threshold)
        else:
            set_pose = target[f"{prop_name}"].offset = set_pose
            self.set_keyframe(target, rhubarb, frame_num - self.hold_frame_threshold)
        obj.animation_data.action.fcurves[-1].keyframe_points[
            -1
        ].interpolation = "CONSTANT"

    def modal(self, context, event):
        wm = context.window_manager
        rhubarb = wm.rhubarb_panel_settings
        target, obj = get_target(context)

        wm.progress_update(50)
        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            try:
                result = json.loads(stderr)
                if result["type"] == "progress":
                    debugger(result["log"]["message"])
                    self.message = result["log"]["message"]

                if result["type"] == "failure":
                    self.report(type={"ERROR Type Failure"}, message=result["reason"])
                    return {"CANCELLED"}

            except ValueError:
                pass
            except TypeError:
                pass
            except json.decoder.JSONDecodeError:
                pass

            self.rhubarb.poll()

            if self.rhubarb.returncode is not None:
                wm.event_timer_remove(self._timer)
                results = json.loads(stdout)
                fps = context.scene.render.fps
                last_frame = 0
                prev_pose = 0

                # Logic for Armature or GPencil obj
                for cue in results["mouthCues"]:
                    frame_num = round(cue["start"] * fps) + rhubarb.start_frame
                    if frame_num - last_frame > self.hold_frame_threshold:
                        debugger(
                            "hold frame: {0}".format(
                                frame_num - self.hold_frame_threshold
                            )
                        )
                        # Set prev_pose for Armature or GPencil obj
                        self.set_keyframes_on_target(
                            obj, target, rhubarb, frame_num, prev_pose
                        )

                    debugger(
                        "start: {0} frame: {1} value: {2}".format(
                            cue["start"], frame_num, cue["value"]
                        )
                    )

                    mouth_shape = "mouth_" + cue["value"].lower()
                    if mouth_shape in rhubarb:
                        pose_index = rhubarb[mouth_shape]
                    else:
                        pose_index = 0

                    # Set pose_index for Armature or GPencil obj
                    self.set_keyframes_on_target(
                        obj, target, rhubarb, frame_num, pose_index
                    )
                    prev_pose = pose_index
                    last_frame = frame_num

                    wm.progress_end()
                self.report({"INFO"}, f"Rhubarb Lipsync Complete on '{obj.name}'")
                return {"FINISHED"}

            return {"PASS_THROUGH"}
        except subprocess.TimeoutExpired as ex:
            return {"PASS_THROUGH"}
        except json.decoder.JSONDecodeError:
            debugger(stdout)
            wm.progress_end()
            self.report({"ERROR"}, "Error!!! Json Decoder")
            return {"CANCELLED"}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            self.report({"ERROR"}, template.format(type(ex).__name__, ex.args))
            wm.progress_end()
            return {"CANCELLED"}

    def set_keyframe(self, target, rhubarb, frame):
        data_path = rhubarb.presets
        key_name = f'["{data_path}"]'
        if rhubarb.obj_modes == "timeoffset":
            key_name = "offset"
            target = target.get(data_path)

        # Keyframe target
        target.keyframe_insert(
            data_path=key_name,
            frame=frame,
        )

    def invoke(self, context, event):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        inputfile = bpy.path.abspath(
            context.window_manager.rhubarb_panel_settings.sound_file
        )
        dialogfile = bpy.path.abspath(
            context.window_manager.rhubarb_panel_settings.dialog_file
        )
        recognizer = bpy.path.abspath(addon_prefs.recognizer)
        executable = bpy.path.abspath(addon_prefs.executable_path)
        # This is ugly, but Blender unpacks the zip without execute permission
        try:
            os.chmod(executable, 0o744)
        except FileNotFoundError:
            self.report(
                {"ERROR"},
                f"CHECK EXECUTABLE PATH IN ADDON PREFERENCES. \n Rhubarb Executable not found at {executable}.",
            )

        # Lines that need to be excuted before the modal operator can go below this comment.

        command = [
            executable,
            "-f",
            "json",
            "--machineReadable",
            "--extendedShapes",
            "GHX",
            "-r",
            recognizer,
            inputfile,
        ]

        if dialogfile:
            command.append("--dialogFile")
            command.append(dialogfile)
        wm = context.window_manager
        self.rhubarb = subprocess.Popen(
            command, stdout=subprocess.PIPE, universal_newlines=True
        )

        wm = context.window_manager
        self._timer = wm.event_timer_add(2, window=context.window)

        wm.modal_handler_add(self)

        wm.progress_begin(0, 100)

        return {"RUNNING_MODAL"}

    def execute(self, context):
        return self.invoke(context, None)

    def finished(self, context):
        context.scene.frame_set(context.scene.frame_current + 1)
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


classes = (RHUBARB_OT_Execute_Rhubarb_Lipsync,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
