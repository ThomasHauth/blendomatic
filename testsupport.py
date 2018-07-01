
import tempfile
import shutil
import os
import subprocess


def compare_image_file(referencefile, inputfile, threshold=10):
    # compare file
    try:
        compare_cmd = ["compare", "-metric", "fuzz", inputfile, referencefile, "__out__diff.png"]
        print ("Executing compare : {}".format(compare_cmd))
        subprocess.check_output(compare_cmd,
                                stderr=subprocess.STDOUT)
        # if the exit is 0, the files were exactly the same
        print("Files are equal")
        return True
    except subprocess.CalledProcessError as cpe:
        # parse the metric for the difference
        diff_metric = str(cpe.output).split(" ")
        if len(diff_metric) > 0:
            diff_metric = float(diff_metric[0])
            print ("Comparison Metric {} between {} and {}".format(diff_metric, inputfile, referencefile))
            if diff_metric < threshold:
                return True

    return False


class TempTestFolder(object):

    def __init__(self, multipleFolders=False):
        self.multipleFolders = multipleFolders
        self.folderA = None
        self.folderB = None

    def get_test_blendfiles(self):

        testfile_folder = "test_models"
        # return os.path.abspath("test_models/cube.blend")
        return [ os.path.join(testfile_folder, f) for f in ["monkey.blend", "cube.blend", "sphere.blend",
                                                            "cube.blendomatic",
                                                            # textures
                                                            "debug-texture-cube.png",
                                                            # reference images
                                                            "cube_bake-reference.png"]]

    def get_tempfolder(self):
        return self.tmpfolder

    def get_test_blendomatic_config(self):
        return os.path.abspath("test_models/cube.blendomatic")

    def get_cube_blend_filename(self):
        return os.path.join(self.tmpfolder, "cube.blend")

    def get_bakereference_filename(self):
        return os.path.join(self.tmpfolder,"cube_bake-reference.png")

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

        return self

    def __exit__(self, ex_type, ex_val, ex_tb):
        # make sure to move back to the previous directory
        os.chdir(self.current_wd)
        shutil.rmtree(self.tmpfolder)
