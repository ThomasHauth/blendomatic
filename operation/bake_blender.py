
def bake_texture( baked_texture_filename, obj_to_bake):

    unselect_all()
    obj = bpy.data.objects[obj_to_bake]
    bpy.context.scene.objects.active = obj
    obj.select = True
    bpy.ops.object.mode_set(mode='OBJECT')

    # Set bake margins ( I guess we don't need this )
    # bpy.context.scene.render.bake_margin = 2

    if len(obj.data.uv_textures) == 0:
        # no texture assigned, bail out
        print ("Object {} cannot be baked, because no image assigned".format(obj_to_bake))
        return

    # always take the first image assigned to this object
    img = obj.data.uv_textures[0].data[0].image
    print(obj.data.uv_textures[0].data[0].image)
    if img is None:
        # no texture assigned, bail out
        print ("Object {} cannot be baked, because image assigned but data not valid".format(obj_to_bake))
        return

    # select all we need
    bpy.ops.object.mode_set(mode='EDIT' ,toggle=False)
    bpy.ops.mesh.select_all(action='SELECT')
    obj.select = True
    bpy.context.scene.objects.active = obj
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    # bpy.data.screens['UV Editing'].areas[1].spaces[0].image = img

    try:
        # bake() uses cycles, bake_image() the blender renderer ....
        bpy.ops.object.bake()
    except RuntimeError as re:
        print ("Object {} cannot be baked, because not properly setup".format(obj_to_bake))
        return

    if baked_texture_filename is None:
        # auto-generate:
        img_fname = os.path.basename(os.path.abspath(img.filepath_raw)).split(".")
        img_fname_bake = img_fname[0] + "-bake." + img_fname[1]
        baked_texture_filename = image_output_folder + img_fname_bake

    img.filepath_raw = baked_texture_filename
    img.file_format = "PNG"
    img.save()
