from setuptools import find_packages, setup

setup(
    name="prm-spine-exporter",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)
