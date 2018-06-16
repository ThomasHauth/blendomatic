
import unittest
import subprocess
import tempfile
import shutil
import os


class IntegrationTest(unittest.TestCase):

    def assertFileExists(self, filename):
        self.assertTrue(os.path.isfile(filename), "File {} does not exist".format(filename))



class TempTestFolder(object):

    def get_test_blendfiles(self):

        testfile_folder = "test_models"
        #return os.path.abspath("test_models/cube.blend")
        return [ os.path.join(testfile_folder, f) for f in ["cube.blend", "monkey.blend", "sphere.blend",
                                                            "cube.blendomatic"]]

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def place_testfiles(self, tmpfolder):
        # place testfile
        for f in self.get_test_blendfiles():
            shutil.copy( f, tmpfolder)

    def __enter__(self):
        self.tmpfolder = tempfile.mkdtemp()

        # transfer test models and config files
        self.place_testfiles(self.tmpfolder)

        return self.tmpfolder

    def __exit__(self, ex_type, ex_val, ex_tb):
        shutil.rmtree(self.tmpfolder)


class BlendomaticIntegration(IntegrationTest):

    def test_filediscorvey(self):

        with TempTestFolder() as tmpfolder:
            subprocess.check_call(["./blendomatic.py", "export", "--filenames", "{}/*.blend".format(tmpfolder),
                                   "--output-folder", str(tmpfolder)])

            # check if the output files have been generated
            # easy export of one model
            self.assertFileExists(os.path.join( tmpfolder, "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder, "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "both_cubes.obj"))




    def test_output_same_folder_as_blend_file(self):

        with TempTestFolder() as tmpfolder:
            subprocess.check_call(["./blendomatic.py", "export", "--filenames", "test_models/*.blend",
                                   "--output-folder", str(tmpfolder)])

            # check if the output files have been generated

            # easy export of one model
            self.assertFileExists(os.path.join( tmpfolder, "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder, "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "both_cubes.obj"))


