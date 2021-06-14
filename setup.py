#!/usr/bin/env python

from setuptools import setup

setup(
    name="Jazzify",
    version="1.0",
    description="Make a song jazzy.",
    author="Kevin Yen",
    author_email="yenkevin1203@gmail.com",
    url="https://github.com/NivekNey/Jazzify",
    packages=["jazzify"],
    requires=[
        "beautifulsoup4",
        "selenium",
        "joblib",
        "pandas",
        "tensorflow",
    ],
)
