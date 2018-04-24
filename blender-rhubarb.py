import bpy
from bpy.props import IntProperty, FloatProperty
import io
import sys
import subprocess
from threading  import Thread
from queue import Queue, Empty
import json


class RhubarbLipsync(bpy.types.Operator):
    """Move an object with the mouse, example"""
    bl_idname = "object.rhubarb_lipsync"
    bl_label = "Rhubarb lipsync"

    def modal(self, context, event):
        try:
            (stdout, stderr) = self.rhubarb.communicate(timeout=1)

            if stdout:
                results = json.loads(stdout)
                #print(results)
                if results['mouthCues']:
                    for cue in results['mouthCues']:
                        fps = bpy.context.scene.render.fps

                        # get_pose_from_cue()
                        # set_time()
                        # bpy.ops.poselib.apply_pose(pose_index=self.pose_index)
                        print("start: {0} frame: {1} value: {2}".format(cue['start'], cue['start']*fps ,cue['value']))

            return {'FINISHED'}
        except Exception as e:
            # print("Exception: " + e.Message)
            return {'PASS_THROUGH'}



    def invoke(self, context, event):
        inputfile = "D:/Cloud/OneDrive/rhubarb/67703__acclivity__alphabet-male.wav"
        self.rhubarb = subprocess.Popen("D:/Cloud/OneDrive/rhubarb/rhubarb.exe -f json --machineReadable %s" % inputfile,
                                   stdout=subprocess.PIPE, universal_newlines=True)

        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, context.window)

        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}



    def finished(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)



def register():
    bpy.utils.register_class(RhubarbLipsync)


def unregister():
    bpy.utils.unregister_class(RhubarbLipsync)


if __name__ == "__main__":
    register()

