
import unittest
import subprocess
import os
from testsupport import TempTestFolder


class IntegrationTest(unittest.TestCase):

    def assertFileExists(self, filename):
        self.assertTrue(os.path.isfile(filename), "File {} does not exist".format(filename))


class BlendomaticIntegration(IntegrationTest):

    def test_export(self):
        mainfile = os.path.abspath("blendomatic.py")

        with TempTestFolder() as tmpfolder:
            subprocess.check_call([mainfile, "export", "--filenames", "{}/*.blend".format(tmpfolder.get_tempfolder()),
                                   "--output-folder", str(tmpfolder.get_tempfolder())])

            # check if the output files have been generated
            # easy export of one model
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(), "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(), "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(), "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(), "both_cubes.obj"))

    def test_bake(self):
        mainfile = os.path.abspath("blendomatic.py")

        with TempTestFolder() as tmpfolder:
            subprocess.check_call([mainfile, "bake", "--filenames", "{}/cube.blend".format(tmpfolder.get_tempfolder()),
                                   "--output-folder", str(tmpfolder.get_tempfolder())])

            # check if the output files have been generated
            # baked render of the cube
            self.assertFileExists(os.path.join(tmpfolder.get_tempfolder(), "cube_bake.png"))


    def test_output_same_folder_as_blend_file(self):
        mainfile = os.path.abspath("blendomatic.py")

        with TempTestFolder(multipleFolders=True) as tmpfolder:
            # don't give an output folder option, this means
            subprocess.check_call([mainfile, "export", "--filenames",
                                   "folderA/*.blend;folderB/*.blend;"])

            # check if the output files have been generated

            # easy export of one model, must be in the folder the model is also located
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(),"folderA", "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(),"folderB", "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(),"folderB", "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder.get_tempfolder(),"folderB", "both_cubes.obj"))


