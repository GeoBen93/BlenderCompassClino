bl_info = {
    "name" : "Compass-clino",
    "author" : "Ben Clarke",
    "version" : (0,1),
    "blender" : (2,90,1),
    "location" : "View3d > Tool",
    "wiki_url" : "https://github.com/GeoBen93/BlenderCompassClino",
    "category" : "3D View"
}

import bpy
import bmesh
import numpy as np
import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

# custom operator
class DipOperator(bpy.types.Operator):
    bl_idname = "wm.dip_operator"
    bl_label = "Calculate Dip Data"

    def execute(self, context):
        # load object data
        obj_data = bpy.context.active_object.data
        # find indices of faces that have been selected
        obj = bpy.context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        select_list = []

        for f in bm.faces:
            if f.select:
                select_list.append(f.index)

        N = len(select_list)
        faces = obj_data.polygons
        dip_list, dip_dir_list = [], []

        for i in select_list:
            normal_vector = faces[i].normal
            
            x = normal_vector[0]
            y = normal_vector[1]
            z = normal_vector[2]
            
            dip = 90 - np.degrees(np.arcsin(z))
            
            dir = np.degrees(np.arctan2(x,y)) # north clockwise atan2 convention atan2(x,y)
            dir = (dir + 360) % 360 # modulo operation to convert -180->180 to 0->360
            
            dip_list.append(dip)
            dip_dir_list.append(dir)

        mean_dip = np.mean(dip_list)    
        std_dip = np.std(dip_list)
        sem_dip = (std_dip/np.sqrt(N))*1.96

        mean_dip_dir = np.mean(dip_dir_list) 
        std_dip_dir = np.std(dip_dir_list)
        sem_dip_dir = (std_dip_dir/np.sqrt(N))*1.96

        result_dip = 'Dip: %.2f +/- %.2f' % (mean_dip, sem_dip)
        result_dip_dir = 'Dip dir: %.2f +/- %.2f' % (mean_dip_dir, sem_dip_dir)
        n = 'N = %d' % N
        
        def ShowMessageBox(title = "Results", icon = 'INFO', lines=''):
            myLines=lines
            def draw(self, context):
                for n in myLines:
                    self.layout.label(text=n)

            bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)  

        ShowMessageBox(lines = (result_dip, result_dip_dir, n, '(Copied to clip-board)'))
        
        # prepare data for clipbaord copy
        copy_data =  '%.2f, %.2f, %.2f, %.2f, %d' % (mean_dip, sem_dip, mean_dip_dir, sem_dip_dir, N)
        
        copy2clip(copy_data)
        
        return {'FINISHED'}

# UI panel
class DipPanel(bpy.types.Panel):
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "Compass-clinometer"
    bl_idname = "PT_dip_info"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Compass-Clino"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        # invoke custom operator
        row.operator("wm.dip_operator" , text = "Measure Dip")
        row = layout.row()
        

def register():
    bpy.utils.register_class(DipOperator)
    bpy.utils.register_class(DipPanel)

def unregister():
    bpy.utils.unregister_class(DipOperator)
    bpy.utils.unregister_class(DipPanel)

if __name__ == "__main__":
    register()
