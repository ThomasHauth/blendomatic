import abc
import argparse


class OperationBase(metaclass=abc.ABCMeta):

    def add_arguments(self, parser):
        parser.add_argument('--filenames', required=True,
                            help='Name of the file to import. This supports flexfiles.')
        parser.add_argument('--worker', type=int,
                            help='The number of woker processes to use')
        parser.add_argument('--central-scheduler', action='store_true',
                            help='Use local scheduler instead to connect to central one',
                            default=False)
        parser.add_argument('--blender-executable',
                            help='Path to the blender executable to use',
                            default="blender")

    @abc.abstractmethod
    def name(self, lbah):
        pass