#!/usr/bin/env python

import os
import os.path
import sys
from setuptools import setup  # noqa

pure = None
if '--pure' in sys.argv:
    pure = True
    sys.argv.remove('--pure')
elif '--universal' in sys.argv:
    pure = True


with open("DESCRIPTION.md", "r") as fh:
    long_description = fh.read()


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import versioneer  # noqa
del sys.path[0]

try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = pure

except ImportError:
    bdist_wheel = None


if __name__ == "__main__":
    cmds = versioneer.get_cmdclass()
    cmds['bdist_wheel'] = bdist_wheel

    extras = {}
    setup(
        name="multievent",
        version=versioneer.get_version(),
        description="Wait for multiple events simultaneously",  # noqa
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
        cmdclass=cmds,
        **extras
    )
