import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb

# bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)


class RhubarbLipsyncPanel(bpy.types.Panel):
    """Panel to control options of rhubarb operator"""

    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AI Lipsync"
    bl_label = "Controller AI Lipsync"
    bl_context = "posemode"

    # https://gist.github.com/daylanKifky/252baea63eb0c39858e3e9b57f1af167
    bpy.types.Scene.obj_selection = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.bone_selection = bpy.props.StringProperty()

    def draw(self, context):

        sc = bpy.data.scenes["Scene"]
        self.layout.prop_search(
            sc, "bone_selection", sc.obj_selection.data, "bones", text="Bone"
        )
        layout = self.layout
        prop = context.object.rhubarb
        row = layout.row()
        row.label(text="Property Name:")
        sub = row.row()
        sub.enabled = bpy.data.scenes["Scene"].bone_selection is not ""
        sub.prop(prop, "user_path", text="")
        row = layout.row()
        row = layout.row()
        row.menu(menu="OBJECT_MT_select_test", text="Select a Property")

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

        row = layout.row(align=True)
        row.prop(prop, "sound_file", text="Sound file")

        row = layout.row(align=True)
        row.prop(prop, "dialog_file", text="Dialog file")

        row = layout.row()
        row.prop(prop, "start_frame", text="Start frame")

        row = layout.row()
        sub = row.row()
        sub.enabled = (
            bpy.data.scenes["Scene"].bone_selection is not ""
            and bpy.data.objects["Josephine - Control"].rhubarb.user_path is not ""
        )
        sub.operator(operator="object.rhubarb_lipsync")

    @classmethod
    def poll(cls, context):
        return bpy.data.scenes["Scene"].bone_selection is not None


# Panel now stores all values in the same property group but it is not in pose mode Next step is to clean up the operator.


class MouthShapesProperty(bpy.types.PropertyGroup):
    """definitions for rhubarb properties"""

    mouth_a: bpy.props.IntProperty(name="moutha", default=1)
    mouth_b: bpy.props.IntProperty(name="mouthb", default=2)
    mouth_c: bpy.props.IntProperty(name="mouthc", default=3)
    mouth_d: bpy.props.IntProperty(name="mouthd", default=4)
    mouth_e: bpy.props.IntProperty(name="mouthe", default=5)
    mouth_f: bpy.props.IntProperty(name="mouthf", default=6)
    mouth_g: bpy.props.IntProperty(name="mouthg", default=7)
    mouth_h: bpy.props.IntProperty(name="mouthh", default=8)
    mouth_x: bpy.props.IntProperty(name="mouthx", default=9)

    user_path: bpy.props.StringProperty(
        name="Enter Custom Property Name",
        description="Enter the name of an int property exactly as it appears in the Custom Properties of the selected Bone",
    )
    sound_file: bpy.props.StringProperty(name="sound_file", subtype="FILE_PATH")
    dialog_file: bpy.props.StringProperty(name="dialog_file", subtype="FILE_PATH")
    stored_mouths: bpy.props.IntVectorProperty(name="stored_mouths", size=9)
    default_mouths: bpy.props.IntVectorProperty(name="default_mouths", size=9)
    aval_props: bpy.props.StringProperty(name="aval_prop_names")
    start_frame: bpy.props.IntProperty(name="start_frame")


class BasicMenu(bpy.types.Menu):
    """Testing menu to draw a list of props based on the selected context from above"""

    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        print("draw menu active")
        # Can I make these definitions global?
        obj_path = bpy.context.object
        sc = bpy.data.scenes["Scene"]
        bone = sc.bone_selection
        bone_path = obj_path.pose.bones["{0}".format(bone)]

        # TESTING How to print all props on a bone https://blenderartists.org/t/is-it-possible-to-set-all-the-custom-properties-of-a-bone-to-0/545554/3
        print("active-drawprops")
        for y, _ in bone_path.items():
            print(y)
            self.layout.prop(bone_path, f'["{y}"]', text=f"{y}")
        print("list below3")


def register():
    bpy.utils.register_class(MouthShapesProperty)
    bpy.utils.register_class(RhubarbLipsyncPanel)
    bpy.utils.register_class(BasicMenu)

    bpy.types.Action.mouth_shapes = bpy.props.PointerProperty(type=MouthShapesProperty)
    bpy.types.Object.rhubarb = bpy.props.PointerProperty(type=MouthShapesProperty)


def unregister():
    bpy.utils.unregister_class(MouthShapesProperty)
    bpy.utils.unregister_class(RhubarbLipsyncPanel)
    bpy.utils.unregister_class(BasicMenu)
