__version__ = "3.0.2"

bl_info = {
    "name": "Rhubarb Lipsync-DEV",
    "author": "Customized by Nick Alberelli, based on: Addon by Andrew Charlton, includes Rhubarb Lip Sync by Daniel S. Wolf",
    "version": (3, 0, 2),
    "blender": (3, 0, 0),
    "location": "VIEW3D > Sidebar > AI Lipsync",
    "description": "Integrate Rhubarb Lipsync into Tiny Media Blender Workflow",
    "wiki_url": "https://github.com/adcharlton/blender-rhubarb-lipsync",
    "tracker_url": "https://github.com/adcharlton/blender-rhubarb-lipsync/issues",
    "support": "COMMUNITY",
    "category": "Animation",
    "warning": "This addon is in development and NOT ready to for production.",
}


if "bpy" in locals():
    import importlib

    if "op_blender_rhubarb" in locals():
        importlib.reload(op_blender_rhubarb)
        importlib.reload(pnl_blender_rhubarb)
        importlib.reload(prefs_blender_rhubarb)
else:
    from . import op_blender_rhubarb, pnl_blender_rhubarb, prefs_blender_rhubarb

import bpy


def register():
    op_blender_rhubarb.register()
    pnl_blender_rhubarb.register()
    prefs_blender_rhubarb.register()


def unregister():
    op_blender_rhubarb.unregister()
    pnl_blender_rhubarb.unregister()
    prefs_blender_rhubarb.unregister()
