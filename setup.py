from setuptools import setup, find_packages

setup(
    name="grafos",
    version="0.1",
    packages=find_packages(where="contenidos/_static/code"),
    package_dir={"": "contenidos/_static/code"},
    include_package_data=True,
    description="Código de grafos para apuntes UNTREF-EDD",
    author="UNTREF-EDD",
    python_requires=">=3.8",
)
