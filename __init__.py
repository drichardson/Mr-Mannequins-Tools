# Contributor(s): James Goldsworthy (j.kroovy.creative.services@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Mr Mannequins Tools",
    "author": "James Goldsworthy (Jim Kroovy)",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "description": "Loads, saves, imports and exports UE4 Mannequin compatible armatures and meshes",
    "warning": "",
    "wiki_url": "https://www.youtube.com/c/JimKroovy",
    "category": "Characters",
}

import bpy
import os

def GetFiles():
    default_dir = os.path.dirname(os.path.realpath(__file__))
    items = []
    for filename in os.listdir(default_dir):
        filepath = os.path.join(default_dir, filename)
        identifier = filepath
        #print("identifier type is {0}, {1}".format(type(identifier), identifier))
        name = filename
        description = filepath
        items.append((identifier, name, description))
    return items

class JK_MMT_Props(bpy.types.PropertyGroup):

    def GetFiles(self, context):
        return GetFiles()
    
    selected_file: bpy.props.EnumProperty(
        name="Files",
        description="Enum File Picker",
        items=GetFiles,
        default=None
        )

class JK_OT_PrintFilename(bpy.types.Operator):
    """Print the selected filename"""
    bl_idname = "jk.print_filename"
    bl_label = "Print Filename"
    
    def execute(self, context):
        MMT = context.scene.JK_MMT
        #rig_name = bpy.path.display_name_from_filepath(MMT.L_rigs)[9:] # does the same thing but should be utf-8 compatible...
        print("Selected File is {0}".format(MMT.selected_file))
        return {'FINISHED'}
    
# stash interface panel...       
class JK_PT_MMT_Stash(bpy.types.Panel):
    bl_label = "My File Picker"
    bl_idname = "JK_PT_MMT_Stash"
    bl_space_type = 'VIEW_3D'
    bl_context= 'objectmode'
    bl_region_type = 'UI'
    bl_category = "Mr Mannequins Tools"

    def draw(self, context):
        layout = self.layout
        MMT = context.scene.JK_MMT
        layout.prop(MMT, "selected_file")
        layout.box().operator("jk.print_filename")       
                                        
#---------- REGISTRATION -----------------------------------------------------------------------    

JK_MMT_classes = (
    JK_MMT_Props,
    JK_OT_PrintFilename,
    JK_PT_MMT_Stash,
    )

def register():
    from bpy.utils import register_class
    for C in JK_MMT_classes:
        register_class(C)
    bpy.types.Scene.JK_MMT = bpy.props.PointerProperty(type=JK_MMT_Props)

def unregister():
    from bpy.utils import unregister_class
    for C in reversed(JK_MMT_classes):
        unregister_class(C)
    del bpy.types.Scene.JK_MMT
