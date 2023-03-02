from setuptools import find_packages, setup

setup(
    name="rubbrband",
    install_requires=["docker>=6.0.0", "yaspin", "typer>=0.7.0", "rich"],
    include_package_data=True,
    packages=find_packages(),
)
