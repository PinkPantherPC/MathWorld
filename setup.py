from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as documentation:
    long_description = documentation.read()

setup(
    name="mathworld",
    version="0.1.0",
    description="A python module for using sympy with analytic geometry",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PinkPantherPC/MathWorld",
    author="Tobia Petrolini",
    license="MIT",

    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.10",

    install_requires=[
        "sympy>=1.13.3",
    ],

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education"
        "Intended Audience :: Developers"
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],

    keywords="math geometry analytic line point sympy symbolic calculation CAS",
)
