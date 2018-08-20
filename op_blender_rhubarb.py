import bpy
from bpy.props import IntProperty, FloatProperty
import io
import sys
import subprocess
from threading  import Thread
from queue import Queue, Empty
import json


class RhubarbLipsyncOperator(bpy.types.Operator):
    """Run Rhubarb lipsync"""
    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    cue_prefix = 'Mouth_'

    @classmethod
    def poll(cls, context):
        return context.selected_pose_bones

    def modal(self, context, event):
        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            if stdout:
                wm = context.window_manager
                wm.event_timer_remove(self._timer)

                results = json.loads(stdout)
                fps = context.scene.render.fps
                lib = context.object.pose_library

                if not results['mouthCues']: return

                for cue in results['mouthCues']:
                    print("start: {0} frame: {1} value: {2}".format(cue['start'], cue['start'] * fps , cue['value']))

                    pose_index = context.object.pose_library.mouth_shapes['mouth_' + cue['value'].lower()]

                    frame_num = round(cue['start'] * fps) + context.object.pose_library.mouth_shapes.start_frame


                    bpy.ops.poselib.apply_pose(pose_index=pose_index)
     
                    
                    for bone in context.selected_pose_bones:
                        bone.keyframe_insert(data_path='location', frame=frame_num)
                        if bone.rotation_mode == 'QUATERNION':
                            bone.keyframe_insert(data_path='rotation_quaternion', frame=frame_num)
                        else:
                            bone.keyframe_insert(data_path='rotation_euler', frame=frame_num)
                        bone.keyframe_insert(data_path='scale', frame=frame_num)


                return {'FINISHED'}
        except subprocess.TimeoutExpired as ex:
            return {'PASS_THROUGH'}
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            print(template.format(type(ex).__name__, ex.args))
            return {'CANCELLED'}


    def invoke(self, context, event):
        user_preferences = context.user_preferences
        addon_prefs = user_preferences.addons[__package__].preferences

        inputfile = context.object.pose_library.mouth_shapes.sound_file
        dialogfile = context.object.pose_library.mouth_shapes.dialog_file
        if dialogfile:
            dialog = "--dialogFile %s" % dialogfile
        else:
            dialog = ""

        executable = bpy.path.abspath(addon_prefs.executable_path)
        self.rhubarb = subprocess.Popen("%s -f json --machineReadable %s --extendedShapes GHX %s"
                                        % (executable, dialog, inputfile),
                                        stdout=subprocess.PIPE, universal_newlines=True)

        wm = context.window_manager
        self._timer = wm.event_timer_add(1, context.window)

        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}



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

