import bpy
import os
import sys
import json
import pprint

def unselect_all():
    for obj in bpy.data.objects:
        obj.select = False

def export_obj(output_folder, obj_filename, objs_to_export):

    unselect_all()

    if len(objs_to_export) == 1 and objs_to_export[0] == "":
        # if no objects have been selected, export everything
        for obj in bpy.data.objects:
            obj.select = True
            print("Object {} selected for export".format(obj))
    else:
        # specific objects selected
        for obj_name in objs_to_export:
            obj = bpy.data.objects[obj_name]
            # select all objects used for export
            obj.select = True
            print("Object {} selected for export".format(obj))

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


# extract parameters for extraction
exportObjects = None
outputFileName = None
inputFileName = None
bakeTextureFileName = None
objectToBake = None

jobParameterFile = None

for a in sys.argv:
    splitted = a.split("=")
    if len(splitted) > 1:
        if splitted[0] == "jobParameterFile":
            jobParameterFile = splitted[1]

if jobParameterFile is None:
    print ("No jobParameterFile provided, exiting.")
    sys.exit(1)

# read in job parameters
with open(jobParameterFile, "r") as parameter_file:
    jobParameter = json.load(parameter_file)

print("Got job parameters:")
pprint.pprint(jobParameter)

bpy.ops.wm.open_mainfile(filepath=jobParameter["blender_filename"])

output_folder = jobParameter["output_folder"]

assert (len(jobParameter["output_filenames"]) == len(jobParameter["object_names"]))

for i in range(len(jobParameter["output_filenames"])):
    export_obj(output_folder, jobParameter["output_filenames"][i][0], jobParameter["object_names"][i])

sys.exit(0)
