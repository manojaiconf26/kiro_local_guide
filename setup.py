"""Setup configuration for Chennai Local Guide."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chennai-local-guide",
    version="1.0.0",
    author="Content Creator Tools",
    description="A tool for content creators to navigate Chennai authentically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "dataclasses; python_version<'3.7'",
    ],
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "hypothesis>=6.0.0",
        ],
        "dev": [
            "black",
            "flake8",
            "mypy",
        ],
    },
)