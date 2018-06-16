#!/usr/bin/env python

import luigi
import operation.export
import modifiers.transform

import sys
import argparse
import glob


def resolve_files(filesparameter):
    paths = filesparameter.split(";")

    # flatten nested list
    # only python => 3.5 supports recursive globs
    if (sys.version_info[0] >= 3) and (sys.version_info[1] >= 5):
        glob_paths = sum([glob.iglob(p, recursive=True) for p in paths], [])
    else:
        glob_paths = sum([glob.glob(p) for p in paths], [])

    return glob_paths

if __name__ == '__main__':
    operations = [operation.export.ExportOperation()]
    modifiers = [modifiers.transform.TransformModifier()]

    parser = argparse.ArgumentParser(
        description='Batch process Blender rendering and exporting with Python automation.')
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
