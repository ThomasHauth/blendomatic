import luigi
import os
from . import blendertask

from .base import OperationBase

class ExportTask(blendertask.BlenderTask):

    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    output_filenames = luigi.ListParameter(default=[])
    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    object_names = luigi.ListParameter(default=[])

    output_folder = luigi.Parameter(default="")
    format = luigi.Parameter()

    def output(self):
        config = self.compile_config()
        # nested list
        return [[luigi.LocalTarget( os.path.join(self.output_folder, os.path.basename(nested_file))) for nested_file in ofile] for ofile in config["output_filenames"]]

    def name(self):
        return "export"

    def blender_python(self):
        return "export_blender.py"

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
