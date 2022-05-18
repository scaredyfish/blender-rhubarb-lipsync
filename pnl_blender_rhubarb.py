import bpy
from bpy_extras.io_utils import ImportHelper
from . import op_blender_rhubarb
import bpy, mathutils

bpr = bpy.props

"""Below are definitions for enumurated list of properties. 
List of properties will be used for fetching how many 
custom properties exist on a bone or object."""

data_for_enum = []


def enum_items_generator(self, context):
    enum_items = []
    for e, d in enumerate(data_for_enum):
        enum_items.append((d[0], d[0], d[0], e))
        # as you see for each tuple in my list I use [0] item to generate enum value/name and [1] item for description + integer from enumerate for id
    return enum_items


def report(self, message):  # Just to report errors
    self.report({"ERROR"}, message)
    return {"CANCELLED"}


class EEA_OT_Enum_Add(bpy.types.Operator):
    """Operator for adding items to the enum prop"""

    bl_idname = "eea.eea_enum_add"
    bl_label = "EEA_OT_Enum_Add"
    bl_description = "Add new enum item"

    new_name: bpy.props.StringProperty(default="Preset name", name="Preset name ")

    def execute(self, context):
        obj_path = bpy.context.object
        sc = bpy.data.scenes["Scene"]
        bone = sc.bone_selection
        bone_path = obj_path.pose.bones["{0}".format(bone)]

        global data_for_enum

        eea = context.object.rhubarb
        aob = context.view_layer.objects.active

        if aob == None:  # For case when there is no active object
            return report(self, "No active object selected!!!")

        # TESTING How to print all props on a bone https://blenderartists.org/t/is-it-possible-to-set-all-the-custom-properties-of-a-bone-to-0/545554/3
        data_for_enum.clear()
        for prop_name, _ in bone_path.items():
            # self.layout.prop(bone_path, f'["{y}"]', text=f"{y}")
            data_for_enum.append(
                (prop_name, prop_name, prop_name)
            )  # here I append to data_for_enum new tuple
        print("list below3")

        return {"FINISHED"}


class EEA_OT_Enum_Remove(bpy.types.Operator):
    """Operator for removing items to the enum prop"""

    bl_idname = "eea.eea_enum_remove"
    bl_label = "EEA_OT_Enum_Remove"
    bl_description = "Remove current enum item"

    def execute(self, context):
        global data_for_enum

        eea = context.object.rhubarb

        if len(data_for_enum) != 0:
            did = [x[0] for x in data_for_enum].index(
                eea.presets
            )  # I search for index of current enum in my list [0] items of my tuples
            data_for_enum.pop(did)  # I pop out item with this index from my list

            # at this moment my list is already changed and enum already regenereted

            if (
                did > len(data_for_enum) - 1 and data_for_enum != []
            ):  # here I set enum to value of my list last item in case when I remove last enum item, othervise active enum become empty :)
                eea.presets = data_for_enum[len(data_for_enum) - 1][0]

        else:
            return report(self, "No more items to remove")
        return {"FINISHED"}


class RhubarbLipsyncPanel(bpy.types.Panel):
    """Panel to control options of rhubarb operator"""

    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AI Lipsync"
    bl_label = "Controller AI Lipsync"
    bl_context = "posemode"

    bpy.types.Scene.obj_selection = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.bone_selection = bpy.props.StringProperty()

    def draw(self, context):
        # Bone Selection Menu

        sc = bpy.data.scenes["Scene"]
        obj = bpy.context.object
        self.layout.prop(sc, "obj_selection", text="")

        self.layout.prop_search(
            sc, "bone_selection", sc.obj_selection.data, "bones", text="Bone"
        )
        layout = self.layout
        prop = context.object.rhubarb

        # Manually enter prop name as string
        row = layout.row()
        row.label(text="Property Name:")

        sub = row.row()
        sub.enabled = bpy.data.scenes["Scene"].bone_selection is not ""
        sub.prop(prop, "user_path", text="")

        # Testing Enum Dropdown Menu
        col = layout.column(align=True)
        eea = context.object.rhubarb
        row = layout.row()

        row = col.row(align=True)
        row.operator("eea.eea_enum_add", text="Load Properties")
        row.prop(eea, "presets", text="")

        # Mouth Shape Definitions
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
        sub.enabled = bpy.data.scenes["Scene"].bone_selection is not ""
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
    presets: bpy.props.EnumProperty(items=enum_items_generator, name="Position Preset")


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


ctr = [
    EEA_OT_Enum_Add,
    EEA_OT_Enum_Remove,
    MouthShapesProperty,
    RhubarbLipsyncPanel,
    BasicMenu,
]


def register():
    for cls in ctr:
        bpy.utils.register_class(cls)
    bpy.types.Object.rhubarb = bpy.props.PointerProperty(type=MouthShapesProperty)


def unregister():
    for cls in reversed(ctr):
        bpy.utils.unregister_class(cls)
