import bpy

from rhubarb_lipsync.core import refresh_target


class RHUBARB_PT_Main_Panel(bpy.types.Panel):
    """Panel to control options of rhubarb operator"""

    bl_idname = "RHUBARB_PT_Main_Panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Rhubarb Lipsync"
    bl_label = "Rhubarb Lipsync"

    # Pointer definitions
    bpy.types.Scene.obj_selection = bpy.props.PointerProperty(type=bpy.types.Object)
    bpy.types.Scene.bone_selection = bpy.props.StringProperty()

    def draw(self, context):

        # Panel Definitions
        sc = context.scene
        rhubarb = context.window_manager.rhubarb_panel_settings
        layout = self.layout

        # Display active object name
        # layout.label(text=f"Active Object: {obj.name}")  # TODO Improve this.
        row = layout.row(align=True)
        row.prop(rhubarb, "obj_modes", text="Target Type", toggle=True)

        obj = refresh_target(context)
        if not obj:
            return

        # if obj is Armature select a bone to target
        if rhubarb.obj_modes == "bone":
            layout.prop_search(
                sc, "bone_selection", obj.id_data.pose, "bones", text="Bone"
            )
        row = layout.row()
        # Load and Select Properties

        if rhubarb.presets == "":
            row.label(text="No Properties Found", icon="ERROR")
        if not rhubarb.obj_modes == "":
            row.prop(
                rhubarb,
                "presets",
                text="Properties",
            )

        # row.operator("rhubarb.enum_get", text="Load Properties")

        # User editable Mouth Definitions
        col = layout.column()
        col.prop(rhubarb, "mouth_a", text="Mouth A (MBP)")
        col.prop(rhubarb, "mouth_b", text="Mouth B (EE/etc)")
        col.prop(rhubarb, "mouth_c", text="Mouth C (E)")
        col.prop(rhubarb, "mouth_d", text="Mouth D (AI)")
        col.prop(rhubarb, "mouth_e", text="Mouth E (O)")
        col.prop(rhubarb, "mouth_f", text="Mouth F (WQ)")
        col.prop(rhubarb, "mouth_g", text="Mouth G (FV)")
        col.prop(rhubarb, "mouth_h", text="Mouth H (L)")
        col.prop(rhubarb, "mouth_x", text="Mouth X (rest)")

        # Set Rhubarb Executable depencies
        row = layout.row(align=True)
        row.prop(rhubarb, "sound_file", text="Sound file")
        row = layout.row(align=True)
        row.prop(rhubarb, "dialog_file", text="Dialog file")
        row = layout.row()
        row.prop(rhubarb, "start_frame", text="Start frame")

        # Button to execute rhubarb operation
        row = layout.row()
        row.operator(operator="rhubarb.execute_rhubarb_lipsync")


classes = (RHUBARB_PT_Main_Panel,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
