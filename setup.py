import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drive-files-gen",
    version="0.0.2",
    author="Val Le Nain",
    author_email="vallenain@gmail.com",
    description="Tool to generate files on Google Drive from a JSON file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vallenain/Drive-files-generator",
    tests_require=["pytest"],
    py_modules=["drive_files_gen"],
    keywords="google-drive JSON automation",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ],
    install_requires=[
        "google-auth",
        "google-auth-oauthlib",
        "google-api-python-client",

    ],
    python_requires='>=3.6',
)
