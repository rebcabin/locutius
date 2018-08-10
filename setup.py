from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="locutius",
    version="1.0.2",
    author="Brian Beckman",
    author_email="bc.beckman@gmail.com",
    description=("Speaking multimethods and conditional term "
                 "rewriting into Python from Clojure and Mathematica."),
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="locutius,clojure,mathematica,multimethod,multimethods,decorator,"
             "decorators,dispatch,term-rewriting,conditional-term-rewriting",
    url="https://github.com/rebcabin/locutius",
    packages=['locutius'],
    test_suite='tests',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
