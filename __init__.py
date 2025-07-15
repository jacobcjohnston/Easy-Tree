# This add-on is licensed under the MIT License.
# See the LICENSE file in the root of this project for details.

bl_info = {
    "name":        "Easy Tree",
    "author":      "Jacob Johnston",
    "version":     (1, 0, 0),
    "blender":     (4, 5, 0),        # minimum Blender version
    "location":    "View3D > Sidebar > Easy tree",
    "description": "Add an infinite variety of Geometry Nodes 100% procedural trees",
    "category":    "3D View"
}

import bpy
from . import panel, operators

classes = []
classes += panel.classes
classes += operators.classes

def register():
    bpy.types.Scene.tree_preset = bpy.props.EnumProperty(
        name="preset",
        description="Choose a tree preset",
        items=[
            ('SMALL', "Small", "A default tree"),
            ('TALL', "Tall", "Tall Tree Preset"),
            ('THIN', "Thin", "Thin Tree Preset"),
            ('LARGE', "Large", "Large Tree Preset"),
            ('DEAD', "Dead", "Dead Tree Preset (No Leaves)"),
        ],
        default='SMALL'
    )
    
    bpy.types.Scene.season = bpy.props.EnumProperty(
        name="Mode",
        description="Choose a mode",
        items=[
            ('SPRING', "Spring", "Light Green Leaves"),
            ('SUMMER', "Summer", "Green Leaves"),
            ('FALL', "Fall", "Red & Orange Leaves"),
        ],
        default='SPRING'
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.season
    del bpy.types.Scene.tree_preset

if __name__ == "__main__":
    register()