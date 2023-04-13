# coding: utf-8
import pkg_resources
import setuptools
import os
from pathlib import Path

VERSION = "1.0.6"

install_requires = []
for req_file in ["requirements.txt"]:
  file_path = os.path.join(Path('.'), req_file)
  with open(file_path) as requirements_txt:
      install_requires.extend([
          str(requirement)
          for requirement
          in pkg_resources.parse_requirements(requirements_txt)
      ])

lib = "NNTrade.source.market"

libs = [f"{lib}.{pkg}" for pkg in setuptools.find_packages(where="src")]
libs.append(lib)

setuptools.setup(
    name=lib,
    version=VERSION,
    description="market source lib",
    author_email="",
    url="",
    keywords=["market", "source"],
    install_requires=install_requires,
    packages=libs,
    package_dir={lib: 'src'},
    include_package_data=True,
    long_description="""\
    Library to get, store and work with market quotes and indicators
    """
)
