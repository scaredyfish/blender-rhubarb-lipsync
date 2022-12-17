import bpy

from rhubarb_lipsync.core import refresh_target, initlize_props


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
        rhubarb = context.window_manager.rhubarb_panel_settings
        layout = self.layout
        target_col = layout.column()
        mode_row = target_col.row(align=True)
        mode_row.prop(rhubarb, "obj_modes", text="Target Type", toggle=True)

        obj = refresh_target(context)
        if not obj:
            return

        # if obj is Armature select a bone to target
        if rhubarb.obj_modes == "bone" and context.active_object.type == "ARMATURE":
            target_col.prop_search(
                context.scene, "bone_selection", obj.id_data.pose, "bones", text="Bone"
            )
        # Load and Select Properties
        if not rhubarb.obj_modes == "":
            target_col.prop(
                rhubarb,
                "presets",
                text="Properties",
            )

        # User editable Mouth Definitions
        initlize_props(rhubarb)
        prop_col = layout.column()
        prop_col.prop(rhubarb, "mouth_b", text="Mouth B (EE/etc)")
        prop_col.prop(rhubarb, "mouth_c", text="Mouth C (E)")
        prop_col.prop(rhubarb, "mouth_d", text="Mouth D (AI)")
        prop_col.prop(rhubarb, "mouth_e", text="Mouth E (O)")
        prop_col.prop(rhubarb, "mouth_f", text="Mouth F (WQ)")
        prop_col.prop(rhubarb, "mouth_g", text="Mouth G (FV)")
        prop_col.prop(rhubarb, "mouth_h", text="Mouth H (L)")
        prop_col.prop(rhubarb, "mouth_x", text="Mouth X (rest)")

        # Set Rhubarb Executable depencies
        set_col = layout.column()
        set_col.separator()

        set_col.prop(rhubarb, "sound_file", text="Sound file")
        set_col.prop(rhubarb, "dialog_file", text="Dialog file")
        set_col.prop(rhubarb, "start_frame", text="Start frame")

        # Button to execute rhubarb operation
        set_col.separator()
        set_col.operator(operator="rhubarb.execute_rhubarb_lipsync")


classes = (RHUBARB_PT_Main_Panel,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
