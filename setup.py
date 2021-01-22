import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loop-destroyer-mattyonweb", # Replace with your own username
    version="0.0.3",
    author="Jacopo Belbo",
    author_email="kfgodel@autistici.org",
    description="A loop destroyer, in the vein of William Basinsky",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'loop-destroyer = loop_destroyer.loop_destroyer:launcher',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        # "License :: OSI Approved :: MIT License",
        # "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
