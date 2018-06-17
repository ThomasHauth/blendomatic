
import bpy
import sys
import pprint
import json

def unselect_all():
    for obj in bpy.data.objects:
        obj.select = False

def select_all_objects():
    select_objects([""])

def select_objects(objs_to_export):
    """
    Selects objects in blender so they can be used for later operations
    :param objs_to_export: Name of the objects to select, or select all
        objects if there is one entry in the array with an empty string
    :return: None
    """

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


def parse_jobinput():
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
    return jobParameter