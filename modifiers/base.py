import abc
import argparse


class ModifierBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_arguments(self, parser):
        pass

    @abc.abstractmethod
    def name(self):
        pass
