from setuptools import setup, find_namespace_packages

setup(
    name="helper",
    version="1",
    description="Command line helper",
    author="Sergiy Ponomarenko",
    license="MIT",
    include_package_data=True,
    packages=find_namespace_packages(),
    entry_points={"console_scripts": ["assistant = console_helper.CLI:main"]},
)
