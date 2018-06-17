import os
import luigi
import tempfile
import json
import subprocess

# try import with python3 module name first
try:
    import configparser as configparser_import
except ImportError:
    import ConfigParser as configparser_import

from blendomaticutil import  parse_list_string


class BlenderTask(luigi.Task):

    blender_filename = luigi.Parameter()

    parse_as_lists = ["output_filenames", "object_names"]

    def compile_config(self):
        """
        Combines the luigi task parameters with what is configured in the .blendomatic file
        """

        # if there is not output folder configured, use folder where the
        # blend file is located
        if self.output_folder == "":
            self.output_folder = os.path.split(os.path.abspath(self.blender_filename))[0]

        # check if there is a special configuration for this input file
        config_filename = os.path.splitext(
            os.path.abspath(self.blender_filename))[0] + ".blendomatic"

        # export luigi parameters
        params = {}
        for name, val in self.get_params():
            params[name] = getattr(self, name)

        print(
            "Checking for input file-specific config {}".format(config_filename))
        if os.path.isfile(config_filename):
            cfg_parser = configparser_import.ConfigParser()
            cfg_parser.read(config_filename)

            for sec in cfg_parser.sections():
                if sec == self.name():
                    # overwrite local settings
                    for key, val in cfg_parser.items(sec):
                        print("Overwriting {}.{} configuration with {} from input-file specific config file".format(sec, key, val))
                        if key in self.parse_as_lists:
                            val = parse_list_string(val)
                        params[key] = val

        # expand parameters

        return params

    def run(self):
        with tempfile.NamedTemporaryFile(mode="w") as job_json:

            params = self.compile_config()

            # write as json to tmp file
            json_string = json.dump(params, job_json)
            # job_json.write(str(json_string))
            job_json.flush()

            # we have to generate a json file (or a python file with the
            # parameters)
            this_python_path = os.path.dirname(os.path.realpath(__file__))
            subprocess.check_call(["blender",
                                   "--background",
                                   "--python",
                                   os.path.join(this_python_path, "export_blender.py"),
                                   "jobParameterFile=" + job_json.name])
