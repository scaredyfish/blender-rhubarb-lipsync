from distutils.util import execute
import enum
from operator import index
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


class RhubarbLipsyncOperator(bpy.types.Operator):
    """Run Rhubarb lipsync"""

    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = "Mouth_"
    hold_frame_threshold = 4

    def modal(self, context, event):

        wm = context.window_manager
        wm.progress_update(50)
        user_input = context.object.rhubarb.presets

        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            try:
                result = json.loads(stderr)
                if result["type"] == "progress":
                    print(result["log"]["message"])
                    self.message = result["log"]["message"]

                if result["type"] == "failure":
                    self.report(type={"ERROR"}, message=result["reason"])
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
                obj = context.object
                last_frame = 0
                prev_pose = 0
                bone = bpy.data.scenes["Scene"].bone_selection
                user_data_path = context.object.rhubarb.presets
                bone_path = obj.pose.bones["{0}".format(bone)]
                for cue in results["mouthCues"]:
                    frame_num = round(cue["start"] * fps) + obj.rhubarb.start_frame
                    if frame_num - last_frame > self.hold_frame_threshold:
                        print(
                            "hold frame: {0}".format(
                                frame_num - self.hold_frame_threshold
                            )
                        )
                        bone_path["{0}".format(user_data_path)] = prev_pose
                        self.set_keyframes(
                            context, frame_num - self.hold_frame_threshold
                        )

                    print(
                        "start: {0} frame: {1} value: {2}".format(
                            cue["start"], frame_num, cue["value"]
                        )
                    )

                    mouth_shape = "mouth_" + cue["value"].lower()
                    if mouth_shape in context.object.rhubarb:
                        pose_index = context.object.rhubarb[mouth_shape]
                        print(pose_index)
                    else:
                        pose_index = 0

                    bone_path["{0}".format(user_data_path)] = pose_index
                    self.set_keyframes(context, frame_num)

                    prev_pose = pose_index
                    last_frame = frame_num

                    wm.progress_end()
                return {"FINISHED"}

            return {"PASS_THROUGH"}
        except subprocess.TimeoutExpired as ex:
            return {"PASS_THROUGH"}
        except json.decoder.JSONDecodeError:
            print(stdout)
            print("Error!!!")
            wm.progress_end()
            return {"CANCELLED"}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            print(template.format(type(ex).__name__, ex.args))
            wm.progress_end()
            return {"CANCELLED"}

    def set_keyframes(self, context, frame):
        obj = context.object
        bone = bpy.data.scenes["Scene"].bone_selection
        user_data_path = context.object.rhubarb.presets
        bone_path = obj.pose.bones["{0}".format(bone)]
        bone_path.keyframe_insert(
            data_path='["{0}"]'.format(user_data_path),
            frame=frame,  # CHANGE THIS PATH TO BE USER EDITABLE
        )
        context.object.animation_data.action.fcurves[-1].keyframe_points[
            -1
        ].interpolation = "CONSTANT"

    def invoke(self, context, event):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        inputfile = bpy.path.abspath(context.object.rhubarb.sound_file)
        dialogfile = bpy.path.abspath(context.object.rhubarb.dialog_file)
        recognizer = bpy.path.abspath(addon_prefs.recognizer)
        executable = bpy.path.abspath(addon_prefs.executable_path)
        # This is ugly, but Blender unpacks the zip without execute permission
        os.chmod(executable, 0o744)

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


class StoreMouthValues(bpy.types.Operator):

    bl_idname = "object.rhubarb_lipsync_storemouths"
    bl_label = "Store Rhubarb Mouths"
    """For testing purposes. Save mouth 'definitions' for rhubarb lipsync"""

    def execute(self, context):
        obj = context.object
        save = obj.rhubarb.stored_mouths
        a = obj.rhubarb.mouth_a
        b = obj.rhubarb.mouth_b
        c = obj.rhubarb.mouth_c
        d = obj.rhubarb.mouth_d
        e = obj.rhubarb.mouth_e
        f = obj.rhubarb.mouth_f
        g = obj.rhubarb.mouth_g
        h = obj.rhubarb.mouth_h
        x = obj.rhubarb.mouth_x
        MouthList = [a, b, c, d, e, f, g, h, x]
        for x, mouths in enumerate(MouthList):
            save[x] = MouthList[x]
            print(save[x])
        return {"FINISHED"}


class DefMouthValues(bpy.types.Operator):

    bl_idname = "object.rhubarb_lipsync_defemouths"
    bl_label = "Define Rhubarb Mouths"
    """For Testing purposes. Load saved mouth 'definitions' from rhubarb lipsync"""

    def execute(self, context):
        obj = context.object
        read = obj.rhubarb.stored_mouths
        obj.rhubarb.mouth_a = read[0]
        obj.rhubarb.mouth_b = read[1]
        obj.rhubarb.mouth_c = read[2]
        obj.rhubarb.mouth_d = read[3]
        obj.rhubarb.mouth_e = read[4]
        obj.rhubarb.mouth_f = read[5]
        obj.rhubarb.mouth_g = read[6]
        obj.rhubarb.mouth_h = read[7]
        obj.rhubarb.mouth_x = read[8]
        for x in read:
            print(str(x))
        return {"FINISHED"}


def register():
    bpy.utils.register_class(RhubarbLipsyncOperator)
    bpy.utils.register_class(StoreMouthValues)
    bpy.utils.register_class(DefMouthValues)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncOperator)
    bpy.utils.unregister_class(StoreMouthValues)
    bpy.utils.unregister_class(DefMouthValues)


if __name__ == "__main__":
    register()
