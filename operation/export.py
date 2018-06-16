import luigi
import os
import json
import subprocess
import tempfile

# try import with python3 module name first
try:
    import configparser as configparser_import
except ImportError:
    import ConfigParser as configparser_import

from .base import OperationBase
from blendomaticutil import  parse_list_string

class ExportTask(luigi.Task):

    blender_filename = luigi.Parameter()
    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    output_filenames = luigi.ListParameter(default=[])
    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    object_names = luigi.ListParameter(default=[])

    output_folder = luigi.Parameter(default=".")
    format = luigi.Parameter()

    parse_as_lists = ["output_filenames", "object_names"]

    def compile_config(self):
        """
        Combines the luigi task parameters with what is configured in the .blendomatic file
        """

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
            subprocess.check_call(["blender",
                                   "--background",
                                   "--python",
                                   os.path.abspath(
                                   "operation/export_blender.py"),
                                   "jobParameterFile=" + job_json.name])

    def output(self):
        config = self.compile_config()
        # nested list
        return [[luigi.LocalTarget( os.path.join(self.output_folder, os.path.basename(nested_file))) for nested_file in ofile] for ofile in config["output_filenames"]]

    def name(self):
        return "export"
# there can be files for each blender file which overwrite certain parameters, like
# which objects to export etc...

class ExportOperation(OperationBase):

    def add_arguments(self, parser):
        super(ExportOperation, self).add_arguments(parser)

        parser.add_argument('--format', choices=["OBJ"], default="OBJ",
                            help='The format of the exported file')
        parser.add_argument('--output-filenames',
                            help='Name of the outfile, if not set the input file name'
                            'will be used with the correct extension.')
        parser.add_argument('--object-names', default="",
                            help='Name of the object to export. If no name is given, all '
                            'objects in the file will be exported.')

    def generate_tasks(self, args, files, modifiers=[]):
        tasks = []
        for input_file in files:

            if args.output_filenames:
                output_filenames = args.output_filenames
            else:
                fname_ext = os.path.splitext(os.path.abspath(input_file))
                output_filenames = "{}.{}".format(
                    fname_ext[0], args.format.lower())

            tasks.append(
                    ExportTask(
                        blender_filename=os.path.abspath(input_file), output_filenames=[[output_filenames]],
                            output_folder=args.output_folder,
                            format=args.format, object_names=[[args.object_names]]))
        return tasks


    def name(self):
        return "export"
