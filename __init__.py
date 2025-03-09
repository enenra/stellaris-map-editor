bl_info = {
    "name": "Stellaris Map Editor",
    "description": "This is a small addon for Blender 4.3+ for editing Stellaris preset maps.",
    "author": "enenra",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "Add-ons",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "git_url": "https://github.com/enenra/stellaris-map-editor",
    "support": "COMMUNITY",
    "category": "Utility"
}

import bpy

from bpy.props          import PointerProperty

from .sme_operators    import *
from .sme_object       import *
from .sme_ui           import *


classes = (
    SME_OT_Import_Map,
    SME_OT_Export_Map,
    SME_OT_Add_System,
    SME_OT_Add_Nebula,
    SME_OT_Add_Hyperlane,
    SME_Object,
    SME_PT_Panel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Object.sme = PointerProperty(type=SME_Object)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Object.sme


def menu_func(self, context):
    for cls in classes:
        if str(cls).find("SME_OT_") != -1:
            self.layout.operator(cls.bl_idname)


if __name__ == "__main__":
    register()