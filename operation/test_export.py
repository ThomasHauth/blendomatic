import unittest

from . import export
import os.path
import tempfile
import shutil

class TestExportTask(unittest.TestCase):

    def get_test_blendfile(self):
        return os.path.abspath("test_models/cube.blend")

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def test_export_single_object(self):
        tmpfolder = tempfile.mkdtemp()

        # place testfile
        blendfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendfile())[1])
        shutil.copy( self.get_test_blendfile(), blendfilename )

        objfilename = blendfilename + ".obj"
        extask = export.ExportTask(blender_filename=blendfilename,
                                   output_filenames=[[objfilename]],
                                   output_folder=tmpfolder,
                                   format="OBJ",
                                   object_names=[["Cube"]])
        extask.run()

        # check if file exists
        self.assertTrue(os.path.isfile(os.path.join(tmpfolder, objfilename)))

        shutil.rmtree(tmpfolder)

    def test_export_multiple_objects_via_config_file(self):
        tmpfolder = tempfile.mkdtemp()

        # place testfile
        blendfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendfile())[1])
        shutil.copy( self.get_test_blendfile(), blendfilename )
        # copy configfile
        blendomaticfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendomatic_config())[1])
        shutil.copy( self.get_test_blendomatic_config(), blendomaticfilename )

        extask = export.ExportTask(blender_filename=blendfilename,
                                   format="OBJ")
        extask.run()

        # check if file exists
        self.assertTrue(os.path.isfile("first_cube.obj"))
        self.assertTrue(os.path.isfile("second_cube.obj"))

        shutil.rmtree(tmpfolder)
