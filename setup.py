import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loop-destroyer", # Replace with your own username
    version="0.1.0",
    author="Jacopo Belbo",
    author_email="kfgodel@autistici.org",
    description="A loop destroyer, for your personal disintegration loops.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattyonweb/loop-destroyer",
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'loop-destroyer = loop_destroyer.loop_destroyer:launcher',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Multimedia :: Sound/Audio"
    ],
    python_requires='>=3.7',
)
