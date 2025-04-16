from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "hidapi_py",
        ["src/hidapi_py/bindings.cpp"],
        include_dirs=[pybind11.get_include()],
        language="c++",
    ),
]

setup(
    name="hidapi_py",
    version="0.1.0",
    author="Benjamin Heuberger",
    author_email="beni.heu@gmail.com",
    description="Python wrapper for HIDAPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    packages=["hidapi_py"],
    package_dir={"": "src"},
    zip_safe=False,
)