import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb

bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)

list_of_props = []


class RhubarbLipsyncPanel(bpy.types.Panel):
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
        self.layout.prop(sc, "obj_selection", text="Object")
        obj_path = bpy.data.scenes["Scene"].obj_selection
        arm_path = obj_path.pose.bones  # ["{0}".format(bone)]
        list_of_props.clear()
        if sc.obj_selection:
            if sc.obj_selection.type == "ARMATURE":
                self.layout.prop_search(
                    sc, "bone_selection", sc.obj_selection.data, "bones", text="Bone"
                )

        layout = self.layout
        prop = context.object.rhubarb
        row = layout.row()
        row.prop(prop, "user_path", text="Prop-Name")
        row = layout.row()
        row = layout.row()
        row.menu(
            menu="OBJECT_MT_select_test", text_ctxt="test1", text="Select a Property"
        )

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

        if not (context.preferences.addons[__package__].preferences.executable_path):
            row.label(
                text="Please set rhubarb executable location in addon preferences"
            )
            row = layout.row()

        row.operator(operator="object.rhubarb_lipsync")


# Panel now stores all values in the same property group but it is not in pose mode Next step is to clean up the operator.


class MouthShapesProperty(bpy.types.PropertyGroup):
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
        name="user_path", description="Enter the name of an int property"
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
        # Can I make these definitions global?
        layout = self.layout

        obj_path = bpy.data.scenes["Scene"].obj_selection
        bone = bpy.data.scenes["Scene"].bone
        bone_path = obj_path.pose.bones["{0}".format(bone)]
        sc = bpy.data.scenes["Scene"]
        arm_path = obj_path.pose.bones
        rhubarb = bpy.context.object.rhubarb
        print("draw menu active")
        layout.operator(
            "object.select_all", text="Select/Deselect All"
        ).action = "TOGGLE"
        layout.operator("object.select_all", text="Inverse").action = "INVERT"
        layout.operator("object.select_random", text="Random")

        print("draw menu active2")
        bone_path = arm_path["{0}".format(sc.bone)]
        """How to print all props on a bone https://blenderartists.org/t/is-it-possible-to-set-all-the-custom-properties-of-a-bone-to-0/545554/3"""
        for x, value in bone_path.items():
            # if type(value) is int: #Off for test
            print('pose.bones["%s"]["%s"] =  %.1f' % (bone_path.name, x, value))
            # rhubarb.aval_props = +"{0}".format(x) #NFG
        print("list below")
        print(list_of_props)


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
