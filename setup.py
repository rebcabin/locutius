from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="locutius",
    version="1.0.0",
    author="Brian Beckman",
    author_email="bc.beckman@gmail.com",
    description=("Clojure-style multimethods with arbitrary dispatch keys."),
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="locutius,multimethod,multimethods,decorator,decorators,dispatch",
    url="https://github.com/rebcabin/locutius",
    packages=['locutius'],
    test_suite='test_locutius',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
