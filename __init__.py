__version__ = '1.0.0'

bl_info = {
    'name': 'Rhubarb Lipsync',
    'author': 'Andrew Charlton',
    'version': (1, 0, 0),
    'blender': (2, 7, 9),
    'location': 'Properties > Armature',
    'description': 'Integrate Rhubarb Lipsync into Blender',
    'wiki_url': 'https://github.com/adcharlton/blender-rhubarb-lipsync',
    'tracker_url': 'https://github.com/adcharlton/blender-rhubarb-lipsync/issues',
    'support': 'COMMUNITY',
    'category': 'Animation',
}




if 'bpy' in locals():
    import importlib

    if 'op_blender_rhubarb' in locals():
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