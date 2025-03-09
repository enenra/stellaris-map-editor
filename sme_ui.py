import bpy

from bpy.types  import Panel


class SME_PT_Panel(Panel):
    """"""
    bl_idname = "SME_PT_Panel"
    bl_label = "Stellaris Map Editor"
    bl_category = "SME"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


    def draw(self, context):
        layout = self.layout
        active_object = context.active_object

        if active_object is not None:
            if active_object.sme.object_type == 'system':
                box = layout.box()
                box.label(text="Object", icon='OBJECT_DATA')

                box.prop(active_object, 'name')
                box.prop(active_object.sme, 'sme_id')

            elif active_object.sme.object_type == 'nebula':
                box = layout.box()
                box.label(text="Object", icon='OBJECT_DATA')

                box.prop(active_object, 'name')

            elif active_object.sme.object_type == 'add_hyperlane':
                box = layout.box()
                box.label(text="Object", icon='OBJECT_DATA')

                box.label(text=active_object.name)
                box.prop(active_object.modifiers["Hyperlane"], '["Socket_4"]', text="From")
                box.prop(active_object.modifiers["Hyperlane"], '["Socket_5"]', text="To")

        box = layout.box()
        box.label(text="Operators", icon='ADD')
        col = box.column(align=True)

        col.operator('scene.sme_add_system')
        col.operator('scene.sme_add_nebula')
        col.operator('scene.sme_add_hyperlane')

        box = layout.box()
        box.label(text="I/O", icon='FILE')

        box.operator('scene.sme_import_map')
        box.operator('scene.sme_export_map')