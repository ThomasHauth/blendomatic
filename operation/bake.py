import luigi
import os
from . import blendertask

from .base import OperationBase

class BakeTask(blendertask.BlenderTask):

    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    output_filenames = luigi.ListParameter(default=[])
    # nested list, because every object output file can have multiple object_names to
    # be contained in this output file
    object_names = luigi.ListParameter(default=[])

    output_folder = luigi.Parameter(default="")
    image_format = luigi.Parameter()

    def output(self):
        config = self.compile_config()
        # nested list
        return [[luigi.LocalTarget( os.path.join(self.output_folder, os.path.basename(nested_file))) for nested_file in ofile] for ofile in config["output_filenames"]]

    def name(self):
        return "bake"

    def blender_python(self):
        return "bake_blender.py"

# there can be files for each blender file which overwrite certain parameters, like
# which objects to export etc...

class BaketOperation(OperationBase):

    def add_arguments(self, parser):
        super(BaketOperation, self).add_arguments(parser)

        parser.add_argument('--image-format', choices=["PNG","JPEG"], default="PNG",
                            help='The format of the baked image file')
        parser.add_argument('--output-filenames',
                            help='Name of the outfile, if not set the input file name'
                            'will be used with the correct extension.')
        parser.add_argument('--object-names', default="",
                            help='Name of the objects to bake.')

    def generate_tasks(self, args, files, modifiers=[]):
        tasks = []
        for input_file in files:

            if args.output_filenames:
                output_filenames = args.output_filenames
            else:
                fname_ext = os.path.splitext(os.path.abspath(input_file))
                output_filenames = "{}.{}".format(
                    fname_ext[0], args.image_format.lower())

            tasks.append(
                    BakeTask(
                        blender_filename=os.path.abspath(input_file), output_filenames=[[output_filenames]],
                            output_folder=args.output_folder,
                            image_format=args.image_format, object_names=[[args.object_names]]))
        return tasks


    def name(self):
        return "bake"
