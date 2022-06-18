import setuptools
import os
import pathlib

from src.tapas_base import util_system as us

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tapas-utaustin",
    version="0.0.1",
    author="Thomas Logan",
    author_email="thomas.logan.atx@gmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/trishullab/tapas",
    project_urls={
        "Bug Tracker": "https://github.com/trishullab/tapas/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=(x := setuptools.find_packages(where="src"), print(x), x)[-1],
    python_requires=">=3.6",
    package_data = {
        'tapas_res': us.all_paths(us.project_path('tapas_res'))
    }
)