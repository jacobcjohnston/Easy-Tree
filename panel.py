import bpy


class EASYTREE_PT_GeoNodesPanel(bpy.types.Panel):
    bl_label = "Easy Tree"
    bl_idname = "EASYTREE_PT_geo_nodes_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'         # This makes it part of the N-panel
    bl_category = "Easy Tree"         # This creates a new tab called "Tools"


    def draw(self, context):
        layout = self.layout
        #layout.label(text="Add Any Tree you want!")
        layout.prop(context.scene, "tree_preset", text="Preset")
        layout.prop(context.scene, "season", text="Season")
        layout.operator("object.add_tree_tool", text="Add Tree")
        
        row = layout.row()
        #row.label(text="Leaf Visibility")
        row.operator("object.hide_tree_leaves", text="Hide All Leaves")
        row.operator("object.show_tree_leaves", text="Show All Leaves")


classes = [EASYTREE_PT_GeoNodesPanel]