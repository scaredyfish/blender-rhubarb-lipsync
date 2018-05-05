import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty

class RhubarbAddonPreferences(AddonPreferences):
    bl_idname = __package__

    executable_path = StringProperty(
            name="Rhubarb lipsync executable",
            subtype='FILE_PATH',
            )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "executable_path")

def register():
    bpy.utils.register_class(RhubarbAddonPreferences)


def unregister():
    bpy.utils.unregister_class(RhubarbAddonPreferences)