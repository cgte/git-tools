from setuptools import setup, find_packages
import sys, os

version = "0.3.dev0"

setup(
    name="git-tools",
    version=version,
    description="Tools for everyday git use",
    long_description="""\
""",
    classifiers=[],
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords="git",
    author="Colin Goutte",
    author_email="cgte@bk.ru",
    url="https://github.com/cgte/git-tools",
    license="GNU GPL v3",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points={
        "console_scripts": [
            "autorebase = gittools.autorebase:main",
            "syncgitdir = gittools.syncrepodir:main",
            "syncfeatures = gittools.syncfeatures:main",
            "listopen = gittools.listopen:main",
            "autoclean = gittools.autoclean:main",
            "listold = gittools.listold:main",
            "diagnose = gittools.diagnose:main",
        ]
    },
)
