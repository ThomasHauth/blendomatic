import os
import sys
import bpy

# add the path to this file as the python path so we can
# import additional python code
blendomatic_python_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(blendomatic_python_path)

import blenderutil

def bake_texture(obj_to_bake, image_format, baked_texture_filename):

    obj = blenderutil.select_objects([obj_to_bake])[0]
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set bake margins ( I guess we don't need this )
    # bpy.context.scene.render.bake_margin = 2

    if len(obj.data.uv_textures) == 0:
        # no texture assigned, bail out
        print ("Object {} cannot be baked, because no image assigned".format(obj_to_bake))
        return False

    # always take the first image assigned to this object
    #img = obj.data.uv_textures[0].data[0].image
    #if img is None:
    #    # no texture assigned, bail out
    #    print ("Object {} cannot be baked, because image assigned but data not valid".format(obj_to_bake))
    #    return False
    #print("Selected image for baking {} ".format(img))

    # select all we need
    bpy.ops.object.mode_set(mode='EDIT' ,toggle=False)
    bpy.ops.mesh.select_all(action='SELECT')

    #bpy.ops.uv.smart_project()
    #bpy.ops.uv.select_all(action='SELECT')

    obj.select = True
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # bpy.data.screens['UV Editing'].areas[1].spaces[0].image = img



    currentImageName = "new_bake"
    bake_target = bpy.data.images.new(name=currentImageName, width=1024, height=1024)
    bake_target.filepath_raw = baked_texture_filename
    bake_target.file_format = image_format

    print("Target {}".format(bake_target))

    # Specify the bake type
    bpy.data.scenes["Scene"].render.bake_type = "FULL" #"TEXTURE"

    for uv in obj.data.uv_textures:
        print (uv)
    obj.data.uv_textures[0].active = True

    bpy.ops.object.mode_set(mode='OBJECT')
    # Set the target image
    for d in obj.data.uv_textures[0].data:
        d.image = bake_target

    try:
        # bake() uses cycles, bake_image() the blender renderer ....
        bpy.ops.object.bake_image() #( save_mode="EXTERNAL", filepath="deine-mutter.png")#type="COMBINED", save_mode="EXTERNAL", filepath="deine-mutter.png")
    except RuntimeError as re:
        print ("Runtime Error {}".format(re))
        print ("Object {} cannot be baked, because not properly setup".format(obj_to_bake))
        return

    #if baked_texture_filename is None:
    #    # auto-generate:
    #    img_fname = os.path.basename(os.path.abspath(img.filepath_raw)).split(".")
    #    img_fname_bake = img_fname[0] + "-bake." + img_fname[1]
    #    baked_texture_filename = image_output_folder + img_fname_bake

    bake_target.save()

jobParameter = blenderutil.parse_jobinput()

bpy.ops.wm.open_mainfile(filepath=jobParameter["blender_filename"])
output_folder = jobParameter["output_folder"]

assert (len(jobParameter["output_filenames"]) == len(jobParameter["object_names"]))

for i in range(len(jobParameter["output_filenames"])):
    # we only support baking one object atm.
    if bake_texture(jobParameter["object_names"][i][0],
                    jobParameter["image_format"],
                    jobParameter["output_filenames"][i][0]) == False:
        sys.exit(1)


bpy.ops.wm.save_as_mainfile(filepath="after_bake.blend")
sys.exit(0)
