import bpy

from bpy.types  import PropertyGroup
from bpy.props  import (EnumProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        IntProperty,
                        StringProperty,
                        BoolProperty,
                        PointerProperty,
                        CollectionProperty
                        )


class SME_Object(PropertyGroup):

    sme_id: IntProperty(
        name="ID",
        description="",
        default=-1
    )

    object_type: EnumProperty(
        name="Type",
        description="",
        items=(
            ('none', "None", ""),
            ('system', "System", ""),
            ('nebula', "Nebula", ""),
            ('add_hyperlane', "Hyperlane", "")
            ),
        default='none'
    )