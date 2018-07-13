import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blendomatic",
    version="0.0.1",
    author="Thomas Hauth",
    author_email="thomas.hauth@web.de",
    description="Automatic scripting and batch operations for Blender ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThomasHauth/blendomatic",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)
