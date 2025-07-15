
import bpy
import random
import os


SOCKET = {
    "nBranches":"Socket_25",
    "trunk":"Socket_40",
    "treetop":"Socket_26",
    "numLevels":"Socket_27",
    "bLength": "Socket_28",
    "rAngle":"Socket_29",
    "rJitter":"Socket_30",
    "gravity":"Socket_31",
    "thickness":"Socket_32",
    "seed":"Socket_16",   
    "addLeaves":"Socket_19",
    "season":"Socket_17",
    "twoOrThree": "Socket_25",
    "showLeaves":"Socket_39",
    "minHeight":"Socket_12",
}

def get_addon_filepath():
    """
    Returns the absolute path to the directory where this add-on's .py file is located.
    """
    # Use __file__ to get the path of the current script
    # os.path.dirname gets the directory of that script
    return os.path.dirname(os.path.abspath(__file__))


class EASYTREE_OT_HideLeavesTool(bpy.types.Operator):
    bl_idname = "object.hide_tree_leaves"
    bl_label = "Hide Leaves"
    
    bl_options = {'REGISTER', 'UNDO'}
    bl_description = "Hides all of the leaves in the viewport"
    
    
    def execute(self, context):
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups["Simple Tree Generator"]:
                    #print(mod)
                    mod[SOCKET["showLeaves"]] = False
                    obj.update_tag()
        bpy.context.view_layer.update()
        
        self.report({'INFO'}, f"Hid Leaves")
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)


class EASYTREE_OT_ShowLeavesTool(bpy.types.Operator):
    bl_idname = "object.show_tree_leaves"
    bl_label = "Show Leaves"
    bl_description = "Shows all of the leaves in the viewport"
    
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.type == 'NODES' and mod.node_group == bpy.data.node_groups["Simple Tree Generator"]:
                    #print(mod)
                    mod[SOCKET["showLeaves"]] = True
                    obj.update_tag()
        bpy.context.view_layer.update()
        
        self.report({'INFO'}, f"Hid Leaves")
        return {'FINISHED'}
        
    def invoke(self, context, event):
        return self.execute(context)


class EASYTREE_OT_AddTreeTool(bpy.types.Operator):
    bl_idname = "object.add_tree_tool"
    bl_label = "Easy Tree Tool"
    
    bl_options = {'REGISTER', 'UNDO'}
    
    
    def execute(self, context):
        filepath = os.path.join(get_addon_filepath(), "assets", "assets.blend")
        name = "Simple Tree Generator"

        if not filepath or not os.path.exists(filepath):
            self.report({'ERROR'}, f"Asset .blend file not found: {filepath}. Please ensure it exists in the 'assets' subfolder of the add-on.")
            return {'CANCELLED'}

        bpy.ops.mesh.primitive_cube_add(location=bpy.context.scene.cursor.location)
        obj = bpy.context.active_object
        obj.name = "Tree"
        
        mod = obj.modifiers.new(name="Tree Generator", type='NODES')

        if name in bpy.data.node_groups:
            mod.node_group = bpy.data.node_groups[name]
        else:
            try:
                with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
                    if name in data_from.node_groups:
                        data_to.node_groups.append(name)
                    else:
                        self.report({'ERROR'}, f"Node Group '{self.node_group_name}' not found in '{filepath}'.")
                        return {'CANCELLED'}
                if name in bpy.data.node_groups:
                    mod.node_group = bpy.data.node_groups[name]
                    self.report({'INFO'}, f"Successfully appended Node Group '{name}' from '{filepath}'.")      
                else:
                    self.report({'ERROR'}, f"Failed to append Node Group '{name}'.")
                    return {'CANCELLED'}
            except Exception as e:
                self.report({'ERROR'}, f"Error appending node group: {e}")
                return {'CANCELLED'}
    
    
        #Tall
        if context.scene.tree_preset == 'TALL':
            mod[SOCKET["trunk"]] = 5
            mod[SOCKET["numLevels"]] = 5
            mod[SOCKET["bLength"]] = 8
            mod[SOCKET["rAngle"]] = 0.698
            mod[SOCKET["thickness"]] = 3.0
            
        elif context.scene.tree_preset == 'THIN':
            mod[SOCKET["trunk"]] = 2
            mod[SOCKET["treetop"]] = 5
            mod[SOCKET["numLevels"]] = 4
            mod[SOCKET["bLength"]] = 6
            mod[SOCKET["rAngle"]] = 0.523
            mod[SOCKET["thickness"]] = 1.8
            mod[SOCKET["minHeight"]] = 5
        
        elif context.scene.tree_preset == 'DEAD':
            mod[SOCKET["twoOrThree"]] = 1#'Three Branches'
            mod[SOCKET["trunk"]] = 1
            mod[SOCKET["numLevels"]] = 4
            mod[SOCKET["bLength"]] = 10
            mod[SOCKET["rAngle"]] = 0.41
            mod[SOCKET["rJitter"]] = 0.25
            mod[SOCKET["gravity"]] = 1.7
            mod[SOCKET["thickness"]] = 1.8
            mod[SOCKET["addLeaves"]] = False
            
        elif context.scene.tree_preset == 'LARGE':
            mod[SOCKET["trunk"]] = 2
            mod[SOCKET["treetop"]] = 2
            mod[SOCKET["numLevels"]] = 6
            mod[SOCKET["bLength"]] = 8
            mod[SOCKET["rAngle"]] = 0.488
            mod[SOCKET["thickness"]] = 2.9
            
            
        if context.scene.season == 'SPRING':
            mod[SOCKET["season"]] = 0.0
        elif context.scene.season == 'SUMMER':
            mod[SOCKET["season"]] = 0.5
        else:
            mod[SOCKET["season"]] = 1.0
        
        mod[SOCKET["seed"]] = random.randint(0, 9000)
        
        
        self.report({'INFO'}, f"Added {obj.name}!")
        return {'FINISHED'}
    
    def invoke(self, context, event):
        return self.execute(context)
    

classes = (EASYTREE_OT_AddTreeTool, EASYTREE_OT_HideLeavesTool, EASYTREE_OT_ShowLeavesTool)