from setuptools import setup, find_packages

REQUIRED_PACKAGES = [
    "spacy<=3.7.2",
    # "numpy", # spaCy already depends on numpy
]

setup(
    name="spacy_space",
    version="0.0.0-alpha03",
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
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
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
    ],
)