import bpy
from bpy_extras.io_utils import ImportHelper
from . import  op_blender_rhubarb

class RhubarbLipsyncPanel(bpy.types.Panel):
    bl_idname = "DATA_PT_rhubarb_lipsync"
    bl_label = "Rhubarb Lipsync"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        obj = context.object
        return (obj and obj.type == 'ARMATURE')


    def draw(self, context):
        layout = self.layout

        prop = context.object.mouth_shapes

        col = layout.column()
        col.prop(prop, 'mouth_a', text="Mouth A (MBP)")
        col.prop(prop, 'mouth_b', text="Mouth B (EE/etc)")
        col.prop(prop, 'mouth_c', text="Mouth C (E)")
        col.prop(prop, 'mouth_d', text="Mouth D (AI)")
        col.prop(prop, 'mouth_e', text="Mouth E (O)")
        col.prop(prop, 'mouth_f', text="Mouth F (WQ)")
        col.prop(prop, 'mouth_g', text="Mouth G (FV)")
        col.prop(prop, 'mouth_h', text="Mouth H (L)")
        col.prop(prop, 'mouth_x', text="Mouth X (rest)")

        row = layout.row(align=True)
        row.prop(prop, 'sound_file', text='Sound file')

        row = layout.row(align=True)
        row.prop(prop, 'dialog_file', text='Dialog file')

        row = layout.row()
        row.prop(prop, 'start_frame', text='Start frame')

        row = layout.row()

        if not (context.preferences.addons[__package__].preferences.executable_path):
            row.label(text="Please set rhubarb executable location in addon preferences")
            row = layout.row()

        row.operator(operator = "object.rhubarb_lipsync")


#https://blender.stackexchange.com/a/78592 
enum_items_store = []

def enum_items(self, context):

    items = []
    for action in bpy.data.actions:
        not_an_action = False
        if (not(action.asset_data is None)):
            for i in action.fcurves:
                if (not (i.data_path.split("\"")[1] in context.object.pose.bones)):
                    not_an_action = True
                    print("hello!")    
                    break
                    
        else:
            continue
        if not_an_action:
            continue
        # NEW CODE
        # Scan the list of IDs to see if we already have one for this mesh
        maxid = -1
        id = -1
        found = False
        for idrec in enum_items_store:
            id = idrec[0]
            if id > maxid:
                maxid = id
            if idrec[1] == action.name:
                found = True
                break

        if not found:
            enum_items_store.append((maxid+1, action.name))

        # AMENDED CODE - include the ID
        items.append( (action.name, action.name, "", id) )

    return items

poses = bpy.props.EnumProperty(
    items=enum_items,
    name='Poses',
    description='Poses',
)

class MouthShapesProperty(bpy.types.PropertyGroup):
    mouth_a : poses
    mouth_b : poses
    mouth_c : poses
    mouth_d : poses
    mouth_e : poses
    mouth_f : poses
    mouth_g : poses
    mouth_h : poses
    mouth_x : poses

    sound_file : bpy.props.StringProperty(name="sound_file",subtype='FILE_PATH')
    dialog_file : bpy.props.StringProperty(name="dialog_file",subtype='FILE_PATH')

    start_frame : bpy.props.IntProperty(name="start_frame")

def register():
    bpy.utils.register_class(MouthShapesProperty)
    bpy.utils.register_class(RhubarbLipsyncPanel)

    bpy.types.Object.mouth_shapes = bpy.props.PointerProperty(type=MouthShapesProperty)


def unregister():
    bpy.utils.unregister_class(MouthShapesProperty)
    bpy.utils.unregister_class(RhubarbLipsyncPanel)