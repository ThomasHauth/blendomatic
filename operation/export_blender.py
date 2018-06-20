import bpy
import os
import sys

# add the path to this file as the python path so we can
# import additional python code
blendomatic_python_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(blendomatic_python_path)

import blenderutil

def export_obj(output_folder, obj_filename, objs_to_export):

    blenderutil.select_objects(objs_to_export)

    output_file_path = os.path.join(output_folder, os.path.basename(obj_filename))
    # call export with a lot of parameters we did not provide yet to the user
    bpy.ops.export_scene.obj(filepath=output_file_path, check_existing=False,
                             axis_forward='-Z', axis_up='Y',
                             filter_glob="*.obj;*.mtl",
                             use_selection=True, use_animation=False,
                             use_mesh_modifiers=True, use_edges=True,
                             use_smooth_groups=False, use_smooth_groups_bitflags=False,
                             use_normals=True, use_uvs=True,
                             use_materials=True, use_triangles=True,
                             use_nurbs=False, use_vertex_groups=False,
                             use_blen_objects=True, group_by_object=False,
                             group_by_material=False, keep_vertex_order=False,
                             global_scale=1, path_mode='AUTO')

jobParameter = blenderutil.parse_jobinput()

bpy.ops.wm.open_mainfile(filepath=jobParameter["blender_filename"])
output_folder = jobParameter["output_folder"]

assert (len(jobParameter["output_filenames"]) == len(jobParameter["object_names"]))

for i in range(len(jobParameter["output_filenames"])):
    export_obj(output_folder, jobParameter["output_filenames"][i][0], jobParameter["object_names"][i])

sys.exit(0)
