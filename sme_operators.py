import bpy

from bpy.types  import Operator
from bpy.props  import StringProperty, IntProperty, BoolProperty, EnumProperty

from .sme_importer import *
from .sme_exporter import export_map_file


class SME_OT_Import_Map(Operator):
    """"""
    bl_idname = "scene.sme_import_map"
    bl_label = "Import Map"
    bl_options = {'REGISTER', 'UNDO'}


    filter_glob: StringProperty(
        default='*.txt',
        options={'HIDDEN'}
        )

    filepath: StringProperty(
        subtype="FILE_PATH"
        )


    @classmethod
    def poll(cls, context):
        return context.scene is not None


    def execute(self, context):

        return import_map_file(self, context, self.filepath)


    def invoke(self, context, event):

        context.window_manager.fileselect_add(self)

        return {'RUNNING_MODAL'}


class SME_OT_Export_Map(Operator):
    """"""
    bl_idname = "scene.sme_export_map"
    bl_label = "Export Map"
    bl_options = {'REGISTER', 'UNDO'}


    filter_glob: StringProperty(
        default='*.txt',
        options={'HIDDEN'}
        )

    filepath: StringProperty(
        subtype="FILE_PATH"
        )


    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.mode == 'OBJECT'


    def execute(self, context):

        result = export_map_file(self, context)

        return result


    def invoke(self, context, event):

        context.window_manager.fileselect_add(self)
        self.filepath = context.scene.name + ".txt"

        return {'RUNNING_MODAL'}


class SME_OT_Add_System(Operator):
    """"""
    bl_idname = "scene.sme_add_system"
    bl_label = "Add System"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        create_system()

        return {'FINISHED'}


class SME_OT_Add_Nebula(Operator):
    """"""
    bl_idname = "scene.sme_add_nebula"
    bl_label = "Add Nebula"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        create_nebula()

        return {'FINISHED'}


class SME_OT_Add_Hyperlane(Operator):
    """"""
    bl_idname = "scene.sme_add_hyperlane"
    bl_label = "Add Hyperlane"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):

        create_hyperlane()

        return {'FINISHED'}