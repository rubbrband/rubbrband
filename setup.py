from setuptools import find_packages, setup

setup(
    name="rubbrband",
    install_requires=["docker==6.0.1", "yaspin", "typer[all]"],
    include_package_data=True,
    packages=find_packages(),
)
