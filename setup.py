#!/usr/bin/env python

import os
import os.path
import sys
from setuptools import setup  # noqa

with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import versioneer  # noqa

del sys.path[0]


if __name__ == "__main__":
    extras = {}
    setup(
        name="ptvsd",
        version=versioneer.get_version(),
        description="Remote debugging server for Python support in Visual Studio and Visual Studio Code",  # noqa
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        author="Karthik Nadig",
        author_email="karthiknadig@gmail.com",
        url="https://github.com/karthiknadig/multievent",
        python_requires=">=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Debuggers",
            "Operating System :: OS Independent",
            "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
            "License :: OSI Approved :: MIT License",
        ],
        package_dir={"": "src"},
        packages=["multievent"],
        cmdclass=versioneer.get_cmdclass(),
        **extras
    )
