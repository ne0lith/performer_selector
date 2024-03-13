from setuptools import setup

setup(
    name="performer_selector",
    version="0.1",
    description="A Python module for selecting performers from specified root directories.",
    author="ne0lith",
    author_email="ne0lith@proton.me",
    py_modules=["main"],
    install_requires=[
        "prompt_toolkit",
    ],
)
