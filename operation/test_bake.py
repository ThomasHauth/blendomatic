import unittest

from . import bake
import os.path
import tempfile
import shutil
import subprocess

from testsupport import TempTestFolder, compare_image_file


class TestBakeTask(unittest.TestCase):

    def get_test_blendfile(self):
        return os.path.abspath("test_models/cube.blend")

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def get_test_bake_reference(self):
        return os.path.abspath("test_models/cube_bake-reference.png")

    def test_bake_single_object(self):

        # place testfile
        #blendfilename = os.path.join(tmpfolder, os.path.split(self.get_test_blendfile())[1])
        #shutil.copy( self.get_test_blendfile(), blendfilename )

        with TempTestFolder() as tmpfolder:

            bakefilename = os.path.abspath(tmpfolder.get_cube_blend_filename() + ".png")
            baketask = bake.BakeTask(blender_filename=tmpfolder.get_cube_blend_filename(),
                                   output_filenames=[[bakefilename]],
                                   output_folder=tmpfolder.get_tempfolder(),
                                   image_format="PNG",
                                   object_names=[["Cube"]],
                                   ignore_blendomatic_files=True)
            baketask.run()

            # check if file exists
            self.assertTrue(os.path.isfile(bakefilename))
            self.assertTrue(compare_image_file(bakefilename, tmpfolder.get_bakereference_filename()))


    def test_bake_cycles_single_object(self):
        with TempTestFolder() as tmpfolder:
            # place testfile
            blendfilename = os.path.join(tmpfolder.get_tempfolder(), os.path.split(self.get_test_blendfile())[1])

            bakefilename = blendfilename + ".png"
            baketask = bake.BakeTask(blender_filename=blendfilename,
                                   output_filenames=[[bakefilename]],
                                   output_folder=tmpfolder.get_tempfolder(),
                                   image_format="PNG",
                                   object_names=[["Cube"]],
                                   render_engine="cycles",
                                   ignore_blendomatic_files=True)
            baketask.run()

            # check if file exists
            self.assertTrue(os.path.isfile(bakefilename))
            #compare_image_file(bakefilename, tmpfolder.get_bakecyclesreference_filename())
