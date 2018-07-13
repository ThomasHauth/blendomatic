.. _introduction:
.. highlight:: bash

***********
blendomatic
***********

.. image:: https://api.travis-ci.org/ThomasHauth/blendomatic.svg?branch=master
   :target: https://travis-ci.org/ThomasHauth/blendomatic

Introduction
============

Blendomatic helps you to automated exporting content (models, baked textures etc) from your blend files. It can be
configured to be part of the asset pipeline of your game or other media project. Blendomatic provides some common
operations on blend files and you can modify them or provide custom operations required by your project. Here is
an example how blenomatic exports objects from all blend files in one folder::

    blendomatic.py export --format 3DS --filenames "test_models/*.blend"

Installation instructions
=========================
TODO

Operations
==========

At the heart of blendomatic are operations. Operations which are useful for most projects come together with
blendomatic:

* export

Exports one or more objects from a blend file into a file format of your choice.

* baking

Bakes various properties like lighting, normal map etcetera onto a texture and stores this texture in a format of
your choice.

Command line
============

The easiest way to use blendomatic is to provide all configuration via the command line. Some command line options
are common, no matter which operation you select. A required parameter is the --input-files which allows you to
select one blend file or multiple using * as wildcard as Input. The selected operation will then be executed for
each blend matching the input-files list.

Blendomatic files
=================
Often you want to run one operation for all files in your asset folder and even though the same operation is executed,
some parameters might differ for each blend file. For example, for some blend files you just want to export one object
while for others you wanto export multiple objects in one file.

to allow a more fine grained customization than possible on the command line, you can create a blendomatic file which
has the same name as your blend file, but uses . blendomatic as file ending. So a blend file monkey.blend would get a
blendomatic file named monkey.blendomatic in the same folder. This files will be automatically picked up by blendomatic
and set all the parameters of the selected operation. Here is a simple example of a blendomatic file which specifies
some parameters for the export and bake operations.

Luigi and content change discovery
==================================

Blendomatic will automatically check if the output files for a bake and export operation already exist and not
execute the operation of they do. This speeds up the asset creation of projects significantly. If you still want
blendomatic to execute all operations, you can use the --force-operations (to be implemented)




