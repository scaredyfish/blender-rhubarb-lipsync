from . import ops, props, ui, prefs

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


def register():
    ops.register()
    ui.register()
    props.register()
    prefs.register()


def unregister():
    ops.unregister()
    ui.unregister()
    props.unregister()
    prefs.unregister()
