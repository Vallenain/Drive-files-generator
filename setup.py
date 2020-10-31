import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drive-files-gen",
    version="0.0.1",
    author="Val Le Nain",
    author_email="vallenain@gmail.com",
    description="Tool to generate files on Google Drive from a JSON file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vallenain/Drive-files-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
