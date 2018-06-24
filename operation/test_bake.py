import unittest

from . import bake
import os.path
import tempfile
import shutil

class TestBakeTask(unittest.TestCase):

    def get_test_blendfile(self):
        return os.path.abspath("test_models/cube.blend")

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def test_bake_single_object(self):
        tmpfolder = tempfile.mkdtemp()

        # place testfile
        blendfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendfile())[1])
        shutil.copy( self.get_test_blendfile(), blendfilename )

        bakefilename = blendfilename + ".png"
        baketask = bake.BakeTask(blender_filename=blendfilename,
                               output_filenames=[[bakefilename]],
                               output_folder=tmpfolder,
                               image_format="PNG",
                               object_names=[["Cube"]])
        baketask.run()

        # check if file exists
        self.assertTrue(os.path.isfile(os.path.join(tmpfolder, bakefilename)))

        shutil.rmtree(tmpfolder)

