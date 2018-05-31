#!/usr/bin/env python3
# run with python3 assets/assetbuild/assetbuild.py

import luigi
import time
import subprocess
import json

import operation.base
import operation.export

import modifiers.base
import modifiers.transform

import os
import glob
import sys
import multiprocessing
import argparse
import glob


def resolve_files(filesparameter):
    paths = filesparameter.split(";")

    # flatten nested list
    glob_paths = sum([glob.glob(p) for p in paths], [])

    return glob_paths

if __name__ == '__main__':
    operation.base.OperationBase.register(operation.export.ExportOperation)
    operations = [operation.export.ExportOperation()]

    modifiers.base.ModifierBase.register(modifiers.transform.TransformModifier)
    modifiers = [modifiers.transform.TransformModifier()]

    parser = argparse.ArgumentParser(
        description='Batch process Blender rendering with Python automation.')
    parser.add_argument('operation', help='Blender operation to run',
                        choices=[o.name() for o in operations])
    # operation: export, render, blah
    # modifiers: location, position, color etc.
    # file source: filename , text file, wild cards
    # output file names: command line, text

    args = parser.parse_args(sys.argv[1:2])
    selected_operation = [
        o for o in operations if o.name() == args.operation][0]
    operation_parser = argparse.ArgumentParser(
        description='Operation {}'.format(selected_operation.name()))
    selected_operation.add_arguments(operation_parser)
    operation_args = operation_parser.parse_args(sys.argv[2:])

    input_files = resolve_files(operation_args.filenames)
    tasks = selected_operation.generate_tasks(operation_args, input_files)

    luigi.build(
        tasks,
        local_scheduler=not operation_args.central_scheduler,
     workers=4)
