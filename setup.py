import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="opendbf",
    version="0.0.1",
    author="Fangchen Li",
    author_email="fangchen.li@outlook.com",
    description="A pure python dbf file reader.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VirosaLi/opendbf",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        "Programming Language :: Python :: 3",
        'Typing :: Typed',
        'License :: OSI Approved :: BSD License',
        "Operating System :: OS Independent",
        'Natural Language :: English',
    ],
    python_requires=">=3.7",
)
