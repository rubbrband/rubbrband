from setuptools import find_packages, setup

setup(
    name="rubbrband",
    install_requires=["requests"],
    include_package_data=True,
    packages=find_packages(),
)
