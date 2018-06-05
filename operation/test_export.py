import unittest

import export
import os.path
import tempfile
import shutil

class TestExportTask(unittest.TestCase):

    def get_test_blendfile(self):
        return os.path.abspath("test_models/cube.blend")

    def test_export_single_object(self):
        tmpfolder = tempfile.mkdtemp()

        print (tmpfolder)
        # place testfile
        blendfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendfile())[1])
        shutil.copy( self.get_test_blendfile(), blendfilename )

        objfilename = blendfilename + ".obj"
        extask = export.ExportTask(blender_filename=blendfilename,
                                   output_filenames=objfilename,
                                   format="OBJ",
                                   object_names="Cube")
        extask.run()

        # check if file exists
        self.assertTrue(os.path.isfile(objfilename))

        shutil.rmtree(tmpfolder)
