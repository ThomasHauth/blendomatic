import abc

from .base import ModifierBase


class TransformModifier(ModifierBase):

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            '--modifier-transform', default=false, action="store_true",
                            help='Add a transform modifier')
        parser.add_argument('--modifier-transform-scale', default="1,1,1",
                            help='Scale factors for x,y and z axis'
                            'will be used with the correct extension.')

    def name(self):
        return "transform"
