from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="spacy_space",
    version="0.0.0-alpha01",
    packages=find_packages(),
    install_requires=requirements,
    description="spacy_space : add adequate spaces in-between single sentences via spaCy",
    license="MIT",
    keywords=[
        "NLP",
        "natural language processing",
        "computational linguistics",
        "linguistics",
        "language",
        "natural language",
        "text analytics",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
)