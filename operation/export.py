import abc
import argparse
import luigi
import os
import json
import subprocess
import tempfile
import time

from .base import OperationBase


class ExportTask(luigi.Task):

    blender_filename = luigi.Parameter()
    output_filename = luigi.Parameter()
    object_name = luigi.Parameter()
    format = luigi.Parameter()

    def run(self):
        with tempfile.NamedTemporaryFile(mode="w") as job_json:
            # export luigi parameters
            params = {}
            for name, val in self.get_params():
                # print (val.__dict__)
                params[name] = "{}".format(getattr(self, name))

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
        return luigi.LocalTarget(self.output_filename)

# there can be files for each blender file which overwrite certain parameters, like
# which objects to export etc...


class ExportOperation(OperationBase):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument('--format', choices=["OBJ"], default="OBJ",
                            help='The format of the exported file')
        parser.add_argument('--output-filename',
                            help='Name of the outfile, if not set the input file name'
                            'will be used with the correct extension.')
        parser.add_argument('--object-name', default="",
                            help='Name of the object to export. If no name given, the '
                            'first object in the file will be exported.')

    def generate_tasks(self, args, files, modifiers=[]):

        tasks = []
        for input_file in files:

            if args.output_filename:
                output_filename = args.output_filename
            else:
                fname_ext = os.path.splitext(os.path.abspath(input_file))
                output_filename = "{}.{}".format(
                    fname_ext[0], args.format.lower())

            tasks.append(
                ExportTask(
                    blender_filename=os.path.abspath(input_file), output_filename=output_filename,
                        format=args.format, object_name=args.object_name))
        return tasks

    def name(self):
        return "export"
