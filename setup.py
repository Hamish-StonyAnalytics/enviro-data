from setuptools import setup, find_packages

setup(
    name="TRCJupyter",
    version="0.1",
    packages=find_packages(include=["scripts", "scripts.*"])
)