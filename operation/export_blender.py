import bpy
import os
import sys
import json
import pprint

image_output_folder = "/home/poseidon/dev/locky/assets/images/"

# export
# ~/apps/blender-2.79-linux-glibc219-x86_64/blender --background --python bexport.py action=export exportObjects=lock outputFileName=/home/poseidon/dev/locky/assets/models/padlock1.obj inputFileName=/home/poseidon/dev/locky/assets/models/padlock1.blend
#
# baking
# ~/apps/blender-2.79-linux-glibc219-x86_64/blender --background --python bexport.py action=bake bakeTextureFileName=/home/poseidon/dev/locky/assets/models/baked.png inputFileName=/home/poseidon/dev/locky/assets/models/debugbox.blend objectToBake=Cube


def unselect_all():
    for obj in bpy.data.objects:
        obj.select = False


def export_obj(obj_filename, objs_to_export):

    unselect_all()
    for obj in objs_to_export:
        o = bpy.data.objects[obj]
        # select all objects used for export
        o.select = True
        print(o)

    # call export
    bpy.ops.export_scene.obj(filepath=obj_filename, check_existing=False,
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
action = None

print (sys.argv)


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

export_obj(jobParameter["output_filenames"], [jobParameter["object_names"]])

sys.exit(0)
