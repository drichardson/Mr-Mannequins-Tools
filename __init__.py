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
import sys
import os
import importlib # i dont think executing importlib.reload(script) on scripts is needed as they all run from scene property values but doing it anyway just to be on the safe side...

from bpy.props import (StringProperty, BoolProperty, BoolVectorProperty, IntProperty, IntVectorProperty, FloatProperty, EnumProperty, PointerProperty, CollectionProperty)
                       
from bpy.types import (Panel, Menu, WorkSpaceTool, Operator, PropertyGroup, AddonPreferences)

from bpy.utils import (register_class, unregister_class)

from mathutils import Matrix, Vector

from bpy.app.handlers import persistent

#---------- NOTES ------------------------------------------------------------------------------

# This is still a work in progress! I'm still not all that happy with the UI...
# and there are a whole bunch of options and functionality to create and finalize...
# i've got the main pieces of logic sussed out for this initial release and they should not need to change much...

# i suppose if you are reading this then you're probably trying to figure out how it all works...
# there are two parts to this add-on, the main and most useful part is the UE4 export FBX logic... (see MMT_Export_FBX.py for more info)
# which exports a UE4 mannequin compatible .FBX, no more retargeting needed! Woop!

# Then there is the stashing logic which enables the user to save their meshes/materials and reload them in other blend files...
# First the user creates a stash folder somewhere, then they are able write, load and remove library .blends to and from this location...
# the selection of library .blends is through drop down enum menus that display whats in the currently selected stash...
# users can have multiple stashes and the current stash can also be changed through a drop down enum menu...

# When a mesh/material is added to a stash a reference clean up text is written and stored with it...
# then when a mesh/material is loaded that clean up text is executed in order to set those references relative to what is in the current .blend...
# if a saved reference is not in the current .blend then it is linked to the scene... (see MMT_Stash_Object.py and MMT_Stash_Material.py for more info)

# I did want to make the rig properties specific to armatures but doing that makes them a pain to animate so they are attached to objects instead...
# which isn't all bad as that also means that in the future i can easily drive character mesh shape keys and options from the armature within the same actions...

# MMT stands for Mr Mannequins Tools, E stands for export, I stands for import, S stands for Stash, L stands for Load, A stands for Add, O stands for option...
# and JK/Jk/jk stands for Jim Kroovy and is the creator prefix i use for anything that might be used elsewhere... (makes for easier searching in most editing programs)

#---------- FUNCTIONS --------------------------------------------------------------------------

# get stashed items from default and custom stashes...
def Get_Stashed_MMT(MMT_path, armature, type):
    default_dir = os.path.join(MMT_path, "MMT_Stash")
    items = []
    # gather items from default stash by type...
    for filename in os.listdir(default_dir):
        if type in filename:
            if type == 'MESH':
                if armature.JK_MMT.Rig_type in filename:
                    name_start = (15 if "MANNEQUIN" in filename else 9)
                    items.append((os.path.join(default_dir, filename), filename[name_start:-6], os.path.join(default_dir, filename)))
            else:
                items.append((os.path.join(default_dir, filename), filename[9:-6], os.path.join(default_dir, filename)))
    return items

# all the main add-on options...
class JK_MMT_Props(PropertyGroup):
    
    def Get_Stashed_Armatures(self, context):
        return Get_Stashed_MMT(self.MMT_path, bpy.context.object, 'ARMATURE')
    
    MMT_path: StringProperty(
        name="",
        description="Where the addon scripts are",
        default=os.path.dirname(os.path.realpath(__file__)),
        maxlen=1024,
        )
    
    L_rigs: EnumProperty(
        name="Rig",
        description="Armature to load",
        items=Get_Stashed_Armatures,
        default=None
        )

# loads a saved armature...        
class JK_OT_L_Rig(Operator):
    """Loads the selected armature from default stash"""
    bl_idname = "jk.l_rig"
    bl_label = "Load Rig"
    
    def execute(self, context):
        MMT = context.scene.JK_MMT
        #rig_name = os.path.basename(MMT.L_rigs)[9:-6] - causing utf-8 errors on some systems??
        rig_name = bpy.path.display_name_from_filepath(MMT.L_rigs)[9:] # does the same thing but should be utf-8 compatible...
        print("Rig name is {0}".format(rig_name))
        return {'FINISHED'}
    
# stash interface panel...       
class JK_PT_MMT_Stash(Panel):
    bl_label = "Stash"
    bl_idname = "JK_PT_MMT_Stash"
    bl_space_type = 'VIEW_3D'
    bl_context= 'objectmode'
    bl_region_type = 'UI'
    bl_category = "Mr Mannequins Tools"

    def draw(self, context):
        layout = self.layout
        MMT = context.scene.JK_MMT
        layout.prop(MMT, "L_rigs")
        layout.box().operator("jk.l_rig")       
                                        
#---------- REGISTRATION -----------------------------------------------------------------------    

JK_MMT_classes = (
    JK_MMT_Props,
    JK_OT_L_Rig,
    JK_PT_MMT_Stash,
    )

def register():
    for C in JK_MMT_classes:
        register_class(C)
    bpy.types.Scene.JK_MMT = PointerProperty(type=JK_MMT_Props)

def unregister():
    for C in reversed(JK_MMT_classes):
        unregister_class(C)
    del bpy.types.Scene.JK_MMT
