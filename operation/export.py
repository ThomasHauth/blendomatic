import argparse
import luigi
import os
import json
import subprocess
import tempfile
import time
import logging

# try import with python3 module name first
try:
    import configparser as configparser_import
except ImportError:
    import ConfigParser as configparser_import

from .base import OperationBase

class ExportTask(luigi.Task):

    blender_filename = luigi.Parameter()
    output_filenames = luigi.Parameter()
    object_names = luigi.Parameter()
    format = luigi.Parameter()

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
            params[name] = "{}".format(getattr(self, name))

        print(
            "Checking for input file-specific config {}".format(config_filename))
        if os.path.isfile(config_filename):
            cfg_parser = configparser_import.ConfigParser()
            cfg_parser.read(config_filename)

            for sec in cfg_parser.sections():
                if sec == self.name():
                    # overwrite local settings
                    for key in cfg_parser[sec]:
                        val = cfg_parser[sec][key]
                        print(
                            "Overwriting {}.{} configuration with {} from input-file specific config file".format(sec, key, val))
                        params[key] = cfg_parser[sec][key]
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
            # subprocess.check_call(["blender",
            #                      "--background",
            #                       "--python",
            #                       os.path.abspath(
            #                       "operation/export_blender.py"),
            #                       "jobParameterFile=" + job_json.name])

    def output(self):
        config = self.compile_config()
        return [luigi.LocalTarget(ofile) for ofile in config["output_filenames"].split(",")]

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
                            help='Name of the object to export. If no name given, the '
                            'first object in the file will be exported.')

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
                    blender_filename=os.path.abspath(input_file), output_filenames=output_filenames,
                        format=args.format, object_names=args.object_names))
        return tasks

    def name(self):
        return "export"
