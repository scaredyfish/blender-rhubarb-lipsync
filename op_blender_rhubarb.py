import bpy
from bpy.props import IntProperty, FloatProperty
import blf
import bgl
import io
import sys
import select
import subprocess
from threading import Thread
from queue import Queue, Empty
import json
import os
from mathutils import Matrix


class RhubarbLipsyncOperator(bpy.types.Operator):
    """Run Rhubarb lipsync"""
    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = 'Mouth_'
    hold_frame_threshold = 4

    @classmethod
    def poll(cls, context):
        return context.preferences.addons[__package__].preferences.executable_path and \
            context.selected_pose_bones and \
            context.object.pose_library.mouth_shapes.sound_file

    def modal(self, context, event):
        wm = context.window_manager
        wm.progress_update(50)

        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            try:
                result = json.loads(stderr)
                if result['type'] == 'progress':
                    print(result['log']['message'])
                    self.message = result['log']['message']

                if result['type'] == 'failure':
                    self.report(type={'ERROR'}, message=result['reason'])
                    return {'CANCELLED'}

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
                lib = context.object.pose_library
                last_frame = 0
                prev_pose = context.object.pose_library.mouth_shapes["mouth_x"]

                for cue in results['mouthCues']:
                    frame_num = round(cue['start'] * fps) + lib.mouth_shapes.start_frame
                    

                    # add hold key if time since last key is large
                    if frame_num - last_frame > self.hold_frame_threshold:
                        print("hold frame: {0}".format(frame_num- self.hold_frame_threshold))
                        self.apply_pose(context, frame_num - self.hold_frame_threshold, bpy.data.actions[prev_pose])

                    print("start: {0} frame: {1} value: {2}".format(cue['start'], frame_num , cue['value']))

                    mouth_shape = 'mouth_' + cue['value'].lower()
                    if mouth_shape in context.object.pose_library.mouth_shapes:
                        pose_index = context.object.pose_library.mouth_shapes[mouth_shape]
                    else:
                        pose_index = context.object.pose_library.mouth_shapes["mouth_x"]

                    
                    self.apply_pose(context, frame_num - self.hold_frame_threshold, bpy.data.actions[pose_index])

                    prev_pose = pose_index
                    last_frame = frame_num
                    wm.progress_end()
                return {'FINISHED'}

            return {'PASS_THROUGH'}
        except subprocess.TimeoutExpired as ex:
            return {'PASS_THROUGH'}
        except json.decoder.JSONDecodeError:
            print(stdout)
            print("Error!!!")
            wm.progress_end()
            return {'CANCELLED'}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            print(template.format(type(ex).__name__, ex.args))
            wm.progress_end()
            return {'CANCELLED'}

    def apply_pose(self, context, frame, pose):
        bpy.context.scene.frame_set(frame)

        print(pose)

        context.object.pose.apply_pose_from_action(action=pose,evaluation_time=frame)

        for i in pose.fcurves:
            i.evaluate(frame)
            context.object.pose.bones[i.data_path.split("\"")[1]].keyframe_insert(data_path=i.data_path.split("]")[1].replace(".",""), frame=frame)

    def invoke(self, context, event):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        inputfile = bpy.path.abspath(context.object.pose_library.mouth_shapes.sound_file)
        dialogfile = bpy.path.abspath(context.object.pose_library.mouth_shapes.dialog_file)
        recognizer = bpy.path.abspath(addon_prefs.recognizer)
        executable = bpy.path.abspath(addon_prefs.executable_path)

        # This is ugly, but Blender unpacks the zip without execute permission
        os.chmod(executable, 0o744)

        command = [executable, "-f", "json", "--machineReadable", "--extendedShapes", "GHX", "-r", recognizer, inputfile]

        if dialogfile:
            command.append("--dialogFile")
            command.append(dialogfile)

        self.rhubarb = subprocess.Popen(command,
                                        stdout=subprocess.PIPE, universal_newlines=True)

        wm = context.window_manager
        self._timer = wm.event_timer_add(2, window=context.window)

        wm.modal_handler_add(self)

        wm.progress_begin(0, 100)

        return {'RUNNING_MODAL'}

    def execute(self, context):
        return self.invoke(context, None)

    def finished(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def register():
    bpy.utils.register_class(RhubarbLipsyncOperator)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsyncOperator)


if __name__ == "__main__":
    register()
