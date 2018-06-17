
import unittest
import subprocess
import tempfile
import shutil
import os


class IntegrationTest(unittest.TestCase):

    def assertFileExists(self, filename):
        self.assertTrue(os.path.isfile(filename), "File {} does not exist".format(filename))



class TempTestFolder(object):

    def __init__(self, multipleFolders=False):
        self.multipleFolders = multipleFolders
        self.folderA = None
        self.folderB = None

    def get_test_blendfiles(self):

        testfile_folder = "test_models"
        # return os.path.abspath("test_models/cube.blend")
        return [ os.path.join(testfile_folder, f) for f in ["monkey.blend", "cube.blend", "sphere.blend",
                                                            "cube.blendomatic"]]

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def place_testfiles(self, tmpfolder):
        # place testfile

        self.folderA = os.path.join(tmpfolder, "folderA")
        self.folderB = os.path.join(tmpfolder, "folderB")

        if self.multipleFolders:
            os.mkdir(self.folderA)
            os.mkdir(self.folderB)

        i = 0
        for f in self.get_test_blendfiles():
            target_folder = tmpfolder
            if self.multipleFolders:
                target_folder = self.folderA if i == 0 else self.folderB

            shutil.copy(f, target_folder)
            i = i + 1

    def __enter__(self):
        self.tmpfolder = tempfile.mkdtemp()

        # transfer test models and config files
        self.place_testfiles(self.tmpfolder)

        # change working dir
        self.current_wd = os.getcwd()
        os.chdir(self.tmpfolder)

        return self.tmpfolder

    def __exit__(self, ex_type, ex_val, ex_tb):
        # make sure to move back to the previous directory
        os.chdir(self.current_wd)
        shutil.rmtree(self.tmpfolder)


class BlendomaticIntegration(IntegrationTest):

    def test_export(self):
        mainfile = os.path.abspath("blendomatic.py")

        with TempTestFolder() as tmpfolder:
            subprocess.check_call([mainfile, "export", "--filenames", "{}/*.blend".format(tmpfolder),
                                   "--output-folder", str(tmpfolder)])

            # check if the output files have been generated
            # easy export of one model
            self.assertFileExists(os.path.join( tmpfolder, "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder, "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder, "both_cubes.obj"))




    def test_output_same_folder_as_blend_file(self):
        mainfile = os.path.abspath("blendomatic.py")

        with TempTestFolder(multipleFolders=True) as tmpfolder:
            # don't give an output folder option, this means
            subprocess.check_call([mainfile, "export", "--filenames",
                                   "folderA/*.blend;folderB/*.blend;"])

            # check if the output files have been generated

            # easy export of one model, must be in the folder the model is also located
            self.assertFileExists(os.path.join( tmpfolder,"folderA", "monkey.obj"))

            # export of different subset of models from one file
            self.assertFileExists(os.path.join( tmpfolder,"folderB", "first_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder,"folderB", "second_cube.obj"))
            self.assertFileExists(os.path.join( tmpfolder,"folderB", "both_cubes.obj"))


